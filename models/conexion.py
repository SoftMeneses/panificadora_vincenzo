import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            db = "panificadora",
            port = 3306
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
