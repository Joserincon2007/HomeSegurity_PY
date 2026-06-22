import mysql.connector
from Config import Config

def get_connection():
    connection = mysql.connector.connect(
        host="acela.proxy.rlwy.net",
        port=48809,
        user="root",
        password="XKhSuFKjJqxqrrRzDJkMMwkREOAdIuPd",
        database="railway"
    )
    return connection
