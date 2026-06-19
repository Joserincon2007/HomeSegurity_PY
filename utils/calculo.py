from datetime import datetime
from extensions import db

class Avaluo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vivienda_id = db.Column(db.Integer, nullable=False)

    precio_estimado = db.Column(db.Float)
    estado = db.Column(db.String(20), default="Pendiente")

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    solicitante = db.Column(db.String(100))
    correo = db.Column(db.String(120))