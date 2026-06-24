from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from extensions import mail
from conexion import get_connection

dashboard_citas = Blueprint(
    "dashboard_citas",
    __name__,
    url_prefix="/dashboard-citas"
)

# =====================================
# DASHBOARD
# =====================================
@dashboard_citas.route("/")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id,
               c.fecha,
               c.hora,
               c.estado,
               c.recomendaciones,
               v.direccion,
               u.primerNombre,
               u.correo
        FROM citas c
        JOIN vivienda v ON v.id_vivienda = c.vivienda_id
        JOIN usuario u ON u.idUsuario = c.id_usuario_fk
        ORDER BY c.fecha DESC
    """)

    citas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard/dashboard-citas.html",
        citas=citas
    )


# =====================================
# ACTUALIZAR CITA + CORREO
# =====================================
@dashboard_citas.route("/actualizar/<int:id>", methods=["POST"])
def actualizar_cita(id):

    estado = request.form["estado"]
    recomendaciones = request.form["recomendaciones"]
    correo = request.form["correo"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE citas
        SET estado=%s,
            recomendaciones=%s
        WHERE id=%s
    """, (estado, recomendaciones, id))

    conn.commit()

    cursor.close()
    conn.close()

    # ===== ENVIAR CORREO =====
    try:
        msg = Message(
            subject="Actualización de tu cita - Home Security",
            recipients=[correo]
        )

        msg.body = f"""
Hola 👋

Tu cita ha sido actualizada.

Estado: {estado}

Recomendaciones del agente:
{recomendaciones}

Gracias por confiar en Home Security.
        """

        mail.send(msg)

    except Exception as e:
        print("❌ Error enviando correo:", e)

    flash("✅ Cita actualizada y notificada por correo", "success")

    return redirect(url_for("dashboard_citas.dashboard"))