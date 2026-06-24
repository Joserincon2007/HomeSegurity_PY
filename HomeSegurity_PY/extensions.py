from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

mysql = MySQL()
mail = Mail()
db = SQLAlchemy()