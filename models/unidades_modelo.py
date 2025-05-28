from conexion import obtener_conexion
from mysql.connector import Error

class UnidadModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_unidades(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM unidades")
        unidades = cursor.fetchall()
        cursor.close()
        return unidades
    
    def insertar_unidad(self, descr_und):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO unidades (descr_und) VALUES(%s)"
            cursor.execute(sql, (descr_und,))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid
        except Error as e:
            return e
        
    def actualizar_unidad(self, id_und_med, descr_und):
        cursor = self.conexion.cursor()
        sql = "UPDATE unidades SET descr_und = %s WHERE id_und_med = %s"
        cursor.execute(sql, (descr_und, id_und_med))
        self.conexion.commit()
        cursor.close()
        return cursor.rowcount
    
    def eliminar_unidad(self, id_und_med):
        cursor = self.conexion.cursor()
        sql = "DELETE FROM unidades WHERE id_und_med = %s"
        cursor.execute(sql, (id_und_med,))
        self.conexion.commit()
        cursor.close()
        return cursor.rowcount
    