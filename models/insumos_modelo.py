from models.conexion import obtener_conexion
from mysql.connector import Error

class InsumoModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_insumos(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM insumos")
        insumos = cursor.fetchall()
        cursor.close()
        return insumos
    
    def insertar_insumo(self, descr, id_und_med, exist_min, exist_max, stock):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO insumos (descr, id_und_med, exist_min, exist_max, stock) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (descr, id_und_med, exist_min, exist_max, stock))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid #Para evitar conflictos al hacer insert en cascada
        except Error as e:
            return e
    
    def actualizar_insumo(self, id_insumo, descr, id_und_med, exist_min, exist_max, stock):
        cursor = self.conexion.cursor()
        sql = "UPDATE insumos SET descr = %s, id_und_med = %s, exist_min = %s, exist_max = %s, stock = %s WHERE id_insumo = %s"
        cursor.execute(sql,(descr, id_und_med, exist_min, exist_max, stock, id_insumo))
        self.conexion.commit()
        cursor.close()
        return cursor.rowcount
    
    def eliminar_insumo(self, id_insumo):
        cursor = self.conexion.cursor()
        sql = "DELETE FROM insumos WHERE id_insumo = %s"
        cursor.execute(sql, (id_insumo,))
        self.conexion.commit()
        cursor.close()
        return cursor.rowcount