from extensions import db
from datetime import datetime

class Avaluo(db.Model):
    __tablename__ = "avaluo"

    id_avaluo = db.Column(db.Integer, primary_key=True)
    id_vivienda = db.Column(db.Integer, db.ForeignKey("vivienda.id_vivienda"), nullable=False)
    id_usuario = db.Column(db.Integer, nullable=True) 
    
    # CORRECCIÓN 1: Agregar explícitamente la llave foránea a la tabla perito
    id_perito = db.Column(db.Integer, db.ForeignKey("perito.id_perito"), nullable=True)  

    # CORRECCIÓN 2: Crear la relación para acceder a los datos de la Imagen 1
    # Esto permite que en el HTML hagas a.perito.formacion_academica
    perito = db.relationship("Perito", backref="avaluos_asociados")

    solicitante = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    area_m2 = db.Column(db.Float, nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    precio_m2 = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False) 
    antiguedad = db.Column(db.String(50))
    estrato = db.Column(db.Integer)
    parqueadero = db.Column(db.Integer) # Nombre en la DB
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, id_vivienda, solicitante, correo, area_m2, localidad, precio_m2, valor_total, 
                 antiguedad, estrato, parqueadero, descripcion, id_usuario=None, id_perito=None, fecha=None):
        self.id_vivienda = id_vivienda
        self.solicitante = solicitante
        self.correo = correo
        self.id_usuario = id_usuario
        self.id_perito = id_perito
        self.area_m2 = area_m2
        self.localidad = localidad
        self.precio_m2 = precio_m2
        self.valor_total = valor_total
        self.antiguedad = antiguedad
        self.estrato = estrato
        self.parqueadero = parqueadero # Corregido para que coincida con la columna
        self.descripcion = descripcion
        self.fecha = fecha if fecha else datetime.now()