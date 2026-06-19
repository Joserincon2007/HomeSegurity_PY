from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import mysql, db
from routes.agente import agente
from routes.correo import enviar_correo_credenciales
from models.avaluos import Avaluo
from models.vivienda import Vivienda
import uuid
import random
import string
import re

# 🔥 IMPORTANTE: Herramientas para el manejo seguro de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

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
    TEMPLATE_HTML = 'agregarUsuarios.html' 
    try:
        # 1. Obtención de datos del formulario
        nombre = request.form.get('primerNombre')
        apellido = request.form.get('primerApellido')
        documento = request.form.get('num_documento')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        edad_raw = request.form.get('edad')
        direccion = request.form.get('direccion')
        password = request.form.get('contrasena')

        # 🔥 LÍNEA DE CONTROL: Esto imprimirá en tu consola qué está llegando exactamente
        print(f"DEBUG REGISTRO -> Nombre: {nombre}, Correo: {correo}, Password: {password}")

        edad = int(edad_raw) if edad_raw and edad_raw.isdigit() else None

        # 2. Validación de campos obligatorios
        if not nombre or not correo or not password:
            print("❌ Se detuvo en: Campos obligatorios vacíos")
            return render_template(TEMPLATE_HTML, message="Faltan datos obligatorios")

        # 3. Requisitos mínimos de seguridad
        if len(password) < 8:
            print("❌ Se detuvo en: Contraseña menor a 8 caracteres")
            return render_template(TEMPLATE_HTML, message="La contraseña debe tener al menos 8 caracteres.")
        
        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
            print("❌ Se detuvo en: Falta mayúscula, minúscula o número")
            return render_template(TEMPLATE_HTML, message="La contraseña debe incluir mayúsculas, minúsculas y números.")

        # 4. Encriptar contraseña de manera irreversible
        password_encriptada = generate_password_hash(password)

        # 5. Operación en Base de Datos
        cur = mysql.connection.cursor()

        sql = """
        INSERT INTO usuario
        (primerNombre, primerApellido, contrasena, edad,
         direccion, num_documento, correo, telefono, estadoCuenta)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVO')
        """

        # 🔥 CORREGIDO: El orden de los parámetros coincide perfectamente con el SQL
        cur.execute(sql, (
            nombre, apellido, password_encriptada, edad,
            direccion, documento, correo, telefono
        ))

        mysql.connection.commit()
        usuario_id = cur.lastrowid
        cur.close()

        # 6. Guardar sesión
        session['idUsuario'] = usuario_id
        session['usuario'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo
        session['rol'] = "USER"

        return redirect(url_for('auth.login'))

    except Exception as e:
        print("❌ ERROR REGISTRO:", str(e))
        return render_template(
            'agregarUsuarios.html',
            message="Error al registrar"
        )


# ==============================
# LOGIN
# ==============================
@auth.route('/login', methods=['POST', "GET"])
def login():
    # 👉 SOLO mostrar login
    if request.method == "GET":
        return render_template("index.html")

    # 👉 VALIDAR LOGIN
    correo = request.form.get('nombre_usuario')
    password_ingresada = request.form.get('contrasena')

    cur = mysql.connection.cursor()

    # Buscamos al usuario únicamente por su correo
    cur.execute("""
        SELECT idUsuario, primerNombre, primerApellido, correo, rol, contrasena
        FROM usuario
        WHERE correo=%s
    """, (correo,))

    user = cur.fetchone()
    cur.close()

    # 🔥 VERIFICACIÓN SEGURA: Comparamos el hash de la BD con la clave ingresada
    if user and check_password_hash(user[5], password_ingresada):

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


# ==============================
# VIVIENDAS
# ==============================
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
    return render_template("index.html")


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
        VALUES (%s, %s, %s, %s, 'PENDIENTE')
    """, (nombre, apellido, correo, cargo))

    mysql.connection.commit()
    cur.close()

    flash('success_modal') 
    return redirect(url_for('auth.solicitar_admin_form'))