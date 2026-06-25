import sys
import os
import base64
import requests
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, session
from models.avaluos import Avaluo
from models.vivienda import Vivienda
from utils.precios_bogota import calcular_avaluo
from utils.generador_pdf import generar_pdf
from models.usuarios import Usuario 
from models.perito import Perito
from extensions import db
from datetime import datetime

avaluos = Blueprint("avaluos", __name__, url_prefix="/avaluos")

# ==============================================================================
# DECORADOR DE PROTECCIÓN DE ROL: EXCLUSIVO PERITOS
# ==============================================================================
def perito_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'idUsuario' not in session:
            flash("Por favor, inicia sesión para acceder.", "warning")
            return redirect(url_for('auth.login'))
        if session.get("rol") != "PERITO":
            flash("Acceso denegado. Esta sección es exclusiva para Peritos Técnicos.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# FUNCIÓN INTERNA AUXILIAR: ENVIAR CORREO MEDIANTE API BREVO
# ==============================================================================
def enviar_correo_api_brevo(receptor, asunto, cuerpo, adjunto_bytes=None, nombre_adjunto="documento.pdf"):
    api_key = os.environ.get('BREVO_API_KEY')
    remitente = os.environ.get('MAIL_DEFAULT_SENDER', 'joserinconxc2008@gmail.com')

    if not api_key:
        print("❌ Error: No se detectó BREVO_API_KEY en el entorno.", file=sys.stderr)
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }

    payload = {
        "sender": {"email": remitente, "name": "Home Security"},
        "to": [{"email": receptor.strip()}],
        "subject": asunto,
        "textContent": cuerpo
    }

    if adjunto_bytes:
        encoded_content = base64.b64encode(adjunto_bytes).decode('utf-8')
        payload["attachment"] = [{"content": encoded_content, "name": nombre_adjunto}]

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        return response.status_code in [200, 201, 202]
    except Exception as e:
        print(f"❌ Error de red conectando a la API de Brevo: {str(e)}", file=sys.stderr)
        return False


# ==============================================================================
# 1. VISTAS PARA EL CLIENTE (SOLICITANTE)
# ==============================================================================
@avaluos.route("/crear/<int:vivienda_id>", methods=["GET"])
def crear(vivienda_id):
    if 'idUsuario' not in session:
        flash("Debes iniciar sesión para solicitar un avalúo.", "warning")
        return redirect(url_for('auth.login'))

    vivienda = Vivienda.query.get_or_404(vivienda_id)
    precio_m2, precio_total, descripcion = calcular_avaluo(
        vivienda.area_m2, vivienda.localidad, vivienda.estrato, vivienda.antiguedad, vivienda.parqueaderos
    )

    return render_template(
        "avaluos/crear.html",
        vivienda=vivienda, precio=precio_total, precio_m2=precio_m2, descripcion=descripcion
    )


@avaluos.route("/preview_pdf/<int:vivienda_id>")
def preview_pdf(vivienda_id):
    vivienda = Vivienda.query.get_or_404(vivienda_id)
    precio_m2, precio_total, descripcion = calcular_avaluo(
        vivienda.area_m2, vivienda.localidad, vivienda.estrato, vivienda.antiguedad, vivienda.parqueaderos
    )
    
    temp_avaluo = Avaluo(
        id_vivienda=vivienda.id_vivienda,
        solicitante=f"{session.get('usuario', '')} {session.get('apellido', '')}",
        correo=session.get('correo', ''),
        precio_m2=precio_m2, valor_total=precio_total, area_m2=vivienda.area_m2,
        localidad=vivienda.localidad, antiguedad=vivienda.antiguedad, estrato=vivienda.estrato,
        parqueadero=vivienda.parqueaderos, descripcion=descripcion, fecha=datetime.now()
    )
    
    pdf = generar_pdf(temp_avaluo, vivienda)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=previsualizacion_avaluo.pdf'
    return response


