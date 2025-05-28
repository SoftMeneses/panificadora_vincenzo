from conexion import obtener_conexion
from mysql.connector import Error

class PanModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_panes(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM panes")
        panes = cursor.fetchall()
        cursor.close()
        return panes
    
    def insertar_pan(self, descr_pan):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO panes (descr_pan) VALUES(%s)"
            cursor.execute(sql, (descr_pan,))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid
        except Error as e:
            return e
        
    def actualizar_pan(self, id_pan, descr_pan):
        cursor = self.conexion.cursor()
        sql = "UPDATE panes SET descr_pan = %s WHERE id_pan = %s"
        cursor.execute(sql, (descr_pan, id_pan))
        self.conexion.commit()
        cursor.close()
        return cursor.rowcount
    
    def eliminar_pan(self, id_pan):
        cursor = self.conexion.cursor()
        sql = "DELETE FROM panes WHERE id_pan = %s"
        cursor.execute(sql, (id_pan,))
        self.conexion.commit()
        cursor.close()
        return cursor.rowcount