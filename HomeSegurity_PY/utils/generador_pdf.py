from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime

def generar_pdf(avaluo, vivienda):
    """
    Genera un PDF usando xhtml2pdf. 
    Accede a los datos usando puntos (objetos SQLAlchemy).
    """
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: letter; margin: 2cm; }}
            body {{ font-family: Helvetica, Arial, sans-serif; color: #333; }}
            .header {{ text-align: center; border-bottom: 2px solid #002366; padding-bottom: 10px; }}
            .blue-text {{ color: #002366; font-weight: bold; }}
            .content {{ margin-top: 20px; line-height: 1.5; }}
            .footer {{ margin-top: 50px; font-size: 9px; text-align: center; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 class="blue-text">Informe Técnico de Avalúo</h1>
            <p>homeSegurity - Valuación Digital</p>
        </div>
        
        <div class="content">
            <h3>Información del Inmueble</h3>
            <p><strong>Dirección:</strong> {vivienda.direccion}</p>
            <p><strong>Localidad:</strong> {vivienda.localidad}</p>
            <p><strong>Área:</strong> {vivienda.area_m2} m²</p>
            
            <hr>
            
            <h3>Resultado de la Valoración</h3>
            <p><strong>Precio por m²:</strong> ${"{:,.2f}".format(avaluo.precio_m2)}</p>
            <p><strong>Valor Total Estimado:</strong> <span class="blue-text">${"{:,.0f}".format(avaluo.valor_total or 0)}</span></p>            
            <p><strong>Descripción Técnica:</strong><br/>
            {avaluo.descripcion}</p>
        </div>

        <div class="footer">
            <p>Este documento es una previsualización oficial de homeSegurity.</p>
            <p>Generado el: {avaluo.fecha.strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </body>
    </html>
    """

    # Crear el PDF en memoria
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None