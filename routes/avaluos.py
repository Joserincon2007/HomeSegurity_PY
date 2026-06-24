import sys
import os
import base64  # Requerido para codificar el PDF adjunto en la API de Brevo
import requests
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
# FUNCIÓN INTERNA AUXILIAR: ENVIAR CORREO MEDIANTE API BREVO CON/SIN ADJUNTO
# ==============================================================================
def enviar_correo_api_brevo(receptor, asunto, cuerpo, adjunto_bytes=None, nombre_adjunto="documento.pdf"):
    """
    Despacha notificaciones utilizando la API HTTP v3 de Brevo por el puerto 443.
    Evita los cuelgues del firewall de DigitalOcean en puertos SMTP.
    """
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

    # Si pasamos un PDF, lo convertimos a string Base64 requerido por la API
    if adjunto_bytes:
        encoded_content = base64.b64encode(adjunto_bytes).decode('utf-8')
        payload["attachment"] = [
            {
                "content": encoded_content,
                "name": nombre_adjunto
            }
        ]

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        if response.status_code in [200, 201, 202]:
            print(f"✅ Notificación enviada con éxito vía API a {receptor}", file=sys.stderr)
            return True
        else:
            print(f"❌ Brevo API rechazó la solicitud ({response.status_code}): {response.text}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"❌ Error de red conectando a la API de Brevo: {str(e)}", file=sys.stderr)
        return False


# 1. VISTA PARA MOSTRAR EL FORMULARIO
@avaluos.route("/crear/<int:vivienda_id>", methods=["GET"])
def crear(vivienda_id):
    if 'idUsuario' not in session:
        flash("Debes iniciar sesión para solicitar un avalúo.", "warning")
        return redirect(url_for('auth.login'))

    vivienda = Vivienda.query.get_or_404(vivienda_id)

    precio_m2, precio_total, descripcion = calcular_avaluo(
        vivienda.area_m2,
        vivienda.localidad,
        vivienda.estrato,
        vivienda.antiguedad,
        vivienda.parqueaderos
    )

    return render_template(
        "avaluos/crear.html",
        vivienda=vivienda,
        precio=precio_total,
        precio_m2=precio_m2,
        descripcion=descripcion
    )

# 2. RUTA PARA PREVISUALIZAR EL PDF
@avaluos.route("/preview_pdf/<int:vivienda_id>")
def preview_pdf(vivienda_id):
    vivienda = Vivienda.query.get_or_404(vivienda_id)
    
    precio_m2, precio_total, descripcion = calcular_avaluo(
        vivienda.area_m2, 
        vivienda.localidad,
        vivienda.estrato,
        vivienda.antiguedad,
        vivienda.parqueaderos
    )
    
    temp_avaluo = Avaluo(
        id_vivienda=vivienda.id_vivienda,
        solicitante=f"{session.get('usuario', '')} {session.get('apellido', '')}",
        correo=session.get('correo', ''),
        precio_m2=precio_m2,
        valor_total=precio_total,
        area_m2=vivienda.area_m2,
        localidad=vivienda.localidad,
        antiguedad=vivienda.antiguedad,
        estrato=vivienda.estrato,
        parqueadero=vivienda.parqueaderos,
        descripcion=descripcion,
        fecha=datetime.now()
    )
    
    pdf = generar_pdf(temp_avaluo, vivienda)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=previsualizacion_avaluo.pdf'
    return response

# 3. FUNCIÓN FINAL: PROCESAR, GUARDAR Y ENVIAR CORREO VIA API
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
        vivienda.area_m2,
        vivienda.localidad,
        vivienda.estrato,
        vivienda.antiguedad,
        vivienda.parqueaderos
    )

    try:
        nuevo_avaluo = Avaluo(
            id_vivienda=vivienda.id_vivienda,
            solicitante=nombre_completo,
            correo=correo_cliente,
            area_m2=vivienda.area_m2,
            localidad=vivienda.localidad,
            precio_m2=precio_m2,
            valor_total=precio_total,
            antiguedad=vivienda.antiguedad,
            estrato=vivienda.estrato,
            parqueadero=vivienda.parqueaderos,
            descripcion=descripcion,
            id_usuario=id_usuario_logueado,
            fecha=datetime.now()
        )

        db.session.add(nuevo_avaluo)
        db.session.commit()

        # Generar PDF real desde binario
        pdf_final = generar_pdf(nuevo_avaluo, vivienda)
        
        # 🚀 Despachamos mediante la API HTTP de Brevo
        enviar_correo_api_brevo(
            receptor=correo_cliente,
            asunto="Tu Avalúo Técnico - Home Security",
            cuerpo=f"Hola {nombre_completo}, adjuntamos el informe del avalúo técnico de tu propiedad.",
            adjunto_bytes=pdf_final,
            nombre_adjunto=f"Avaluo_{vivienda.localidad}.pdf"
        )

        flash("Avalúo generado y enviado a tu correo correctamente.", "success")
        return redirect(url_for('avaluos.listar'))

    except Exception as e:
        db.session.rollback()
        print(f"❌ DEBUG ERROR EN PROCESAR AVALÚO: {e}", file=sys.stderr)
        flash(f"Error al guardar: {str(e)}", "danger")
        return redirect(request.referrer)

