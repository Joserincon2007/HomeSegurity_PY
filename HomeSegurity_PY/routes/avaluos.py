from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, session
from models.avaluos import Avaluo
from models.vivienda import Vivienda
from utils.precios_bogota import calcular_avaluo
from utils.generador_pdf import generar_pdf
from utils.correo import enviar_correo
from models.usuarios import Usuario 
from models.perito import Perito
from extensions import db
from datetime import datetime

avaluos = Blueprint("avaluos", __name__, url_prefix="/avaluos")

# 1. VISTA PARA MOSTRAR EL FORMULARIO
@avaluos.route("/crear/<int:vivienda_id>", methods=["GET"])
def crear(vivienda_id):
    # Protección: Opción B (Si no hay idUsuario, redirigir al login)
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
    
    # Objeto temporal. Pasamos strings vacíos para solicitante y correo ya que es solo preview
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

# 3. FUNCIÓN FINAL: PROCESAR, GUARDAR Y ENVIAR CORREO
@avaluos.route("/procesar", methods=["POST"])
def procesar_avaluo():
    # --- VALIDACIÓN DE SESIÓN (Sincronizada con tu Login) ---
    if 'idUsuario' not in session:
        flash("Sesión expirada. Por favor, ingresa a tu cuenta.", "danger")
        return redirect(url_for('auth.login'))

    vivienda_id = request.form.get("vivienda_id")
    correo_cliente = request.form.get("correo") or session.get('correo')
    
    # Extraemos datos usando tus llaves de sesión: idUsuario, usuario, apellido
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
        # Creamos el objeto con los argumentos requeridos por el constructor (__init__)
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

        # Enviar PDF real después de guardar
        pdf_final = generar_pdf(nuevo_avaluo, vivienda)
        enviar_correo(
            receptor=correo_cliente,
            asunto="Tu Avalúo Técnico - homeSegurity",
            cuerpo=f"Hola {nombre_completo}, adjuntamos el avalúo de tu propiedad.",
            adjunto=pdf_final
        )

        flash("Avalúo generado y enviado a tu correo correctamente.", "success")
        return redirect(url_for('avaluos.listar'))

    except Exception as e:
        db.session.rollback()
        print(f"DEBUG ERROR EN PROCESAR: {e}")
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
    # Realizamos un JOIN para obtener tanto el avaluo como la vivienda asociada
    # Esto genera la "tupla" que el HTML espera (avaluo, vivienda)
    avaluos_con_vivienda = db.session.query(Avaluo, Vivienda).join(
        Vivienda, Avaluo.id_vivienda == Vivienda.id_vivienda
    ).all()
    
    return render_template("dashboard/dashboard_perito.html", avaluos=avaluos_con_vivienda)

@avaluos.route("/confirmar_cita/<int:id_avaluo>", methods=["POST"])
def confirmar_cita(id_avaluo):
    # 1. Obtener datos del avalúo y la vivienda
    avaluo = Avaluo.query.get_or_404(id_avaluo)
    vivienda = Vivienda.query.get(avaluo.id_vivienda)
    
    fecha_cita = request.form.get("fecha_cita")
    # Limpiamos el ID del perito y el nombre del solicitante de cualquier espacio
    id_perito = request.form.get("id_perito")
    
    # --- LIMPIEZA DE DATOS PARA EVITAR ERROR 555 ---
    # Convertimos a string y usamos .strip() para eliminar espacios o saltos de línea
    correo_destino = str(avaluo.correo).strip()
    nombre_cliente = str(avaluo.solicitante).strip()

    try:
        # 2. Actualizar el registro en la base de datos
        avaluo.id_perito = id_perito
        db.session.commit()

        # 3. Generar el PDF
        pdf_adjunto = generar_pdf(avaluo, vivienda)

        # 4. Redactar el mensaje (Aseguramos que no haya caracteres extraños)
        cuerpo_correo = f"""
Hola {nombre_cliente},

Su solicitud de avalúo para la propiedad ubicada en {vivienda.direccion} ha sido confirmada.

DETALLES DE LA VISITA TÉCNICA:

Fecha y Hora: {fecha_cita}
Perito Asignado: {id_perito}

REQUISITOS OBLIGATORIOS PARA LA INSPECCIÓN:
Para proceder con la certificación del avalúo de su apartamento, es necesario que tenga listos:

1. Certificado de Tradición y Libertad (reciente).
2. Escritura pública de la propiedad.
3. Último recibo del Impuesto Predial.
4. Plano arquitectónico del apartamento.
5. Recibo de servicios públicos (para verificar estrato).

IMPORTANTE: La visita dura entre 45 a 60 minutos. El perito debe acceder a todas las áreas.

Adjunto encontrará el informe preliminar de homeSegurity.

Atentamente,
Departamento Técnico - homeSegurity
"""

        # 5. Notificar por correo con datos limpios
        print(f"DEBUG: Intentando enviar correo a: '{correo_destino}'")
        
        enviar_correo(
            receptor=correo_destino,
            asunto="CONFIRMACIÓN: Cita de Inspección y Requisitos",
            cuerpo=cuerpo_correo,
            adjunto=pdf_adjunto
        )

        flash(f"Cita confirmada. Requisitos enviados a {correo_destino}.", "success")

    except Exception as e:
        db.session.rollback()
        # Imprimimos el error completo en consola para debuggear
        print(f"Error detallado en confirmar_cita: {type(e).__name__} - {e}")
        flash("Error al procesar la confirmación. Verifica la configuración de correo.", "danger")

    return redirect(url_for('avaluos.dashboard_perito'))


