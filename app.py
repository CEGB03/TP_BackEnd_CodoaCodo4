from flask import Flask, jsonify, render_template, request  # Framework web para Python
from flask_mysqldb import MySQL  # Extensión para interactuar con MySQL en Flask
from datetime import datetime  # Para obtener la fecha actual
from flask_cors import CORS  # Para permitir solicitudes desde un dominio diferente (CORS)
import os  # Módulo para interactuar con el sistema operativo junto a las variables de entorno
import json  # Para trabajar con datos en formato JSON

app = Flask(__name__, template_folder='FrontEnd', static_folder='FrontEnd')
CORS(app)  # Aplica CORS a toda la aplicación

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'CEGB03.mysql.pythonanywhere-services.com')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'CEGB03')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'DEADPOOL2020')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'CEGB03$bd_codo_a_codo')

mysql = MySQL(app)


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/hola")
def hello():
    return "<p>Hola, Mundo. backend!</p>"

@app.route("/chau")
def bye():
    return "<p>chau, Mundo!</p>"

@app.route('/FrontEnd/procesar_formulario', methods=['POST'])
def procesar_formulario():
    try:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        mensaje = request.form['mensaje']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO consultas (nombre, apellido, email, telefono, consulta) VALUES (%s, %s, %s, %s, %s)",
                    (nombre, apellido, email, telefono, mensaje))
        mysql.connection.commit()
        cur.close()

        return '<script>alert("¡Consulta ingresada correctamente en la base de datos! Se lo redirige al inicio.");' \
               'window.location.href = "/";</script>'

    except Exception as e:
        return f"Error al procesar el formulario: {str(e)}"

@app.route('/FrontEnd/procesar_compra', methods=['POST'])
def procesar_compra():
    try:
        cantidad_total = 0
        id_concierto = request.form.get('id_concierto')

        recitales_seleccionados = request.form.getlist('RECITALES[]')
        cursor  = mysql.connection.cursor()

        for id_concierto in recitales_seleccionados:
            cursor.execute("SELECT cantidad FROM conciertos WHERE idConciertos = %s", (id_concierto,))
            resultado = cursor.fetchone()
            if resultado:
                cantidad_total += resultado[0]

        return render_template('consultaCompra.html', valor=cantidad_total, id_concierto=id_concierto)

    except Exception as e:
        return f"Error al procesar la compra: {str(e)}"

@app.route('/FrontEnd/cargar_compra', methods=['POST'])
def cargar_compra():
    try:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        cantidad = request.form['cantidad']

        # Obtener el idConciertos desde el campo oculto
        idConciertos_str = request.form.get('id_concierto_visible')
        idConcierto = json.loads(idConciertos_str) if idConciertos_str else []

        # Insertar datos del cliente
        cur = mysql.connection.cursor()

        # Insertar datos del cliente
        cur.execute("INSERT INTO clientes (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)",
                    (nombre, apellido, email, telefono))
        id_cliente = cur.lastrowid


        cur.execute("SELECT MAX(numero) FROM compras")
        max_numero = cur.fetchone()[0]
        numero_compra = max_numero + 1 if max_numero is not None else 1

        # Insertar datos de la compra
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            "INSERT INTO compras (numero, fecha, cantCompra, idCliente, idConcierto) VALUES (%s, %s, %s, %s, %s)",
            (numero_compra, fecha_actual, cantidad, id_cliente,
             idConcierto))  # Aquí asumo que solo tienes un concierto por compra
        id_compra = cur.lastrowid  # Obtener el idCompra recién insertado

        # Actualizar la cantidad disponible en la tabla de conciertos
        cur.execute("UPDATE conciertos SET cantidad = cantidad - %s WHERE idConciertos = %s",
                    (cantidad, idConcierto))

        # Actualizar la fila recién insertada en la tabla de clientes con el idCompra
        cur.execute("UPDATE clientes SET idCompra = %s WHERE idCliente = %s", (id_compra, id_cliente))

        mysql.connection.commit()
        cur.close()

        return '<script>alert("¡Compra realizada correctamente! Se lo redirige al inicio.");' \
               'window.location.href = "/";</script>'

    except Exception as e:
        return f"Error al procesar la compra: {str(e)}"

@app.route('/consultar/<tipo>', methods=['GET'])
def consultar(tipo):
    try:
        # Construir la consulta según el tipo
        consulta = f"SELECT * FROM {tipo}"

        # Ejecutar la consulta
        cur = mysql.connection.cursor()
        cur.execute(consulta)
        resultados = cur.fetchall()
        cur.close()

        # Convertir los resultados a un formato adecuado para la plantilla
        filas = [list(resultado) for resultado in resultados]

        # Mostrar los resultados en la plantilla
        return render_template('consultas.html', tipo=tipo.capitalize(), filas=filas)

    except Exception as e:
        return f"Error al realizar la consulta: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)