@avaluos.route("/procesar", methods=["POST"])
def procesar_avaluo():
    if 'idUsuario' not in session:
        flash("Sesión expirada. Por favor, ingresa a tu cuenta.", "danger")
        return redirect(url_for('auth.login'))

    vivienda_id = request.form.get("vivienda_id")
    correo_cliente = request.form.get("correo") or session.get('correo')
    id_usuario_logueado = session.get('idUsuario')
    nombre_completo = f"{session.get('usuario')} {session.get('apellido')}".strip()

    vivienda = Vivienda.query.get_or_404(vivienda_id)
    precio_m2, precio_total, descripcion = calcular_avaluo(
        vivienda.area_m2, vivienda.localidad, vivienda.estrato, vivienda.antiguedad, vivienda.parqueaderos
    )

    try:
        nuevo_avaluo = Avaluo(
            id_vivienda=vivienda.id_vivienda, solicitante=nombre_completo, correo=correo_cliente,
            area_m2=vivienda.area_m2, localidad=vivienda.localidad, precio_m2=precio_m2,
            valor_total=precio_total, antiguedad=vivienda.antiguedad, estrato=vivienda.estrato,
            parqueadero=vivienda.parqueaderos, descripcion=descripcion, id_usuario=id_usuario_logueado,
            fecha=datetime.now(), estado='Pendiente'  # Inicializado explícitamente en Pendiente
        )

        db.session.add(nuevo_avaluo)
        db.session.commit()

        pdf_final = generar_pdf(nuevo_avaluo, vivienda)
        enviar_correo_api_brevo(
            receptor=correo_cliente,
            subject="Tu Avalúo Técnico - Home Security",
            cuerpo=f"Hola {nombre_completo}, adjuntamos el informe del avalúo técnico preliminar de tu propiedad.",
            adjunto_bytes=pdf_final,
            nombre_adjunto=f"Avaluo_{vivienda.localidad}.pdf"
        )

        flash("Avalúo generado y enviado a tu correo correctamente.", "success")
        return redirect(url_for('avaluos.listar'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar: {str(e)}", "danger")
        return redirect(request.referrer)


@avaluos.route("/listar")
def listar():
    if 'idUsuario' not in session:
        flash("Por favor, inicia sesión para ver tus avalúos.", "warning")
        return redirect(url_for('auth.login'))
        
    id_usuario_logueado = session.get('idUsuario')

    avaluos_list = (
        db.session.query(Avaluo, Vivienda)
        .join(Vivienda, Vivienda.id_vivienda == Avaluo.id_vivienda)
        .filter(Avaluo.id_usuario == id_usuario_logueado)
        .order_by(Avaluo.fecha.desc())
        .all()
    )
    return render_template("avaluos/listar.html", avaluos=avaluos_list)


# ==============================================================================
# 2. VISTAS DE GESTIÓN (EXCLUSIVAS PARA EL PERITO)
# ==============================================================================
@avaluos.route("/dashboard_perito")
@perito_required
def dashboard_perito():
    avaluos_con_vivienda = db.session.query(Avaluo, Vivienda).join(
        Vivienda, Avaluo.id_vivienda == Vivienda.id_vivienda
    ).all()
    return render_template("dashboard/dashboard_perito.html", avaluos=avaluos_con_vivienda)


@avaluos.route("/confirmar_cita/<int:id_avaluo>", methods=["POST"])
@perito_required
def confirmar_cita(id_avaluo):
    avaluo = Avaluo.query.get_or_404(id_avaluo)
    vivienda = Vivienda.query.get(avaluo.id_vivienda)
    
    fecha_cita = request.form.get("fecha_cita")
    hora_cita = request.form.get("hora_cita")
    id_perito_raw = request.form.get("id_perito")
    
    correo_destino = str(avaluo.correo).strip()
    nombre_cliente = str(avaluo.solicitante).strip()

    # Validación básica en backend
    if not fecha_cita or not hora_cita or not id_perito_raw:
        flash("Faltan campos obligatorios para agendar la cita (Fecha, Hora o Perito).", "danger")
        return redirect(url_for('avaluos.dashboard_perito'))

    try:
        # CRÍTICO: Convertir el id_perito a entero para que MySQL no rechace la llave foránea
        id_perito_int = int(id_perito_raw)
        
        # 1. Actualizamos los campos en el objeto de la base de datos
        avaluo.id_perito = id_perito_int
        avaluo.fecha_cita = fecha_cita
        avaluo.hora_cita = hora_cita
        avaluo.estado = 'Agendado'  # <-- Cambiamos el estado de manera explícita
        
        # 2. Confirmar primero los cambios en la Base de Datos
        db.session.commit()

        # 3. Intentar enviar el correo DESPUÉS de guardar con éxito en la DB
        try:
            pdf_adjunto = generar_pdf(avaluo, vivienda)
            cuerpo_correo = (
                f"Hola {nombre_cliente},\n\n"
                f"Su cita para la inspección física de su inmueble ha sido agendada con éxito.\n\n"
                f"Detalles de la visita:\n"
                f"📅 Fecha: {fecha_cita}\n"
                f"⏰ Hora: {hora_cita}\n\n"
                f"Por favor, recuerde contar con los documentos originales de la propiedad a la mano."
            )

            enviar_correo_api_brevo(
                receptor=correo_destino,
                asunto="CONFIRMACIÓN: Cita de Inspección y Requisitos - Home Security",
                cuerpo=cuerpo_correo,
                adjunto_bytes=pdf_adjunto,
                nombre_adjunto="Inspeccion_Agendada.pdf"
            )
            flash(f"Cita agendada para el {fecha_cita} a las {hora_cita}. Notificación enviada a {correo_destino}.", "success")
            
        except Exception as e_mail:
            # Si el correo falla, al menos el estado ya cambió en la base de datos
            print(f"⚠️ Alerta: El avalúo se guardó pero el correo falló: {str(e_mail)}")
            flash(f"Cita agendada en el sistema, pero no se pudo enviar el correo de notificación.", "warning")

    except Exception as e:
        db.session.rollback()
        # IMPRESCINDIBLE: Imprimir el error exacto en tu consola de Railway o terminal de Python
        print(f"❌ ERROR CRÍTICO EN CONFIRMAR_CITA: {str(e)}")
        flash(f"Error al procesar la confirmación en la base de datos: {str(e)}", "danger")

    return redirect(url_for('avaluos.dashboard_perito'))


@avaluos.route("/sincronizar_peritos")
@perito_required
def sincronizar_peritos():
    try:
        # 1. Traer todos los usuarios cuyo rol sea 'PERITO'
        usuarios_peritos = Usuario.query.filter_by(rol='PERITO').all()
        contador = 0
        
        for u in usuarios_peritos:
            # 2. Validar usando 'idUsuario' (tal como está en tu DB) si ya existe en perito
            existe = Perito.query.filter_by(idUsuario=u.idUsuario).first()
            
            if not existe:
                # 3. Crear el registro mapeando los datos dinámicamente
                nuevo_perito = Perito(
                    idUsuario=u.idUsuario,
                    primerNombre=u.usuario,       # Ajusta según el campo exacto de tu modelo Usuario (ej: u.primer_nombre o u.usuario)
                    primerApellido=u.apellido,    # Ajusta según tu campo exacto en Usuario
                    correo=u.correo,
                    edad=None                     # Lo dejamos NULL para que lo editen después o lo calcules si tienes fecha_nacimiento
                )
                db.session.add(nuevo_perito)
                contador += 1
                
        db.session.commit()
        flash(f"Sincronización terminada con éxito. {contador} peritos añadidos.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al sincronizar de forma automática: {str(e)}", "danger")
        
    return redirect(url_for('avaluos.dashboard_perito'))


@avaluos.route("/perito/crear_manual", methods=["GET", "POST"])
@perito_required
def crear_manual():
    if request.method == "POST":
        try:
            nuevo_avaluo = Avaluo(
                id_vivienda=int(request.form.get("id_vivienda")),
                id_usuario=int(request.form.get("id_usuario")),
                id_perito=int(request.form.get("id_perito")) if request.form.get("id_perito") else None, 
                area_m2=float(request.form.get("area_m2")),
                localidad=request.form.get("localidad"),
                precio_m2=float(request.form.get("precio_m2")),
                valor_total=float(request.form.get("valor_total")),
                antiguedad=request.form.get("antiguedad"),
                estrato=request.form.get("estrato"),
                parqueadero=request.form.get("parqueaderos"),
                descripcion=request.form.get("descripcion"),
                solicitante=request.form.get("solicitante"),
                correo=request.form.get("correo"),
                estado=request.form.get("estado") or 'Pendiente'
            )
            db.session.add(nuevo_avaluo)
            db.session.commit()
            flash("Avalúo registrado manualmente.", "success")
            return redirect(url_for('avaluos.listar_perito'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")
            
    usuarios = Usuario.query.all()
    perito_db = Perito.query.all()
    return render_template("avaluos/perito/crear_manual.html", peritos=perito_db, usuarios=usuarios)


@avaluos.route("/perito/mis_avaluos")
@perito_required
def listar_perito():
    id_usuario_logueado = session.get('idUsuario')
    perito = Perito.query.filter_by(idUsuario=id_usuario_logueado).first()
    
    if perito:
        lista_avaluos = (
            db.session.query(Avaluo, Vivienda)
            .join(Vivienda, Vivienda.id_vivienda == Avaluo.id_vivienda)
            .filter(Avaluo.id_perito == perito.id_perito)
            .order_by(Avaluo.fecha.desc())
            .all()
        )
    else:
        lista_avaluos = []
    return render_template("avaluos/perito/listarPerito.html", avaluos=lista_avaluos, perito=perito)


@avaluos.route("/perito/editar/<int:id>", methods=["GET", "POST"])
@perito_required
def editar_avaluo(id):
    avaluo = Avaluo.query.get_or_404(id)
    if request.method == "POST":
        avaluo.solicitante = request.form.get("solicitante")
        avaluo.descripcion = request.form.get("descripcion")
        
        # Mapeamos el nuevo campo valor_final ingresado por el perito
        if request.form.get("valor_final"):
            avaluo.valor_final = float(request.form.get("valor_final"))
            avaluo.estado = 'Finalizado'  # Cambia automáticamente a Finalizado si se asigna el precio de cierre
        
        # También actualiza el valor_total si es modificado en el form
        if request.form.get("valor_total"):
            avaluo.valor_total = float(request.form.get("valor_total"))

        db.session.commit()
        flash("Avalúo actualizado y cerrado con éxito." if avaluo.estado == 'Finalizado' else "Avalúo actualizado.", "info")
        return redirect(url_for('avaluos.listar_perito'))
        
    return render_template("avaluos/perito/editar_avaluo.html", avaluo=avaluo)


@avaluos.route("/perito/eliminar/<int:id>")
@perito_required
def eliminar_avaluo(id):
    avaluo = Avaluo.query.get_or_404(id)
    try:
        db.session.delete(avaluo)
        db.session.commit()
        flash("Registro eliminado.", "warning")
    except Exception as e:
        db.session.rollback()
        flash("No se pudo eliminar.", "danger")
    return redirect(url_for('avaluos.listar_perito'))