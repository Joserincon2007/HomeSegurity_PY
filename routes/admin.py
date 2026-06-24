<<<<<<< HEAD
from extensions import mysql
from flask import Blueprint, render_template, session, redirect, url_for
from routes.correo import enviar_correo_credenciales
from flask import request, flash
=======
import sys
from extensions import mysql
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from routes.correo import enviar_correo_credenciales
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
import random
import string

def generar_password(longitud=10):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    return password

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
def dashboard():
<<<<<<< HEAD

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT id,nombre,apellido,correo,cargo,fecha,estado
        FROM solicitudes_admin
        ORDER BY fecha DESC
    """)

=======
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, nombre, apellido, correo, cargo, fecha, estado
        FROM solicitudes_admin
        ORDER BY fecha DESC
    """)
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
    solicitudes = cur.fetchall()
    cur.close()

    return render_template(
        "dashboard_admin.html",
        solicitudes=solicitudes
    )

@admin.route('/aprobar/<int:id>')
def aprobar_admin(id):
<<<<<<< HEAD

    password = generar_password()

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT correo,cargo
        FROM solicitudes_admin
        WHERE id=%s
    """,(id,))

    correo,cargo = cur.fetchone()

=======
    import sys
    password = generar_password()
    cur = mysql.connection.cursor()

    # 1. Obtener los datos de la solicitud pendiente
    cur.execute("""
        SELECT correo, cargo 
        FROM solicitudes_admin 
        WHERE id=%s
    """, (id,))
    resultado = cur.fetchone()

    if not resultado:
        cur.close()
        print(f"❌ Error: No se encontró la solicitud con ID {id}", file=sys.stderr)
        return redirect(url_for('admin.dashboard'))

    correo, cargo = resultado

    # 2. Verificar si el usuario existe en la tabla de credenciales principales
    cur.execute("SELECT idUsuario FROM usuario WHERE correo=%s", (correo,))
    existe_usuario = cur.fetchone()

    if not existe_usuario:
        # Optativo: Si no existe, podrías decidir INSERTARLO en lugar de hacer UPDATE.
        # Por ahora lo controlamos con un log o un flash de advertencia.
        print(f"⚠️ Alerta: El correo {correo} no está registrado en la tabla 'usuario'.", file=sys.stderr)

    # 3. Actualizar rol y contraseña en la tabla 'usuario'
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
    cur.execute("""
        UPDATE usuario
        SET rol=%s, contraseña=%s
        WHERE correo=%s
<<<<<<< HEAD
    """,(cargo,password,correo))

=======
    """, (cargo, password, correo))

    # 4. Cambiar el estado en el filtro de solicitudes
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
    cur.execute("""
        UPDATE solicitudes_admin
        SET estado='APROBADO'
        WHERE id=%s
<<<<<<< HEAD
    """,(id,))
=======
    """, (id,))
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed

    mysql.connection.commit()
    cur.close()

<<<<<<< HEAD
    enviar_correo_credenciales(correo,password)
=======
    # 5. Despachar las credenciales al correo del solicitante de forma segura
    print(f"--> [ADMIN] Solicitud {id} aprobada en BD. Despachando correo a {correo}...", file=sys.stderr)
    
    try:
        enviar_correo_credenciales(correo, password)
    except Exception as e:
        print(f"❌ Error crítico al enviar el correo tras la aprobación: {e}", file=sys.stderr)
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed

    return redirect(url_for('admin.dashboard'))


@admin.route('/rechazar/<int:id>')
def rechazar_admin(id):
<<<<<<< HEAD

    cur = mysql.connection.cursor()

=======
    cur = mysql.connection.cursor()
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
    cur.execute("""
        UPDATE solicitudes_admin
        SET estado='RECHAZADO'
        WHERE id=%s
<<<<<<< HEAD
    """,(id,))

=======
    """, (id,))
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('admin.dashboard'))


<<<<<<< HEAD
# 1. RUTA PARA MOSTRAR EL FORMULARIO (La página nueva)
# Ruta para mostrar la página del formulario
=======
# ==============================
# CAMBIAR CONTRASEÑA
# ==============================
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
@admin.route('/cambiar-password', methods=['GET'])
def vista_cambiar_password():
    if 'idUsuario' not in session:
        return redirect(url_for('auth.login'))
    return render_template('clientes/contraseña.html')

<<<<<<< HEAD
# Ruta que recibe los datos del formulario
=======
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
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
<<<<<<< HEAD
        return redirect(url_for('auth.login')) # O a donde desees redirigir
    else:
        flash("La contraseña actual es incorrecta", "danger")
        return redirect(url_for('admin.vista_cambiar_password'))
=======
        return redirect(url_for('auth.login'))
    else:
        flash("La contraseña actual es incorrecta", "danger")
        return redirect(url_for('admin.vista_cambiar_password'))
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
