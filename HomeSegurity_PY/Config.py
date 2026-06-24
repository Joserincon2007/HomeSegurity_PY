import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = "d5fb8c4fa8bd46638dadc4e751e0d68d"

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'homesegurity_py'

    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/homesegurity_py"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # ======================
    # MAIL CONFIG
    # ======================
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_USERNAME = "joserinconxc2008@gmail.com"
    MAIL_PASSWORD = "feuybugsrfzpcdyq"
    MAIL_DEFAULT_SENDER = "Home Security <joserinconxc2008@gmail.com>"