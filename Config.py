import os
from dotenv import load_dotenv

# Cargamos el archivo .env del servidor
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "d5fb8c4fa8bd46638dadc4e751e0d68d")

    # Configuración dinámica para MySQL (flask_mysqldb)
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "acela.proxy.rlwy.net")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 48809))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "XKhSuFKjJqxqrrRzDJkMMwkREOAdIuPd")
    MYSQL_DB = os.environ.get("MYSQL_DB", "railway")

    # Configuración dinámica para SQLAlchemy (Usa las mismas variables del .env)
    # Formamos la URL: mysql://usuario:contraseña@host:puerto/base_datos
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", 
        f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ======================
    # MAIL CONFIG (API BREVO)
    # ======================
    # Aunque manejamos la API directamente en correo.py, dejamos este respaldo limpio
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "joserinconxc2008@gmail.com")
