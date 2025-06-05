from models.conexion import obtener_conexion
from mysql.connector import Error

class PanInsumoModelo:
    def __init__(self):
        self.conexion = obtener_conexion()

    def obtener_panes_insumos(self):

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_registro,descr_pan AS id_pan,descr AS id_insumo,cant_insumo,descr_und AS id_und_med FROM panes_insumos INNER JOIN panes ON panes_insumos.ID_PAN = PANES.id_pan INNER JOIN INSUMOS ON insumos.id_insumo = panes_insumos.id_insumo INNER JOIN unidades ON unidades.id_und_med = panes_insumos.id_und_med")
        panes_insumos = cursor.fetchall()
        cursor.close()
        return panes_insumos
    
    def insertar_pan_insumo(self, id_pan, id_insumo, cant_insumo, id_und_med):
    
        try:
            cursor = self.conexion.cursor()
            sql = "INSERT INTO panes_insumos (id_pan, id_insumo, cant_insumo, id_und_med) VALUES(%s, %s, %s, %s)"
            cursor.execute(sql, (id_pan, id_insumo, cant_insumo, id_und_med))
            self.conexion.commit()
            cursor.close()
            return cursor.lastrowid 
        except Error as e:
            return str(e)  
        
    def actualizar_pan_insumo(self, id_registro, id_pan, id_insumo, cant_insumo, id_und_med):
       
        cursor = self.conexion.cursor()
        sql = "UPDATE panes_insumos SET id_pan = %s, id_insumo = %s, cant_insumo = %s, id_und_med = %s WHERE id_registro = %s"
        cursor.execute(sql, (id_pan, id_insumo, cant_insumo, id_und_med, id_registro))
        self.conexion.commit()
        filas_afectadas = cursor.rowcount 
        cursor.close()
        return filas_afectadas  

    def eliminar_pan_insumo(self, id_registro):
      
        cursor = self.conexion.cursor()
        sql = "DELETE FROM panes_insumos WHERE id_registro = %s"
        cursor.execute(sql, (id_registro,))
        self.conexion.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        return filas_afectadas


    def obtener_panes(self):

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_pan, descr_pan FROM panes")  
        panes = cursor.fetchall()
        cursor.close()
        return panes

    def obtener_insumos(self):

        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_insumo, descr FROM insumos")  
        insumos = cursor.fetchall()
        cursor.close()
        return insumos

    def obtener_unidades(self):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_und_med, descr_und FROM unidades") 
        unidades = cursor.fetchall()
        cursor.close()
        return unidades