# 4. DASHBOARD Y GESTIÓN
@avaluos.route("/listar")
def listar():
    avaluos_list = (
        db.session.query(Avaluo, Vivienda)
        .join(Vivienda, Vivienda.id_vivienda == Avaluo.id_vivienda)
        .order_by(Avaluo.fecha.desc())
        .all()
    )
    return render_template("avaluos/listar.html", avaluos=avaluos_list)

@avaluos.route("/dashboard_perito")
def dashboard_perito():
    avaluos_con_vivienda = db.session.query(Avaluo, Vivienda).join(
        Vivienda, Avaluo.id_vivienda == Vivienda.id_vivienda
    ).all()
    return render_template("dashboard/dashboard_perito.html", avaluos=avaluos_con_vivienda)

@avaluos.route("/confirmar_cita/<int:id_avaluo>", methods=["POST"])
def confirmar_cita(id_avaluo):
    avaluo = Avaluo.query.get_or_404(id_avaluo)
    vivienda = Vivienda.query.get(avaluo.id_vivienda)
    
    fecha_cita = request.form.get("fecha_cita")
    id_perito = request.form.get("id_perito")
    
    correo_destino = str(avaluo.correo).strip()
    nombre_cliente = str(avaluo.solicitante).strip()

    try:
        avaluo.id_perito = id_perito
        db.session.commit()

        # Generamos el reporte preliminar
        pdf_adjunto = generar_pdf(avaluo, vivienda)

        cuerpo_correo = f"""
Hola {nombre_cliente},

Su solicitud de avalúo para la propiedad ubicada en {vivienda.direccion} ha sido confirmada.

DETALLES DE LA VISITA TÉCNICA:

Fecha y Hora: {fecha_cita}
Perito Asignado: ID {id_perito}

REQUISITOS OBLIGATORIOS PARA LA INSPECCIÓN:
Para proceder con la certificación del avalúo de su apartamento, es necesario que tenga listos:

1. Certificado de Tradición y Libertad (reciente).
2. Escritura pública de la propiedad.
3. Último recibo del Impuesto Predial.
4. Plano arquitectónico del apartamento.
5. Recibo de servicios públicos (para verificar estrato).

IMPORTANTE: La visita dura entre 45 a 60 minutos. El perito debe acceder a todas las áreas.

Adjunto encontrará el informe preliminar de Home Security.

Atentamente,
Departamento Técnico - Home Security
"""

        # 🚀 Despachamos la confirmación de la cita usando la API HTTP de Brevo
        print(f"--> [PERITO] Confirmando cita para {correo_destino} vía API...", file=sys.stderr)
        enviar_correo_api_brevo(
            receptor=correo_destino,
            asunto="CONFIRMACIÓN: Cita de Inspección y Requisitos",
            cuerpo=cuerpo_correo,
            adjunto_bytes=pdf_adjunto,
            nombre_adjunto="Inspeccion_Preliminar.pdf"
        )

        flash(f"Cita confirmada. Requisitos enviados a {correo_destino}.", "success")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error detallado en confirmar_cita: {type(e).__name__} - {e}", file=sys.stderr)
        flash("Error al procesar la confirmación. Verifica la configuración de correo.", "danger")

    return redirect(url_for('avaluos.dashboard_perito'))

