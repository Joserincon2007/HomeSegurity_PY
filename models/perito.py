from extensions import db

class Perito(db.Model):
    __tablename__ = 'perito'
    
    id_perito = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.BigInteger, db.ForeignKey('usuario.idUsuario', ondelete='CASCADE'), nullable=False)
    
    # Nuevos campos
    primerNombre = db.Column(db.String(100), nullable=False)
    primerApellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=True)