import os
import sys
import requests  # Usamos peticiones web en lugar de SMTP

def enviar_correo_credenciales(correo, password):
    # 1. Traemos la API Key y el remitente desde las variables de entorno
    api_key = os.environ.get('BREVO_API_KEY')
    remitente = os.environ.get('MAIL_DEFAULT_SENDER', 'joserinconxc2008@gmail.com')

    if not api_key:
        print("❌ Error: No se encontró la variable BREVO_API_KEY en el entorno.", file=sys.stderr)
        return False

    # 2. Configuración del endpoint de Brevo v3
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }

    # 3. Estructura del payload en formato JSON
    payload = {
        "sender": {
            "email": remitente,
            "name": "Home Security"
        },
        "to": [
            {
                "email": correo
            }
        ],
        "subject": "✅ Credenciales Autorizadas - Home Security",
        "textContent": f"""
Hola,

Tu solicitud fue APROBADA ✅

Ya puedes ingresar al sistema como ADMINISTRADOR.

🔐 Credenciales:

Correo: {correo}
Contraseña: {password}

Ingresa aquí:
http://142.93.249.184

Home Security
        """
    }

    try:
        # Hacemos la petición POST a través del puerto 443 (Abierto por defecto)
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ Correo enviado correctamente vía API a {correo}", file=sys.stderr)
            return True
        else:
            print(f"❌ Brevo rechazó la API Key o el payload. Código: {response.status_code} - Respuesta: {response.text}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"❌ Error de red al conectar con la API de Brevo: {str(e)}", file=sys.stderr)
        return False
