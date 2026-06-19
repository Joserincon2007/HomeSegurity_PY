from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import mysql
from routes.agente import agente
import uuid
import random
import string
from models.avaluos import Avaluo
from extensions import db
from routes.correo import enviar_correo_credenciales
from models.vivienda import Vivienda


auth = Blueprint('auth', __name__)

# ==============================
# GENERAR PASSWORD
# ==============================
def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# ==============================
# REGISTRO USUARIO
# ==============================
@auth.route('/agregar-usuarios', methods=['POST'])
def agregarUsuarios():

    try:
        nombre = request.form.get('primerNombre')
        apellido = request.form.get('primerApellido')
        documento = request.form.get('num_documento')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        edad = request.form.get('edad')
        direccion = request.form.get('direccion')
        password = request.form.get('contraseña')

        

        if not nombre or not correo or not password:
            return render_template(
                'agregarUsuarios.html',
                message="Faltan datos"
            )

        cur = mysql.connection.cursor()

        sql = """
        INSERT INTO usuario
        (primerNombre, primerApellido, contraseña, edad,
         direccion, num_documento, correo, telefono, estadoCuenta)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'ACTIVO')
        """

        cur.execute(sql, (
            nombre, apellido, password, edad,
            direccion, documento, correo, telefono
        ))

        mysql.connection.commit()

        # obtener id insertado
        usuario_id = cur.lastrowid
        cur.close()

        # 🔥 guardar sesión
        session['idUsuario'] = usuario_id
        session['usuario'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo
        session['rol'] = "USER"

        return redirect(url_for('auth.login'))

    except Exception as e:
        print("ERROR REGISTRO:", e)
        return render_template(
            'agregarUsuarios.html',
            message="Error al registrar"
        )


# ==============================
# LOGIN
# ==============================
@auth.route('/login', methods=['POST',"GET"])
def login():

    # 👉 SOLO mostrar login
    if request.method == "GET":
        return render_template("index.html")

    # 👉 VALIDAR LOGIN
    correo = request.form.get('nombre_usuario')
    password = request.form.get('contrasena')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT idUsuario, primerNombre,
               primerApellido, correo, rol
        FROM usuario
        WHERE correo=%s AND contraseña=%s
    """, (correo, password))

    user = cur.fetchone()
    cur.close()

    if user:

        session['idUsuario'] = user[0]
        session['usuario'] = user[1]
        session['apellido'] = user[2]
        session['correo'] = user[3]
        session['rol'] = user[4]

        if user[4] == "ADMIN":
            return redirect(url_for('admin.dashboard'))

        if user[4] == "AGENTE":
            return redirect(url_for("agente.vivienda"))
        
        if user[4] == "PERITO":
            return redirect(url_for("avaluos.dashboard_perito"))

        return redirect(url_for('home_usuario'))

    return render_template(
        "index.html",
        message="Credenciales incorrectas"
    )


@auth.route("/viviendas")
def ver_vivienda():

    viviendas = Vivienda.query.filter_by(
        estado_publicacion="ACTIVO"
    ).all()

    return render_template(
        "clientes/home.html",
        viviendas=viviendas
    )



# ==============================
# SOLICITAR ADMIN
# ==============================

@auth.route('/solicitar-admin-form')
def solicitar_admin_form():
    if "usuario" in session:
        return render_template("clientes/solicitud-credenciales.html")
    return render_template("index")


@auth.route('/solicitar_admin', methods=['POST'])
def solicitar_admin():

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    cargo = request.form['cargo']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO solicitudes_admin
        (nombre, apellido, correo, cargo, estado)
        VALUES (%s,%s,%s,%s,'PENDIENTE')
    """,(nombre,apellido,correo,cargo))

    mysql.connection.commit()
    cur.close()

    flash('success_modal') 
    return redirect(url_for('auth.solicitar_admin_form'))



