from flask import Blueprint, render_template, request, redirect, url_for, session
from conexion import get_connection
from extensions import mysql
from flask import request, render_template
from werkzeug.utils import secure_filename
from conexion import get_connection
import os

UPLOAD_FOLDER = "static/uploads"

# ==============================
# BLUEPRINT
# ==============================
agente = Blueprint('agente', __name__, url_prefix='/agente')


# ==============================
# LISTAR VIVIENDAS
# ==============================
@agente.route('/vivienda')
def vivienda():

    if session.get("rol") != "AGENTE":
        return redirect(url_for('index'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vivienda ORDER BY id_vivienda DESC")
    viviendas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("vivienda/listar.html", viviendas=viviendas)


# ==============================
# CREAR VIVIENDA (NUEVO MODELO)
# ==============================
@agente.route("/vivienda/crear", methods=["GET", "POST"])
def crear_vivienda():

    if session.get("rol") != "AGENTE":
        return redirect(url_for("index"))

    if request.method == "POST":

        # ===== DATOS PRINCIPALES =====
        ciudad = request.form["ciudad"]
        localidad = request.form["localidad"]
        direccion = request.form["direccion"]
        area_m2 = request.form["area_m2"]
        tipo = request.form["tipo_inmueble"]
        estrato = request.form["estrato"]
        habitaciones = request.form["habitaciones"]
        banos = request.form["banos"]
        parqueaderos = request.form["parqueaderos"]
        antiguedad = request.form["antiguedad"]

        precio = request.form["precio"]
        descripcion = request.form.get("descripcion", "")
        estado = request.form["estado"]

        # ===== FOTO =====
        foto = request.files["foto"]
        nombre_foto = None

        if foto and foto.filename != "":
            nombre_foto = secure_filename(foto.filename)
            foto.save(os.path.join(UPLOAD_FOLDER, nombre_foto))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO vivienda (
                ciudad, localidad, direccion,
                area_m2, tipo_inmueble, estrato,
                habitaciones, banos, parqueaderos, antiguedad,
                precio, descripcion, estado_publicacion, foto
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            ciudad, localidad, direccion,
            area_m2, tipo, estrato,
            habitaciones, banos, parqueaderos, antiguedad,
            precio, descripcion, estado, nombre_foto
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("agente.vivienda"))

    return render_template("vivienda/crear.html")


# ==============================
# CATÁLOGO PÚBLICO
# ==============================
from flask import request
@agente.route("/catalogo")
def catalogo_publico():
    # 1. Capturar los criterios de búsqueda desde la URL
    localidad = request.args.get('localidad')
    tipo = request.args.get('tipo')
    habitaciones = request.args.get('habitaciones')
    precio_max = request.args.get('precio_max')
    area_min = request.args.get('area_min')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 2. Base de la consulta usando la estructura de tu base de datos
    query = "SELECT * FROM vivienda WHERE estado_publicacion='ACTIVO'"
    params = []

    # 3. Agregar filtros dinámicamente si el usuario los llenó
    if localidad:
        query += " AND localidad = %s"
        params.append(localidad)

    if tipo:
        query += " AND tipo_inmueble = %s"
        params.append(tipo)

    if habitaciones:
        query += " AND habitaciones >= %s"
        params.append(habitaciones)

    if precio_max:
        query += " AND precio <= %s"
        params.append(precio_max)

    if area_min:
        query += " AND area_m2 >= %s"
        params.append(area_min)

    # 4. Ordenar por lo más reciente
    query += " ORDER BY id_vivienda DESC"

    # 5. Ejecutar con los parámetros seguros (Corregidos espacios invisibles corruptos)
    cursor.execute(query, params)
    viviendas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes/home.html",
        viviendas=viviendas
    )


# ==============================
# EDITAR VIVIENDA
# ==============================
@agente.route("/vivienda/editar/<int:id>", methods=["GET", "POST"])
def editar_vivienda(id):

    conexion = mysql.connection
    cursor = conexion.cursor()

    if request.method == "POST":

        ciudad = request.form["ciudad"]
        localidad = request.form["localidad"]
        direccion = request.form["direccion"]
        area_m2 = request.form["area_m2"]
        tipo = request.form["tipo_inmueble"]
        estrato = request.form["estrato"]
        habitaciones = request.form["habitaciones"]
        banos = request.form["banos"]
        parqueaderos = request.form["parqueaderos"]
        antiguedad = request.form["antiguedad"]

        precio = request.form["precio"]
        estado = request.form["estado"]
        descripcion = request.form["descripcion"]

        foto = request.files["foto"]

        # ===== CON FOTO NUEVA =====
        if foto and foto.filename != "":
            nombre_foto = secure_filename(foto.filename)
            ruta = os.path.join(UPLOAD_FOLDER, nombre_foto)
            foto.save(ruta)

            cursor.execute("""
                UPDATE vivienda SET
                    ciudad=%s,
                    localidad=%s,
                    direccion=%s,
                    area_m2=%s,
                    tipo_inmueble=%s,
                    estrato=%s,
                    habitaciones=%s,
                    banos=%s,
                    parqueaderos=%s,
                    antiguedad=%s,
                    precio=%s,
                    estado_publicacion=%s,
                    descripcion=%s,
                    foto=%s
                WHERE id_vivienda=%s
            """, (
                ciudad, localidad, direccion,
                area_m2, tipo, estrato,
                habitaciones, banos, parqueaderos, antiguedad,
                precio, estado, descripcion,
                nombre_foto, id
            ))

        # ===== SIN CAMBIAR FOTO =====
        else:
            cursor.execute("""
                UPDATE vivienda SET
                    ciudad=%s,
                    localidad=%s,
                    direccion=%s,
                    area_m2=%s,
                    tipo_inmueble=%s,
                    estrato=%s,
                    habitaciones=%s,
                    banos=%s,
                    parqueaderos=%s,
                    antiguedad=%s,
                    precio=%s,
                    estado_publicacion=%s,
                    descripcion=%s
                WHERE id_vivienda=%s
            """, (
                ciudad, localidad, direccion,
                area_m2, tipo, estrato,
                habitaciones, banos, parqueaderos, antiguedad,
                precio, estado, descripcion, id
            ))

        conexion.commit()
        return redirect(url_for("agente.vivienda"))

    cursor.execute(
        "SELECT * FROM vivienda WHERE id_vivienda=%s",
        (id,)
    )

    vivienda = cursor.fetchone()

    return render_template(
        "vivienda/editar.html",
        vivienda=vivienda
    )


# ==============================
# ELIMINAR VIVIENDA
# ==============================
@agente.route("/vivienda/eliminar/<int:id>")
def eliminar_vivienda(id):
    conexion = mysql.connection
    cursor = conexion.cursor()

    # 1. Borrar primero las citas asociadas para evitar el IntegrityError
    cursor.execute("DELETE FROM citas WHERE vivienda_id = %s", (id,))

    # 2. Obtener la foto para borrarla del servidor (como ya lo tenías)
    cursor.execute("SELECT foto FROM vivienda WHERE id_vivienda = %s", (id,))
    vivienda = cursor.fetchone()

    if vivienda and vivienda[0]:
        ruta_foto = os.path.join(UPLOAD_FOLDER, vivienda[0])
        if os.path.exists(ruta_foto):
            os.remove(ruta_foto)

    # 3. Ahora sí, borrar la vivienda
    cursor.execute("DELETE FROM vivienda WHERE id_vivienda = %s", (id,))

    conexion.commit()
    return redirect(url_for("agente.vivienda"))