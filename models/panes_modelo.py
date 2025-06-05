from models.conexion import obtener_conexion
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

    def obtener_siguiente_id(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT MAX(id_pan) as max_id FROM panes")
            resultado = cursor.fetchone()
            cursor.close()
            max_id = resultado[0] if resultado[0] is not None else 0
            return max_id + 1
        except Error as e:
            print(f"Error al obtener el siguiente ID: {e}")
            return None

    def insertar_pan(self, id_pan, descr_pan):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO panes (id_pan, descr_pan) VALUES(%s, %s)"
            cursor.execute(sql, (id_pan, descr_pan))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al insertar pan: {e}")
            return str(e)  

    def actualizar_pan(self, id_pan, descr_pan):
        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE panes SET descr_pan = %s WHERE id_pan = %s"
            cursor.execute(sql, (descr_pan, id_pan))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al actualizar pan: {e}")
            return 0  

    def eliminar_pan(self, id_pan):
        try:
            cursor = self.conexion.cursor()
            sql = "DELETE FROM panes WHERE id_pan = %s"
            cursor.execute(sql, (id_pan,))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al eliminar pan: {e}")
            return 0  