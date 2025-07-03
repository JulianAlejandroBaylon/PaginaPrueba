from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import locale
from flask import flash

app = Flask(__name__)
locale.setlocale(locale.LC_TIME, 'es_ES.utf8') 

DIAS_SEMANA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
         'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']


registros = []
app.secret_key = 'jhdkasdhuagfifhaksdhaidjas'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        guardar_registro()
        return redirect(url_for('home'))   

    fechas = generar_fechas()
    horarios = generar_horarios()

    return render_template('index.html', fechas=fechas, horarios=horarios, registros=registros)


def generar_fechas():
    hoy = datetime.now()
    fechas = []
    cantidad_dias = 10
    agregados = 0
    actual = hoy

    while agregados < cantidad_dias:
        if actual.weekday() != 6:
            dia_semana = DIAS_SEMANA[actual.weekday()]
            dia = actual.day
            mes = MESES[actual.month - 1]
            fecha_str = f"{dia_semana} {dia:02d} de {mes}"
            fechas.append(fecha_str)
            agregados += 1
        actual += timedelta(days=1)

    return fechas

def generar_horarios():
    return [f"{h:02d}:00" for h in range(10, 17)]

def guardar_registro():

    nombre = request.form['nombre']
    telefono = request.form['telefono']
    dia = request.form['fecha']
    hora = request.form['hora']

    for r in registros:
        if r['dia'] == dia and r['hora'] == hora:
            flash(f"Ya existe un registro para {dia} a las {hora}.")
            return

    registros.append({
        'nombre': nombre,
        'telefono': telefono,
        'dia': dia,
        'hora': hora,
        'estado': 'pendiente' 
    })

@app.route('/confirmar', methods=['POST'])
def confirmar_registro():
    index = int(request.form['index'])
    if 0 <= index < len(registros):
        registros[index]['estado'] = 'confirmado'
    return redirect(url_for('home'))

@app.route('/reprogramar_registro', methods=['POST'])
def reprogramar_registro():
    index = int(request.form['index'])
    if 0 <= index < len(registros):
        registros[index]['estado'] = 'reprogramando'
    return redirect(url_for('home'))


@app.route('/eliminar', methods=['POST'])
def eliminar_registro():
    index = int(request.form['index'])
    if 0 <= index < len(registros):
        registros.pop(index)
    return redirect(url_for('home'))

@app.route('/guardar_reprogramacion', methods=['POST'])
def guardar_reprogramacion():
    index = int(request.form['index'])
    nueva_hora = request.form['nueva_hora']
    if 0 <= index < len(registros):
        registros[index]['hora'] = nueva_hora
        registros[index]['estado'] = 'pendiente'
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
