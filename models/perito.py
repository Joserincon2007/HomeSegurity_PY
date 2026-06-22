from extensions import db # O 'from utils.db import db' según tu proyecto

class Perito(db.Model):
    __tablename__ = 'perito'

    # Llave primaria
    id_perito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Llave foránea hacia la tabla de Usuario (Relación 1:1 o 1:N)
    # Asegúrate de que el nombre de la tabla y columna coincidan: 'usuario.idUsuario'
    idUsuario = db.Column(db.BigInteger, db.ForeignKey('usuario.idUsuario'), nullable=False)
    
    # Campos específicos del perito según tu imagen
    registro_raa = db.Column(db.String(100), nullable=True)
    categoria_especializacion = db.Column(db.String(150), nullable=True)
    formacion_academica = db.Column(db.Text, nullable=True)
    experiencia_anios = db.Column(db.Integer, nullable=True)
    direccion_oficina = db.Column(db.String(200), nullable=True)

    def __init__(self, idUsuario, registro_raa=None, categoria_especializacion=None, 
                 formacion_academica=None, experiencia_anios=None, direccion_oficina=None):
        self.idUsuario = idUsuario
        self.registro_raa = registro_raa
        self.categoria_especializacion = categoria_especializacion
        self.formacion_academica = formacion_academica
        self.experiencia_anios = experiencia_anios
        self.direccion_oficina = direccion_oficina

    # Relación opcional para acceder a los datos del usuario desde el perito
    usuario = db.relationship('Usuario', backref=db.backref('perito_info', uselist=False))