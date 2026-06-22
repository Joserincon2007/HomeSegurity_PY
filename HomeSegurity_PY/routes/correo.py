from flask_mail import Message
from extensions import mail


def enviar_correo_credenciales(correo, password):

    try:
        msg = Message(
            subject="✅ Credenciales de Administrador - Home Security",
            sender="joserinconxc2008@gmail.com",
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
http://localhost:5000

Home Security
        """

        mail.send(msg)
        print("✅ Correo enviado correctamente")

    except Exception as e:
        print("❌ Error enviando correo:", e)