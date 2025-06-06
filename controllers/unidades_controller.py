from models.unidades_model import UnidadModelo

class UnidadControlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = UnidadModelo()

    def cargar_unidades(self):
        unidades = self.modelo.obtener_unidades()
        return unidades 

    def obtener_siguiente_id_unidad(self):
        siguiente_id = self.modelo.obtener_siguiente_id()
        return siguiente_id

    def agregar_unidad(self, id_uni, des_uni):
        nuevo_id = self.modelo.insertar_unidad(id_uni, des_uni)
        if isinstance(nuevo_id, int):
            print(f"Unidad agregada con ID: {nuevo_id}")
            return True, None
        else:
            print(f"Error al agregar unidad: {nuevo_id}")
            return False, nuevo_id

    def actualizar_unidad(self, id_uni, des_uni):
        filas_afectadas = self.modelo.actualizar_unidad(id_uni, des_uni)
        if filas_afectadas > 0:
            print(f"Unidad con ID {id_uni} actualizada.")
            return True, None
        else:
            print("Error al actualizar la unidad.")
            return False, "No se pudo actualizar la unidad."

    def eliminar_unidad(self, id_uni):
        filas_afectadas = self.modelo.eliminar_unidad(id_uni)
        if filas_afectadas > 0:
            print(f"Unidad con ID {id_uni} eliminada.")
            return True, None
        else:
            print("Error al eliminar la unidad.")
            return False, "No se pudo eliminar la unidad."
