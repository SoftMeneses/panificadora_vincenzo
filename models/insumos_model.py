from models.conexion import obtener_conexion
from mysql.connector import Error

class InsumoModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_insumos(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_ins, des_ins, des_uni AS id_uni, exi_min, exi_max, can_disp FROM insumos INNER JOIN unidades ON insumos.id_uni = unidades.id_uni ORDER BY id_ins")
        insumos = cursor.fetchall()
        cursor.close()
        return insumos
    
    def obtener_siguiente_id(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT MAX(id_ins) as max_id FROM insumos")
            resultado = cursor.fetchone()
            cursor.close()
            max_id = resultado[0] if resultado[0] is not None else 0
            return max_id + 1
        except Error as e:
            print(f"Error al obtener el siguiente ID de insumo: {e}")
            return None

    def insertar_insumo(self, id_ins, des_ins, id_uni, exi_min, exi_max, can_disp):
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO insumos (id_ins, des_ins, id_uni, exi_min, exi_max, can_disp) VALUES(%s,%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id_ins, des_ins, id_uni, exi_min, exi_max, can_disp))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid
        except Error as e:
            print(f"Error al insertar insumo: {e}")
            return None
    
    def actualizar_insumo(self, id_ins, des_ins, id_uni, exi_min, exi_max, can_disp):
        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE insumos SET des_ins = %s, id_uni = %s, exi_min = %s, exi_max = %s, can_disp = %s WHERE id_ins = %s"
            cursor.execute(sql, (des_ins, id_uni, exi_min, exi_max, can_disp, id_ins))
            self.conexion.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            return filas_afectadas
        except Error as e:
            print(f"Error al actualizar insumo: {e}")
            return 0
    
    def eliminar_insumo(self, id_ins):
        try:
            cursor = self.conexion.cursor()
            sql = "DELETE FROM insumos WHERE id_ins = %s"
            cursor.execute(sql, (id_ins,))
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
            cursor.execute("SELECT id_uni, des_uni FROM unidades") 
            unidades = cursor.fetchall()
            cursor.close()
            return unidades
        except Error as e:
            print(f"Error al obtener unidades de medida: {e}")
            return []
