from models.panes_modelo import PanModelo

class PanControlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = PanModelo()

    def cargar_panes(self):
        panes = self.modelo.obtener_panes()
        self.vista.cargar_panes(panes)

    def obtener_siguiente_id_pan(self):
        return self.modelo.obtener_siguiente_id()  

    def agregar_pan(self, id_pan, descr_pan):
            nuevo_id = self.modelo.insertar_pan(id_pan, descr_pan)
            if isinstance(nuevo_id, int):
                print(f"Pan agregado con ID: {nuevo_id}")
                return True, None
            else:
                print(f"Error al agregar pan: {nuevo_id}")
                return False, nuevo_id

    def actualizar_pan(self, id_pan, descr_pan):
        try:
            filas_afectadas = self.modelo.actualizar_pan(id_pan, descr_pan)
            print(f"Filas afectadas al actualizar: {filas_afectadas}")
            
            if filas_afectadas >= 0:
                print(f"Pan con ID {id_pan} actualizado o sin cambios.")
                self.cargar_panes()
                return True, None
            else:
                print("Error al actualizar el pan.")
                return False, "No se pudo actualizar el pan."
        except Exception as e:
            print(f"Excepción al actualizar pan: {e}")
            return False, str(e)

    def eliminar_pan(self, id_pan):
        try:
            filas_afectadas = self.modelo.eliminar_pan(id_pan)
            if filas_afectadas > 0:
                print(f"Pan con ID {id_pan} eliminado.")
                self.cargar_panes()
                return True, None
            else:
                print("Error al eliminar el pan.")
                return False, "No se pudo eliminar el pan."
        except Exception as e:
            print(f"Excepción al eliminar pan: {e}")
            return False, str(e)
