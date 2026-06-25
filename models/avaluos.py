from extensions import db
from datetime import datetime, time

class Avaluo(db.Model):
    __tablename__ = 'avaluo'

    id_avaluo = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_vivienda = db.Column(db.BigInteger, db.ForeignKey('vivienda.id_vivienda', ondelete='CASCADE'), nullable=False)
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.idUsuario', ondelete='SET NULL'), nullable=True)
    id_perito = db.Column(db.BigInteger, db.ForeignKey('perito.id_perito', ondelete='SET NULL'), nullable=True)

    # Campos Decimales corregidos de acuerdo a la tabla real
    area_m2 = db.Column(db.Numeric(10, 2), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    precio_m2 = db.Column(db.Numeric(12, 2), nullable=False)
    valor_total = db.Column(db.Numeric(15, 2), nullable=False)
    valor_final = db.Column(db.Numeric(15, 2), nullable=True)

    antiguedad = db.Column(db.Integer, nullable=True)
    estrato = db.Column(db.Integer, nullable=True)
    parqueadero = db.Column(db.Boolean, default=False)
    descripcion = db.Column(db.Text, nullable=True)
    solicitante = db.Column(db.String(100), default='Sin nombre')
    correo = db.Column(db.String(100), default='sin_correo@mail.com')
    estado = db.Column(db.String(30), default='Pendiente')

    # CORRECCIÓN CLAVE: Tipos nativos de Fecha y Hora para MySQL
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cita = db.Column(db.Date, nullable=True)          # Tipo date
    hora_cita = db.Column(db.Time, nullable=True)           # Tipo time
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
