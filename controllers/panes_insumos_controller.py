from models.panes_insumos_model import PanInsumoModelo

class PanesInsumosControlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = PanInsumoModelo()

    def cargar_panes_insumos(self):
        panes_insumos = self.modelo.obtener_panes_insumos()
        return panes_insumos

    def obtener_siguiente_id_registro(self):

        cursor = self.modelo.conexion.cursor()
        cursor.execute("SELECT MAX(id_panins) as max_id FROM panes_insumos")
        resultado = cursor.fetchone()
        cursor.close()
        max_id = resultado[0] if resultado[0] is not None else 0
        return max_id + 1

    def agregar_pan_insumo(self, id_pan, id_ins, can_ins, id_uni):

        nuevo_id = self.modelo.insertar_pan_insumo(id_pan, id_ins, can_ins, id_uni)
        if isinstance(nuevo_id, int):
            print(f"Pan-Insumo agregado con ID: {nuevo_id}")
            return True, None  
        else:
            print(f"Error al agregar Pan-Insumo: {nuevo_id}")
            return False, nuevo_id  
        
    def actualizar_pan_insumo(self, id_panins, id_pan, id_ins, can_ins, id_uni):
        try:
            id_panins = int(id_panins)
            id_pan = int(id_pan)
            id_ins = int(id_ins)
            id_uni = int(id_uni)
            can_ins = float(can_ins)
        except ValueError:
            return False, "Datos inválidos: asegúrate de que todos los campos numéricos estén correctamente llenados."

        filas_afectadas = self.modelo.actualizar_pan_insumo(id_panins, id_pan, id_ins, can_ins, id_uni)
        if filas_afectadas > 0:
            print(f"Pan-Insumo con ID {id_panins} actualizado.")
            return True, None 
        else:
            print("Error al actualizar el Pan-Insumo.")
            return False, "No se pudo actualizar el Pan-Insumo."


    '''
    def actualizar_pan_insumo(self, id_panins, id_pan, id_ins, can_ins, id_uni):  #FIXME este metodo es igual que el de arriba, sólo se especifica el tipo de dato
            
            filas_afectadas = self.modelo.actualizar_pan_insumo(id_panins, id_pan, id_ins, can_ins, id_uni)
            if filas_afectadas > 0:
                print(f"Pan-Insumo con ID {id_panins} actualizado.")
                return True, None 
            else:
                print("Error al actualizar el Pan-Insumo.")
                return False, "No se pudo actualizar el Pan-Insumo." 
    '''

    def eliminar_pan_insumo(self, id_panins):
        filas_afectadas = self.modelo.eliminar_pan_insumo(id_panins)
        if filas_afectadas > 0:
            print(f"Pan-Insumo con ID {id_panins} eliminado.")
            return True, None 
        else:
            print("Error al eliminar el Pan-Insumo.")
            return False, "No se pudo eliminar el Pan-Insumo." 


    def obtener_panes(self):
        return self.modelo.obtener_panes()

    def obtener_insumos(self):
        return self.modelo.obtener_insumos()

    def obtener_unidades(self):
        return self.modelo.obtener_unidades()
