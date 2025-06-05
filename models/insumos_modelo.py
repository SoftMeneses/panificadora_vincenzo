from models.conexion import obtener_conexion
from mysql.connector import Error

class InsumoModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_insumos(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_insumo, descr , descr_und AS id_und_med, exist_min, exist_max, stock FROM insumos INNER JOIN unidades ON insumos.id_und_med = unidades.id_und_med ")
        insumos = cursor.fetchall()
        cursor.close()
        return insumos
    
    def obtener_siguiente_id(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT MAX(id_insumo) as max_id FROM insumos")
            resultado = cursor.fetchone()
            cursor.close()
            max_id = resultado[0] if resultado[0] is not None else 0
            return max_id + 1
        except Error as e:
            print(f"Error al obtener el siguiente ID de insumo: {e}")
            return None

    def insertar_insumo(self, id_insumo,descr, id_und_med, exist_min, exist_max, stock):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO insumos (id_insumo,descr, id_und_med, exist_min, exist_max, stock) VALUES(%s,%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_insumo,descr, id_und_med, exist_min, exist_max, stock))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al insertar insumo: {e}")
            return None
    
    def actualizar_insumo(self, id_insumo, descr, id_und_med, exist_min, exist_max, stock):
        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE insumos SET descr = %s, id_und_med = %s, exist_min = %s, exist_max = %s, stock = %s WHERE id_insumo = %s"
            cursor.execute(sql, (descr, id_und_med, exist_min, exist_max, stock, id_insumo))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al actualizar insumo: {e}")
            return 0
    
    def eliminar_insumo(self, id_insumo):
        try:
            cursor = self.conexion.cursor()
            sql = "DELETE FROM insumos WHERE id_insumo = %s"
            cursor.execute(sql, (id_insumo,))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al eliminar insumo: {e}")
            return 0

    def obtener_unidades(self):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_und_med, descr_und FROM unidades") 
            unidades = cursor.fetchall()
            cursor.close()
            return unidades
        except Error as e:
            print(f"Error al obtener unidades de medida: {e}")
            return []
