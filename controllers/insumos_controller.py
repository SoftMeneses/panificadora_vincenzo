from models.insumos_modelo import InsumoModelo

class InsumoControlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = InsumoModelo()

    def cargar_insumos(self):
        insumos = self.modelo.obtener_insumos()
        return insumos

    def obtener_siguiente_id_insumo(self):
        siguiente_id = self.modelo.obtener_siguiente_id()
        return siguiente_id

    def agregar_insumo(self, id_insumo,descr, id_und_med, exist_min, exist_max, stock):
        nuevo_id = self.modelo.insertar_insumo(id_insumo,descr, id_und_med, exist_min, exist_max, stock)
        if isinstance(nuevo_id, int):
            print(f"Insumo agregado con ID: {nuevo_id}")
            return True, None
        else:
            print(f"Error al agregar insumo: {nuevo_id}")
            return False, nuevo_id

    def actualizar_insumo(self, id_insumo, descr, id_und_med, exist_min, exist_max, stock):
        filas_afectadas = self.modelo.actualizar_insumo(id_insumo, descr, id_und_med, exist_min, exist_max, stock)
        if filas_afectadas > 0:
            print(f"Insumo con ID {id_insumo} actualizado.")
            return True, None
        else:
            print("Error al actualizar el insumo.")
            return False, "No se pudo actualizar el insumo."

    def eliminar_insumo(self, id_insumo):
        filas_afectadas = self.modelo.eliminar_insumo(id_insumo)
        if filas_afectadas > 0:
            print(f"Insumo con ID {id_insumo} eliminado.")
            return True, None
        else:
            print("Error al eliminar el insumo.")
            return False, "No se pudo eliminar el insumo."

    def obtener_unidades(self):
        return self.modelo.obtener_unidades()
