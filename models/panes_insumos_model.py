from models.conexion import obtener_conexion
from mysql.connector import Error

class PanInsumoModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_panes_insumos(self):

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_panins,CONCAT(panes_insumos.id_pan,' - ',des_pan) AS id_pan, CONCAT(insumos.id_ins,' - ', des_ins) AS id_ins, can_ins, CONCAT(unidades.id_uni,' - ',des_uni) AS id_uni FROM panes_insumos INNER JOIN panes ON panes_insumos.ID_PAN = PANES.id_pan INNER JOIN INSUMOS ON insumos.id_ins = panes_insumos.id_ins INNER JOIN unidades ON unidades.id_uni = panes_insumos.id_uni ORDER BY ID_PANINS")
        panes_insumos = cursor.fetchall()
        cursor.close()
        return panes_insumos
    
    def insertar_pan_insumo(self,id_panins, id_pan, id_ins, can_ins, id_uni):
    
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO panes_insumos (id_panins,id_pan, id_ins, can_ins, id_uni) VALUES(%s,%s, %s, %s, %s)"
            cursor.execute(sql, (id_panins,id_pan, id_ins, can_ins, id_uni))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid 
        except Error as e:
            return str(e)  
        
    def actualizar_pan_insumo(self, id_panins, id_pan, id_ins, can_ins, id_uni):
       
        cursor = self.conexion.cursor()
        sql = "UPDATE panes_insumos SET id_pan = %s, id_ins = %s, can_ins = %s, id_uni = %s WHERE id_panins = %s"
        cursor.execute(sql, (id_pan, id_ins, can_ins, id_uni, id_panins))
        self.conexion.commit()
        filas_afectadas = cursor.rowcount 
        cursor.close()
        return filas_afectadas  

    def eliminar_pan_insumo(self, id_panins):
      
        cursor = self.conexion.cursor()
        sql = "DELETE FROM panes_insumos WHERE id_panins = %s"
        cursor.execute(sql, (id_panins,))
        self.conexion.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        return filas_afectadas


    def obtener_panes(self):

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_pan, des_pan FROM panes")  
        panes = cursor.fetchall()
        cursor.close()
        return panes

    def obtener_insumos(self):

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_ins, des_ins FROM insumos")  
        insumos = cursor.fetchall()
        cursor.close()
        return insumos

    def obtener_unidades(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_uni, des_uni FROM unidades") 
        unidades = cursor.fetchall()
        cursor.close()
        return unidades
