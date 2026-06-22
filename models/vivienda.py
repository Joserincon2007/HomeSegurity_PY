from extensions import db

class Vivienda(db.Model):

    __tablename__ = "vivienda"

    id_vivienda = db.Column(db.Integer, primary_key=True)
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    precio = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    foto = db.Column(db.String(200))
    estado_publicacion = db.Column(db.String(20))
    area_m2 = db.Column(db.Float, nullable=False) 
    localidad = db.Column(db.String(100))
    estrato = db.Column(db.Integer)
    antiguedad = db.Column(db.Integer)
    parqueaderos = db.Column(db.Integer)