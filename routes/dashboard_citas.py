import sys
import os
import requests  # 🚀 Cambiamos SMTP por peticiones HTTP v3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from conexion import get_connection

dashboard_citas = Blueprint(
    "dashboard_citas",
    __name__,
    url_prefix="/dashboard-citas"
)

# ==============================================================================
# FUNCIÓN AUXILIAR DE NOTIFICACIÓN VÍA API HTTP (Puerto 443)
# ==============================================================================
def notificar_cambio_cita_api(receptor, estado_cita, recomendaciones_cita):
    """
    Envía una notificación web segura evitando el bloqueo SMTP de DigitalOcean.
    """
    api_key = os.environ.get('BREVO_API_KEY')
    remitente = os.environ.get('MAIL_DEFAULT_SENDER', 'joserinconxc2008@gmail.com')

    if not api_key:
        print("❌ Error: Variable BREVO_API_KEY ausente en el entorno.", file=sys.stderr)
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }

    cuerpo_texto = f"""
Hola 👋

Tu cita ha sido actualizada en nuestro sistema.

📌 Estado actual: {estado_cita}

💬 Recomendaciones del agente:
{recomendaciones_cita}

Gracias por confiar en Home Security.
    """

    payload = {
        "sender": {"email": remitente, "name": "Home Security"},
        "to": [{"email": receptor.strip()}],
        "subject": "⚠️ Actualización de tu cita - Home Security",
        "textContent": cuerpo_texto
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201, 202]:
            print(f"✅ Correo de cita enviado correctamente vía API a {receptor}", file=sys.stderr)
            return True
        else:
            print(f"❌ Brevo rechazó la notificación ({response.status_code}): {response.text}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"❌ Error de red en la API de Brevo al gestionar cita: {str(e)}", file=sys.stderr)
        return False


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
# ACTUALIZAR CITA + CORREO VIA API
# =====================================
@dashboard_citas.route("/actualizar/<int:id>", methods=["POST"])
def actualizar_cita(id):
    estado = request.form["estado"]
    recomendaciones = request.form["recomendaciones"]
    correo = request.form["correo"]

    # 1. Persistencia de la actualización en base de datos (Railway)
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

    # 2. Despacho inmediato mediante API HTTP (Inmune a firewalls)
    print(f"--> [CITAS] Procesando actualización de cita {id}. Notificando a {correo}...", file=sys.stderr)
    notificar_cambio_cita_api(correo, estado, recomendaciones)

    flash("✅ Cita actualizada y notificada por correo", "success")
    return redirect(url_for("dashboard_citas.dashboard"))
