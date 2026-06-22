from extensions import mysql
from flask import Blueprint, render_template, session, redirect, url_for
from routes.correo import enviar_correo_credenciales
from flask import request, flash
import random
import string

def generar_password(longitud=10):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    return password

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
def dashboard():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id,nombre,apellido,correo,cargo,fecha,estado
        FROM solicitudes_admin
        ORDER BY fecha DESC
    """)

    solicitudes = cur.fetchall()
    cur.close()

    return render_template(
        "dashboard_admin.html",
        solicitudes=solicitudes
    )

@admin.route('/aprobar/<int:id>')
def aprobar_admin(id):

    password = generar_password()

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT correo,cargo
        FROM solicitudes_admin
        WHERE id=%s
    """,(id,))

    correo,cargo = cur.fetchone()

    cur.execute("""
        UPDATE usuario
        SET rol=%s, contraseña=%s
        WHERE correo=%s
    """,(cargo,password,correo))

    cur.execute("""
        UPDATE solicitudes_admin
        SET estado='APROBADO'
        WHERE id=%s
    """,(id,))

    mysql.connection.commit()
    cur.close()

    enviar_correo_credenciales(correo,password)

    return redirect(url_for('admin.dashboard'))


@admin.route('/rechazar/<int:id>')
def rechazar_admin(id):

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE solicitudes_admin
        SET estado='RECHAZADO'
        WHERE id=%s
    """,(id,))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('admin.dashboard'))


# 1. RUTA PARA MOSTRAR EL FORMULARIO (La página nueva)
# Ruta para mostrar la página del formulario
@admin.route('/cambiar-password', methods=['GET'])
def vista_cambiar_password():
    if 'idUsuario' not in session:
        return redirect(url_for('auth.login'))
    return render_template('clientes/contraseña.html')

# Ruta que recibe los datos del formulario
@admin.route('/procesar-cambio-password', methods=['POST'])
def procesar_cambio_password():
    if 'idUsuario' not in session:
        return redirect(url_for('auth.login'))

    pass_actual = request.form.get('pass_actual')
    pass_nueva = request.form.get('pass_nueva')
    id_usuario = session.get('idUsuario')

    cur = mysql.connection.cursor()
    cur.execute("SELECT contraseña FROM usuario WHERE idUsuario = %s", (id_usuario,))
    resultado = cur.fetchone()

    if resultado and resultado[0] == pass_actual:
        cur.execute("UPDATE usuario SET contraseña = %s WHERE idUsuario = %s", (pass_nueva, id_usuario))
        mysql.connection.commit()
        flash("Contraseña actualizada exitosamente", "success")
        return redirect(url_for('auth.login')) # O a donde desees redirigir
    else:
        flash("La contraseña actual es incorrecta", "danger")
        return redirect(url_for('admin.vista_cambiar_password'))