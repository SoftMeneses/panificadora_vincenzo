from models.conexion import obtener_conexion
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

    def obtener_siguiente_id(self):
        try:
            
            cursor = self.conexion.cursor()
            cursor.execute("SELECT MAX(id_uni) as max_id FROM unidades")
            resultado = cursor.fetchone()
            cursor.close()
            max_id = resultado[0] if resultado[0] is not None else 0
            return max_id + 1
        except Error as e:
            print(f"Error al obtener el siguiente ID: {e}")
            return None

    def insertar_unidad(self, id_uni, des_uni):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO unidades (id_uni, des_uni) VALUES(%s,%s)"
            cursor.execute(sql, (id_uni, des_uni))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al insertar unidad: {e}")
            return None

    def actualizar_unidad(self, id_uni, des_uni):
        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE unidades SET des_uni = %s WHERE id_uni = %s"
            cursor.execute(sql, (des_uni, id_uni))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al actualizar unidad: {e}")
            return 0

    def eliminar_unidad(self, id_uni):
        try:
            cursor = self.conexion.cursor()
            sql = "DELETE FROM unidades WHERE id_uni = %s"
            cursor.execute(sql, (id_uni,))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al eliminar unidad: {e}")
            return 0
