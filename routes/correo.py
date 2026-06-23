from flask_mail import Message
from extensions import mail
import os  

def enviar_correo_credenciales(correo, password):
    try:
        remitente = os.environ.get('afa7a5001@smtp-brevo.com', 'joserinconxc2008@gmail.com')

        msg = Message(
            subject="✅ Credenciales de Autorizadas - Home Security",
            sender=remitente,
            recipients=[correo]
        )

        msg.body = f"""
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

        mail.send(msg)
        print(f"✅ Correo enviado correctamente a {correo} a través de Brevo")

    except Exception as e:
        print("❌ Error enviando correo:", e)