@avaluos.route("/sincronizar_peritos")
def sincronizar_peritos():
    try:
        from models.usuarios import Usuario 
        from models.perito import Perito     

        # Filtramos usuarios con rol PERITO
        usuarios_peritos = Usuario.query.filter_by(rol='PERITO').all()
        
        contador = 0
        for u in usuarios_peritos:
            # Verificamos si ya existe en la tabla perito por su idUsuario
            existe = Perito.query.filter_by(idUsuario=u.idUsuario).first()
            
            if not existe:
                # Creamos el registro en la tabla perito usando los datos de usuario
                nuevo_perito = Perito(
                    idUsuario=u.idUsuario,
                    registro_raa="SIN_REGISTRO", 
                    categoria_especializacion="General",
                    formacion_academica="Técnico/Profesional",
                    experiencia_anios=0,
                    direccion_oficina=u.direccion # Usamos la dirección de la tabla usuario
                )
                db.session.add(nuevo_perito)
                contador += 1
        
        db.session.commit()
        flash(f"Sincronización terminada. {contador} usuarios ahora son peritos activos.", "success")
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR DE SINCRONIZACIÓN: {e}")
        flash("No se pudo sincronizar la tabla de peritos.", "danger")
        
    return redirect(url_for('avaluos.dashboard_perito'))

# --- CREACIÓN MANUAL POR EL PERITO ---
@avaluos.route("/perito/crear_manual", methods=["GET", "POST"])
def crear_manual():
    if request.method == "POST":
        print("--- INICIANDO PROCESO DE GUARDADO ---")
        try:
            # 1. Captura de datos del formulario
            id_vivienda_form = request.form.get("id_vivienda")
            id_usuario_form = request.form.get("id_usuario")
            id_perito_form = request.form.get("id_perito") # Capturamos del select del HTML
            
            # 2. Conversiones seguras y manejo de variables
            # Definimos val_perito correctamente para evitar el error "not defined"
            val_perito = int(id_perito_form) if id_perito_form and id_perito_form.strip() else None
            
            v_vivienda = int(id_vivienda_form) if id_vivienda_form and id_vivienda_form.strip() else 0
            v_usuario = int(id_usuario_form) if id_usuario_form and id_usuario_form.strip() else 0
            
            v_area = float(request.form.get("area_m2") or 0)
            v_precio = float(request.form.get("precio_m2") or 0)
            v_total = float(request.form.get("valor_total") or (v_area * v_precio))
            
            # 3. Creación del objeto Avaluo
            nuevo_avaluo = Avaluo(
                id_vivienda=v_vivienda,
                id_usuario=v_usuario,
                id_perito=val_perito, # <--- Ahora sí está definida
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

            # 4. Persistencia en la DB
            db.session.add(nuevo_avaluo)
            db.session.commit()
            
            print(">>> ¡GUARDADO EXITOSO EN LA BASE DE DATOS! <<<")
            flash("Avalúo registrado correctamente", "success")
            return redirect(url_for('avaluos.listar_perito'))

        except Exception as e:
            db.session.rollback()
            print(f"!!! ERROR CRÍTICO: {str(e)}")
            flash(f"Error al registrar: {str(e)}", "danger")
    
    # --- BLOQUE PARA CARGAR LA PÁGINA (GET) ---
    usuarios = Usuario.query.all()
    perito_db = Perito.query.all()
    
    print(f"DEBUG: Cantidad de peritos encontrados: {len(perito_db)}")

    return render_template("avaluos/perito/crear_manual.html", 
                           peritos=perito_db, 
                           usuarios=usuarios)


# --- LISTAR SOLO LOS AVALÚOS DEL PERITO ---
@avaluos.route("/perito/mis_avaluos") # <-- Verifica que el prefijo del blueprint sea /avaluos
def listar_perito():
    # 1. Obtenemos el ID del usuario logueado desde la sesión
    id_usuario_logueado = session.get('idUsuario')

    if not id_usuario_logueado:
        return "Error: No hay sesión activa", 401

    # 2. Consultamos la tabla 'perito' para obtener su id_perito real
    perito = Perito.query.filter_by(idUsuario=id_usuario_logueado).first()

    if perito:
        # 3. Traemos todos los avalúos que coincidan con ese id_perito
        # Usamos .all() para obtener la lista completa
        lista_avaluos = Avaluo.query.filter_by(id_perito=perito.id_perito).all()
        
        print(f"DEBUG: Se encontraron {len(lista_avaluos)} avalúos para el perito ID {perito.id_perito}")
    else:
        lista_avaluos = []
        print("DEBUG: El usuario logueado no está registrado como perito.")

    # 4. Enviamos los datos al HTML (asegúrate de que el nombre del archivo sea correcto)
    return render_template("avaluos/perito/listarPerito.html", avaluos=lista_avaluos, perito=perito)

# --- EDITAR AVALÚO ---
@avaluos.route("/perito/editar/<int:id>", methods=["GET", "POST"])
def editar_avaluo(id):
    avaluo = Avaluo.query.get_or_404(id)
    
    if request.method == "POST":
        avaluo.solicitante = request.form.get("solicitante")
        avaluo.valor_total = request.form.get("valor_total")
        avaluo.descripcion = request.form.get("descripcion")
        # Actualiza los demás campos necesarios...
        
        db.session.commit()
        flash("Avalúo actualizado.", "info")
        return redirect(url_for('avaluos.listar_perito'))
        
    return render_template("avaluos/perito/editar_avaluo.html", avaluo=avaluo)

# --- ELIMINAR AVALÚO ---
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