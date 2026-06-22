from flask_mail import Message
from extensions import mail  # Importas la instancia que configuramos arriba
from flask import current_app

def enviar_correo(receptor, asunto, cuerpo, adjunto=None):
    try:
        msg = Message(
            subject=asunto,
            recipients=[receptor],
            body=cuerpo,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )

        if adjunto:
            msg.attach(
                "Avaluo_Tecnico.pdf",
                "application/pdf",
                adjunto
            )

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error en Flask-Mail: {e}")
        return False