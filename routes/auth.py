# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import mysql
from routes.correo import enviar_correo_credenciales
from models.vivienda import Vivienda

import random
import string
import re
import logging

from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# ==============================
# CONFIG LOGGING (IMPORTANTE VPS)
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
        # DEBUG: ver todo lo que llega del formulario
        logging.info(f"FORM DATA: {request.form}")

        # 1. Datos del formulario
        nombre = request.form.get('primerNombre')
        apellido = request.form.get('primerApellido')
        documento = request.form.get('num_documento')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        edad_raw = request.form.get('edad')
        direccion = request.form.get('direccion')
        password = request.form.get('contrasena')

        edad = int(edad_raw) if edad_raw and edad_raw.isdigit() else None

        # 2. Validación básica
        if not nombre or not correo or not password:
            logging.warning("Faltan campos obligatorios")
            return render_template(TEMPLATE_HTML, message="Faltan datos obligatorios")

        # 3. Seguridad contraseña
        if len(password) < 8:
            return render_template(TEMPLATE_HTML, message="Mínimo 8 caracteres")

        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
            return render_template(TEMPLATE_HTML, message="Debe incluir mayúscula, minúscula y número")

        # 4. Hash password
        password_encriptada = generate_password_hash(password)

        # 5. Insert DB
        cur = mysql.connection.cursor()

        sql = """
        INSERT INTO usuario
        (primerNombre, primerApellido, contraseña, edad,
         direccion, num_documento, correo, telefono, estadoCuenta, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVO', 'USER')
        """

        cur.execute(sql, (
            nombre,
            apellido,
            password_encriptada,
            edad,
            direccion,
            documento,
            correo,
            telefono
        ))

        mysql.connection.commit()
        usuario_id = cur.lastrowid
        cur.close()

        logging.info(f"Usuario creado ID: {usuario_id}")

        # 6. Session
        session['idUsuario'] = usuario_id
        session['usuario'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo
        session['rol'] = "USER"

        return redirect(url_for('auth.login'))

    except Exception as e:
        logging.exception("ERROR EN REGISTRO USUARIO")
        return render_template(TEMPLATE_HTML, message=str(e))


# ==============================
# LOGIN
# ==============================
@auth.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "GET":
        return render_template("index.html")

    correo = request.form.get('nombre_usuario')
    password_ingresada = request.form.get('contrasena')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT idUsuario, primerNombre, primerApellido, correo, rol, contraseña
        FROM usuario
        WHERE correo=%s
    """, (correo,))

    user = cur.fetchone()
    cur.close()

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

    return render_template("index.html", message="Credenciales incorrectas")


# ==============================
# VIVIENDAS
# ==============================
@auth.route("/viviendas")
def ver_vivienda():
    viviendas = Vivienda.query.filter_by(estado_publicacion="ACTIVO").all()

    return render_template("clientes/home.html", viviendas=viviendas)