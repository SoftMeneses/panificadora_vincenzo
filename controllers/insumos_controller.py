from models.insumos_model import InsumoModelo

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

    def agregar_insumo(self, id_ins, des_ins, id_uni, exi_min, exi_max, can_disp):
        nuevo_id = self.modelo.insertar_insumo(id_ins, des_ins, id_uni, exi_min, exi_max, can_disp)
        if isinstance(nuevo_id, int):
            print(f"Insumo agregado con ID: {nuevo_id}")
            return True, None
        else:
            print(f"Error al agregar insumo: {nuevo_id}")
            return False, nuevo_id

    def actualizar_insumo(self, id_ins, des_ins, id_uni, exi_min, exi_max, can_disp):
        filas_afectadas = self.modelo.actualizar_insumo(id_ins, des_ins, id_uni, exi_min, exi_max, can_disp)
        if filas_afectadas > 0:
            print(f"Insumo con ID {id_ins} actualizado.")
            return True, None
        else:
            print("Error al actualizar el insumo.")
            return False, "No se pudo actualizar el insumo."

    def eliminar_insumo(self, id_ins):
        filas_afectadas = self.modelo.eliminar_insumo(id_ins)
        if filas_afectadas > 0:
            print(f"Insumo con ID {id_ins} eliminado.")
            return True, None
        else:
            print("Error al eliminar el insumo.")
            return False, "No se pudo eliminar el insumo."

    def obtener_unidades(self):
        return self.modelo.obtener_unidades()
