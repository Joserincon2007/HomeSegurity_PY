from extensions import db
from datetime import datetime

class Avaluo(db.Model):
    __tablename__ = 'avaluo'

    # Llaves Primarias y Foráneas (Todas mapeadas como BigInteger según tu tabla)
    id_avaluo = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_vivienda = db.Column(db.BigInteger, db.ForeignKey('vivienda.id_vivienda', ondelete='CASCADE'), nullable=False)
    id_usuario = db.Column(db.BigInteger, db.ForeignKey('usuario.idUsuario', ondelete='SET NULL'), nullable=True)
    id_perito = db.Column(db.BigInteger, db.ForeignKey('perito.id_perito', ondelete='SET NULL'), nullable=True)

    # Campos de texto (varstring -> String)
    area_m2 = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    precio_m2 = db.Column(db.String(100), nullable=True)
    valor_total = db.Column(db.String(100), nullable=False)
    solicitante = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    estado = db.Column(db.String(100), default='Pendiente')
    valor_final = db.Column(db.String(100), nullable=True)

    # Campos Numéricos y Booleanos
    antiguedad = db.Column(db.Integer, nullable=True)   # mediumint
    estrato = db.Column(db.Integer, nullable=False)      # mediumint
    parqueadero = db.Column(db.Boolean, default=False)  # tinyint (boolean)

    # Blobs y Textos largos
    descripcion = db.Column(db.Text, nullable=True)     # blob/text

    # Fechas y Tiempos
    fecha = db.Column(db.DateTime, default=datetime.utcnow) # timestamp
    fecha_cita = db.Column(db.Date, nullable=True)          # date
    hora_cita = db.Column(db.String(50), nullable=True)     # varstring
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

    def __init__(self, id_vivienda, solicitante, correo, estrato, localidad, area_m2, valor_total, 
                 id_usuario=None, id_perito=None, precio_m2=None, antiguedad=None, parqueadero=False, 
                 descripcion=None, estado='Pendiente', fecha_cita=None, hora_cita=None, valor_final=None):
        self.id_vivienda = id_vivienda
        self.id_usuario = id_usuario
        self.id_perito = id_perito
        self.area_m2 = str(area_m2)
        self.localidad = localidad
        self.precio_m2 = str(precio_m2) if precio_m2 else None
        self.valor_total = str(valor_total)
        self.antiguedad = antiguedad
        self.estrato = estrato
        self.parqueadero = parqueadero
        self.descripcion = descripcion
        self.solicitante = solicitante
        self.correo = correo
        self.estado = estado
        self.fecha_cita = fecha_cita
        self.hora_cita = hora_cita
        self.valor_final = str(valor_final) if valor_final else None