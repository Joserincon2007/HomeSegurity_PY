from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from conexion import get_connection

citas = Blueprint("citas", __name__, url_prefix="/citas")


# =====================================
# CREAR CITA
# =====================================
@citas.route("/crear/<int:id_vivienda>", methods=["GET", "POST"])
def crear_cita(id_vivienda):

    # 🔐 verificar login
    if "idUsuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # obtener vivienda
    cursor.execute(
        "SELECT * FROM vivienda WHERE id_vivienda=%s",
        (id_vivienda,)
    )
    vivienda = cursor.fetchone()

    # ===== GUARDAR =====
    if request.method == "POST":

        fecha = request.form["fecha"]
        hora = request.form["hora"]
        usuario = session["idUsuario"]

        cursor.execute("""
            INSERT INTO citas
            (vivienda_id, id_usuario_fk, fecha, hora, estado)
            VALUES (%s,%s,%s,%s,'PENDIENTE')
        """, (id_vivienda, usuario, fecha, hora))

        conn.commit()

        flash("✅ Cita agendada correctamente")

        cursor.close()
        conn.close()

        return redirect(url_for("citas.mis_citas"))

    cursor.close()
    conn.close()

    return render_template("citas/crear.html", vivienda=vivienda)


# =====================================
# MIS CITAS
# =====================================
@citas.route("/mis-citas")
def mis_citas():

    if "idUsuario" not in session:
        return redirect(url_for("auth.login"))

    usuario = session["idUsuario"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id,
               v.direccion,
               v.ciudad,
               c.fecha,
               c.hora,
               c.estado
        FROM citas c
        JOIN vivienda v ON v.id_vivienda = c.vivienda_id
        WHERE c.id_usuario_fk=%s
        ORDER BY c.fecha DESC
    """, (usuario,))

    citas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("citas/listar.html", citas=citas)


# =====================================
# ELIMINAR CITA
# =====================================
@citas.route("/eliminar/<int:id>")
def eliminar_cita(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM citas WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("citas.mis_citas"))