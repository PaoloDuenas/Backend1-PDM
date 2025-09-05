from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()


def init_db(app):
    app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
    app.config['MYSQL_USER'] = os.getenv("DB_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("DB_NAME")
    app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT"))
    mysql.init_app(app)


def get_db_connection(dictionary=False):
    """
    Devuelve la conexión y un cursor.
    Si dictionary=True, devuelve un cursor que retorna diccionarios.
    """
    try:
        conn = mysql.connection
        if dictionary:
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        else:
            cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")
