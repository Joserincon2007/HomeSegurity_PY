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
from conexion import get_connection



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

        # 🔄 USAMOS LA CONEXIÓN CORRECTA HACIA RAILWAY
        conn = get_connection()
        cur = conn.cursor()

        # 🚀 AGREGAMOS 'rol' EN LA CONSULTA (Requerido para activar tu TRIGGER de Cliente)
        sql = """
        INSERT INTO usuario
        (primerNombre, primerApellido, contraseña, edad,
         direccion, num_documento, correo, telefono, estadoCuenta, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVO', 'USER')
        """

        cur.execute(sql, (
            nombre, apellido, password, edad,
            direccion, documento, correo, telefono
        ))

        # Guardamos los cambios en Railway
        conn.commit()

        # Obtener el ID recién insertado
        usuario_id = cur.lastrowid
        cur.close()
        conn.close()

        # 🔥 Guardar sesión
        session['idUsuario'] = usuario_id
        session['usuario'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo
        session['rol'] = "USER"

        # Redirigir al login o directo al home si ya inició sesión
        return redirect(url_for('auth.login'))

    except Exception as e:
        print("ERROR REGISTRO REALWAY:", e)
        return render_template(
            'agregarUsuarios.html',
            message=f"Error al registrar: {str(e)}"
        )

# ==============================
# LOGIN
# ==============================
@auth.route('/login', methods=['POST', 'GET'])
def login():
    # 👉 SOLO mostrar login
    if request.method == "GET":
        return render_template("index.html")

    # 👉 VALIDAR LOGIN
    correo = request.form.get('nombre_usuario')
    password = request.form.get('contrasena')

    # 🔄 Usamos la conexión correcta a Railway
    conn = get_connection()
    cur = conn.cursor()

    # Buscamos SOLO por correo para traer los datos del usuario de forma segura
    cur.execute("""
        SELECT idUsuario, primerNombre, primerApellido, correo, rol, contraseña
        FROM usuario
        WHERE correo = %s
    """, (correo,))

    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        # Extraemos los datos de la tupla devuelta por MySQL
        id_usuario, nombre, apellido, user_correo, rol, password_db = user

        # 🔐 VALIDACIÓN DE CONTRASEÑA:
        # Opción A (Si usas hashes/encriptación en el registro):
        # es_valido = check_password_hash(password_db, password)
        
        # Opción B (Si estás guardando la clave en texto plano temporalmente):
        es_valido = (password == password_db)

        if es_valido:
            # 🔥 Guardar los datos exactos en la sesión del navegador
            session['idUsuario'] = id_usuario
            session['usuario'] = nombre
            session['apellido'] = apellido
            session['correo'] = user_correo
            session['rol'] = rol

            # 🚀 Redirecciones dinámicas según el rol exacto
            if rol == "ADMIN":
                return redirect(url_for('admin.dashboard'))

            if rol == "AGENTE":
                return redirect(url_for("agente.vivienda"))

            if rol == "PERITO":
                return redirect(url_for("avaluos.dashboard_perito"))

            # Si es 'USER', va al home general
            return redirect(url_for('home_usuario'))

    # Si no entra a ningún if, las credenciales están mal
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
    import sys  # Para capturar el error en journalctl

    try:
        # 1. Capturamos los datos del formulario HTML
        # OJO: Asegúrate de que los 'name' en tu archivo HTML sean exactamente estos
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        cargo = request.form.get('cargo')

        print(f"--> [AUTH] Intentando guardar solicitud: {nombre} {apellido} ({correo})", file=sys.stderr)

        # 2. Conexión e inserción en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO solicitudes_admin
            (nombre, apellido, correo, cargo, estado)
            VALUES (%s, %s, %s, %s, 'PENDIENTE')
        """, (nombre, apellido, correo, cargo))

        mysql.connection.commit()
        cur.close()

        print("--> [AUTH] ¡Solicitud guardada con éxito en la Base de Datos!", file=sys.stderr)
        flash('success_modal')

    except Exception as e:
        # Si algo falla (campo null, error de sintaxis, etc.), lo sabremos aquí de inmediato
        print(f"❌ [AUTH] Error al insertar la solicitud en la BD: {str(e)}", file=sys.stderr)
        flash('error_modal') # O el manejo que prefieras

    return redirect(url_for('auth.solicitar_admin_form'))
