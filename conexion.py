import mysql.connector
from Config import Config

<<<<<<< HEAD

def get_connection():

    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        autocommit=True
    )

    return connection
=======
def get_connection():
    connection = mysql.connector.connect(
        host="acela.proxy.rlwy.net",
        port=48809,
        user="root",
        password="XKhSuFKjJqxqrrRzDJkMMwkREOAdIuPd",
        database="railway"
    )
    return connection
>>>>>>> c67dab7e4e54e767e2a4caa836b42272f18ba9ed
