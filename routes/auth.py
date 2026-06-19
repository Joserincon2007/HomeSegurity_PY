# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import mysql
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import re
import random
import string

auth = Blueprint('auth', __name__)

# ==========================
# LOGS (IMPORTANTE VPS)
# ==========================
logging.basicConfig(level=logging.INFO)


# ==========================
# GENERAR PASSWORD
# ==========================
def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# ==========================
# REGISTRAR USUARIO
# ==========================
@auth.route('/agregar-usuarios', methods=['POST'])
def agregarUsuarios():

    TEMPLATE = "agregarUsuarios.html"

    try:
        # 🔍 VER TODO LO QUE LLEGA
        data = request.form.to_dict()
        logging.info(f"FORM DATA: {data}")

        # ==========================
        # CAPTURA DE DATOS
        # ==========================
        nombre = request.form.get('primerNombre')
        apellido = request.form.get('primerApellido')
        documento = request.form.get('num_documento')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        edad = request.form.get('edad')
        direccion = request.form.get('direccion')
        password = request.form.get('contrasena')
        estadoCuenta = request.form.get('estadoCuenta', 'ACTIVO')

        # ==========================
        # VALIDACIÓN BÁSICA
        # ==========================
        if not nombre or not correo or not password:
            return render_template(TEMPLATE, message="Faltan datos obligatorios")

        # ==========================
        # VALIDACIÓN PASSWORD
        # ==========================
        if len(password) < 8:
            return render_template(TEMPLATE, message="Mínimo 8 caracteres")

        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
            return render_template(TEMPLATE, message="Debe incluir mayúscula, minúscula y número")

        # ==========================
        # HASH PASSWORD
        # ==========================
        password_hash = generate_password_hash(password)

        # ==========================
        # CONEXIÓN MYSQL
        # ==========================
        cur = mysql.connection.cursor()

        # 🔴 VERIFICAR SI CORREO EXISTE
        cur.execute("SELECT idUsuario FROM usuario WHERE correo=%s", (correo,))
        existe = cur.fetchone()

        if existe:
            return render_template(TEMPLATE, message="El correo ya está registrado")

        # ==========================
        # INSERT USUARIO
        # ==========================
        sql = """
        INSERT INTO usuario
        (primerNombre, primerApellido, contraseña, edad,
         direccion, num_documento, correo, telefono, estadoCuenta, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'USER')
        """

        cur.execute(sql, (
            nombre,
            apellido,
            password_hash,
            edad,
            direccion,
            documento,
            correo,
            telefono,
            estadoCuenta
        ))

        mysql.connection.commit()
        usuario_id = cur.lastrowid
        cur.close()

        logging.info(f"Usuario creado ID: {usuario_id}")

        # ==========================
        # SESIÓN
        # ==========================
        session['idUsuario'] = usuario_id
        session['usuario'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo
        session['rol'] = "USER"

        return redirect(url_for('auth.login'))

    except Exception as e:
        logging.exception("ERROR EN REGISTRO")

        return render_template(
            TEMPLATE,
            message=f"Error del servidor: {str(e)}"
        )


# ==========================
# LOGIN
# ==========================
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        return render_template("index.html")

    correo = request.form.get('nombre_usuario')
    password = request.form.get('contrasena')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT idUsuario, primerNombre, primerApellido, correo, rol, contraseña
        FROM usuario
        WHERE correo=%s
    """, (correo,))

    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[5], password):

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

    return render_template("index.html", message="Credenciales incorrectas")