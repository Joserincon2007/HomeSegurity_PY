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
        data = request.form.to_dict()
        logging.info(f"FORM DATA: {data}")

        nombre = data.get('primerNombre')
        apellido = data.get('primerApellido')
        documento = data.get('num_documento')
        correo = data.get('correo')
        telefono = data.get('telefono')
        edad = data.get('edad')
        direccion = data.get('direccion')
        password = data.get('contrasena')
        estadoCuenta = data.get('estadoCuenta', 'ACTIVO')

        if not nombre or not correo or not password:
            return render_template(TEMPLATE, message="Faltan datos")

        cur = mysql.connection.cursor()

        cur.execute("SELECT idUsuario FROM usuario WHERE correo=%s", (correo,))
        if cur.fetchone():
            cur.close()
            return render_template(TEMPLATE, message="Correo ya existe")

        sql = """
        INSERT INTO usuario
        (primerNombre, primerApellido, contraseña, edad,
         direccion, num_documento, correo, telefono, estadoCuenta, rol)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'USER')
        """

        cur.execute(sql, (
            nombre,
            apellido,
            generate_password_hash(password),
            edad,
            direccion,
            documento,
            correo,
            telefono,
            estadoCuenta
        ))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('auth.login'))

    except Exception as e:
        logging.exception("ERROR REGISTRO")
        return f"ERROR: {str(e)}"

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