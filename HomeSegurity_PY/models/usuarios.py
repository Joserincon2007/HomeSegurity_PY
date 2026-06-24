# Imprescindible: Importar la instancia central de db
from extensions import db # <-- AJUSTA ESTA RUTA si tu db está en otro archivo (ej: 'from db import db')

class Usuario(db.Model):
    __tablename__ = 'usuario' # <-- Asegúrate que en DB la tabla se llama 'usuario'

    # Campos primarios y obligatorios
    idUsuario = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    primerNombre = db.Column(db.String(100), nullable=False) # varchar(100) en PHPMyAdmin
    primerApellido = db.Column(db.String(100), nullable=False) # varchar(100)
    contraseña = db.Column(db.String(255), nullable=False) # varchar(255) para hashes
    correo = db.Column(db.String(100), nullable=False, unique=True) # varchar(100) único

    # Campos opcionales (Nulo: Sí)
    edad = db.Column(db.Integer, nullable=True) # int(11)
    direccion = db.Column(db.String(200), nullable=True) # varchar(200)
    num_documento = db.Column(db.String(50), nullable=True, unique=True) # varchar(50)
    telefono = db.Column(db.String(20), nullable=True) # varchar(20)

    # Campos de estado y roles
    # tinyint(1) -> Usamos Boolean de SQLAlchemy (1=True, 0=False)
    estadoCuenta = db.Column(db.Boolean, nullable=True, default=True) 
    rol = db.Column(db.String(50), nullable=True) # 'CLIENTE', 'PERITO', etc.
    estado_admin = db.Column(db.Boolean, nullable=True, default=False) 
    admin_token = db.Column(db.String(255), nullable=True) #varchar(255)

    def __init__(self, primerNombre, primerApellido, contraseña, correo, edad=None, direccion=None, num_documento=None, telefono=None, rol='CLIENTE', estado_admin=False):
        self.primerNombre = primerNombre
        self.primerApellido = primerApellido
        self.contraseña = contraseña
        self.correo = correo
        self.edad = edad
        self.direccion = direccion
        self.num_documento = num_documento
        self.telefono = telefono
        self.rol = rol
        self.estadoCuenta = True # Activa por defecto
        self.estado_admin = estado_admin
        self.admin_token = None

    # --- Propiedad Útil para el CRUD de Perito ---
    # Esto te permitirá usar u.nombre_completo en el HTML sin tenerlo en la base de datos
    @property
    def nombre_completo(self):
        """Devuelve el nombre completo concatenado."""
        return f"{self.primerNombre} {self.primerApellido}"