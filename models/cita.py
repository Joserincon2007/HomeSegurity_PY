from extensions import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = "citas"

    id = db.Column(db.Integer, primary_key=True)

    nombre_cliente = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))

    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

    vivienda_id = db.Column(
        db.Integer,
        db.ForeignKey("viviendas.id"),
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    vivienda = db.relationship("Vivienda", backref="citas")