@avaluos.route("/sincronizar_peritos")
def sincronizar_peritos():
    try:
        usuarios_peritos = Usuario.query.filter_by(rol='PERITO').all()
        contador = 0
        for u in usuarios_peritos:
            existe = Perito.query.filter_by(idUsuario=u.idUsuario).first()
            if not existe:
                nuevo_perito = Perito(
                    idUsuario=u.idUsuario,
                    registro_raa="SIN_REGISTRO", 
                    categoria_especializacion="General",
                    formacion_academica="Técnico/Profesional",
                    experience_anios=0,
                    direccion_oficina=u.direccion 
                )
                db.session.add(nuevo_perito)
                contador += 1
        
        db.session.commit()
        flash(f"Sincronización terminada. {contador} usuarios ahora son peritos activos.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR DE SINCRONIZACIÓN: {e}", file=sys.stderr)
        flash("No se pudo sincronizar la tabla de peritos.", "danger")
        
    return redirect(url_for('avaluos.dashboard_perito'))

@avaluos.route("/perito/crear_manual", methods=["GET", "POST"])
def crear_manual():
    if request.method == "POST":
        try:
            id_vivienda_form = request.form.get("id_vivienda")
            id_usuario_form = request.form.get("id_usuario")
            id_perito_form = request.form.get("id_perito") 
            
            val_perito = int(id_perito_form) if id_perito_form and id_perito_form.strip() else None
            v_vivienda = int(id_vivienda_form) if id_vivienda_form and id_vivienda_form.strip() else 0
            v_usuario = int(id_usuario_form) if id_usuario_form and id_usuario_form.strip() else 0
            
            v_area = float(request.form.get("area_m2") or 0)
            v_precio = float(request.form.get("precio_m2") or 0)
            v_total = float(request.form.get("valor_total") or (v_area * v_precio))
            
            nuevo_avaluo = Avaluo(
                id_vivienda=v_vivienda,
                id_usuario=v_usuario,
                id_perito=val_perito, 
                area_m2=v_area,
                localidad=request.form.get("localidad") or "Sin especificar",
                precio_m2=v_precio,
                valor_total=v_total,
                antiguedad=request.form.get("antiguedad"),
                estrato=request.form.get("estrato"),
                parqueaderos=request.form.get("parqueaderos"),
                descripcion=request.form.get("descripcion"),
                solicitante=request.form.get("solicitante") or "Anónimo",
                correo=request.form.get("correo") or "sin@correo.com"
            )

            db.session.add(nuevo_avaluo)
            db.session.commit()
            
            flash("Avalúo registrado correctamente", "success")
            return redirect(url_for('avaluos.listar_perito'))

        except Exception as e:
            db.session.rollback()
            print(f"❌ ERROR CRÍTICO EN CREAR MANUAL: {str(e)}", file=sys.stderr)
            flash(f"Error al registrar: {str(e)}", "danger")
    
    usuarios = Usuario.query.all()
    perito_db = Perito.query.all()
    return render_template("avaluos/perito/crear_manual.html", peritos=perito_db, usuarios=usuarios)

@avaluos.route("/perito/mis_avaluos")
def listar_perito():
    id_usuario_logueado = session.get('idUsuario')
    if not id_usuario_logueado:
        return "Error: No hay sesión activa", 401

    perito = Perito.query.filter_by(idUsuario=id_usuario_logueado).first()
    if perito:
        lista_avaluos = Avaluo.query.filter_by(id_perito=perito.id_perito).all()
    else:
        lista_avaluos = []

    return render_template("avaluos/perito/listarPerito.html", avaluos=lista_avaluos, perito=perito)

@avaluos.route("/perito/editar/<int:id>", methods=["GET", "POST"])
def editar_avaluo(id):
    avaluo = Avaluo.query.get_or_404(id)
    if request.method == "POST":
        avaluo.solicitante = request.form.get("solicitante")
        avaluo.valor_total = request.form.get("valor_total")
        avaluo.descripcion = request.form.get("descripcion")
        
        db.session.commit()
        flash("Avalúo actualizado.", "info")
        return redirect(url_for('avaluos.listar_perito'))
        
    return render_template("avaluos/perito/editar_avaluo.html", avaluo=avaluo)

@avaluos.route("/perito/eliminar/<int:id>")
def eliminar_avaluo(id):
    avaluo = Avaluo.query.get_or_404(id)
    try:
        db.session.delete(avaluo)
        db.session.commit()
        flash("Registro eliminado correctamente.", "warning")
    except Exception as e:
        db.session.rollback()
        flash("No se pudo eliminar el registro.", "danger")
        
    return redirect(url_for('avaluos.listar_perito'))