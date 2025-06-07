import tkinter as tk
from tkinter import ttk, messagebox
from controllers.panes_insumos_controller import PanesInsumosControlador 

class PanesInsumosView(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#EDE0D4")
        self.controlador = controlador
        self.formulario_visible = False
        self.modo_formulario = None  
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Panes - Insumos", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")
        self.create_crud_bar()
        self.create_table()
        self.tree.pack_forget()
        self.create_formulario()

    def create_crud_bar(self):
        crud_frame = tk.Frame(self, bg="#EDE0D4")
        crud_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        button_style = {
            "bg": "#8B4A1A", 
            "fg": "#EDE0D4", 
            "activebackground": "#B56A3A",
            "font": ("Arial", 14, "bold"), 
            "relief": tk.FLAT,
            "padx": 25, 
            "pady": 12, 
            "bd": 0, 
            "width": 12
        }

        for text in ["CONSULTAR", "AGREGAR", "ACTUALIZAR", "ELIMINAR"]:
            tk.Button(crud_frame, text=text, command=lambda t=text: self.handle_crud(t), **button_style).pack(side=tk.LEFT, padx=(0, 10), ipady=5)

    def create_table(self):
        columns = ("id_panins", "id_pan", "id_ins", "can_ins", "unidad")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headings = [
            ("id_panins", "ID Registro"),
            ("id_pan", "ID Pan"),
            ("id_ins", "ID Insumo"),
            ("can_ins", "Cantidad"),
            ("unidad", "Unidad de Medida")
        ]

        for col, title in headings:
            self.tree.heading(col, text=title, anchor="center")
            self.tree.column(col, anchor="center", width=130)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def create_formulario(self):
        self.form_frame = tk.Frame(self, bg="#D6CCC2", bd=2, relief=tk.GROOVE)
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.form_frame.pack_forget()  

        labels = ["ID Registro", "ID Pan", "ID Insumo", "Cantidad", "Unidad de Medida"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(self.form_frame, text=label_text, bg="#D6CCC2", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            if label_text in ["ID Pan", "ID Insumo", "Unidad de Medida"]:
                combo = ttk.Combobox(self.form_frame, font=("Arial", 12), width=37, state='readonly')
                combo.grid(row=i, column=1, padx=10, pady=5)
                self.entries[label_text] = combo
            else:
                entry = tk.Entry(self.form_frame, font=("Arial", 12), width=40)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries[label_text] = entry

        self.boton_guardar = tk.Button(self.form_frame, text="Guardar", bg="#6D3914", fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=5, command=self.guardar_formulario)
        self.boton_guardar.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.cargar_comboboxes()

    def cargar_comboboxes(self):
        panes = self.controlador.obtener_panes()
        insumos = self.controlador.obtener_insumos()
        unidades = self.controlador.obtener_unidades()

        self.entries["ID Pan"]["values"] = [f"{pan['id_pan']} - {pan['des_pan']}" for pan in panes]
        self.entries["ID Insumo"]["values"] = [f"{insumo['id_ins']} - {insumo['des_ins']}" for insumo in insumos]
        self.entries["Unidad de Medida"]["values"] = [f"{unidad['id_uni']} - {unidad['des_uni']}" for unidad in unidades]

    def handle_crud(self, action):
        self.ocultar_formulario()
        self.tree.pack_forget()

        if action == "CONSULTAR":
            self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        if action == "AGREGAR":
            self.modo_formulario = "agregar"
            self.limpiar_formulario()
            siguiente_id = self.controlador.obtener_siguiente_id_registro()
            if siguiente_id is not None:
                self.entries["ID Registro"].config(state='normal')
                self.entries["ID Registro"].delete(0, tk.END)
                self.entries["ID Registro"].insert(0, str(siguiente_id))
                self.entries["ID Registro"].config(state='readonly')
            self.mostrar_formulario()
        elif action == "ACTUALIZAR":
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Debe seleccionar una fila para actualizar.")
                return
            self.modo_formulario = "actualizar"
            self.rellenar_formulario_con_fila(seleccion[0])
            self.mostrar_formulario()
        elif action == "ELIMINAR":
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Debe seleccionar una fila para eliminar.")
                return
            values = self.tree.item(seleccion[0], "values")
            if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el registro con ID '{values[0]}'?"):
                success, error_message = self.controlador.eliminar_pan_insumo(values[0])
                if success:
                    messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
                    self.cargar_panes_insumos() 
                else:
                    messagebox.showerror("Error", error_message)

    def mostrar_formulario(self):
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.formulario_visible = True
        self.boton_guardar.config(text="Actualizar" if self.modo_formulario == "actualizar" else "Guardar")

    def ocultar_formulario(self):
        self.form_frame.pack_forget()
        self.formulario_visible = False

    def limpiar_formulario(self):
        for entry in self.entries.values():
            entry.config(state='normal')
            entry.delete(0, tk.END)

    def rellenar_formulario_con_fila(self, item_id):
        datos_completos = self.tree_data.get(item_id)
        if not datos_completos:
            messagebox.showerror("Error", "No se encontraron los datos completos del registro.")
            return

        # Rellenar los campos de texto
        self.entries["ID Registro"].config(state='normal')
        self.entries["ID Registro"].delete(0, tk.END)
        self.entries["ID Registro"].insert(0, str(datos_completos["id_panins"]))
        self.entries["ID Registro"].config(state='readonly')

        self.entries["Cantidad"].config(state='normal')
        self.entries["Cantidad"].delete(0, tk.END)
        self.entries["Cantidad"].insert(0, str(datos_completos["can_ins"]))

        # Establecer valores completos ("ID - Descripción") en los Combobox
        for key, label in [("id_pan", "ID Pan"), ("id_ins", "ID Insumo"), ("id_uni", "Unidad de Medida")]:
            full_value = datos_completos.get(key)
            if full_value and full_value in self.entries[label]["values"]:
                self.entries[label].set(full_value)
            else:
                # fallback por si no encuentra el full_value exacto
                self.entries[label].current(0)


    def guardar_formulario(self):
        datos = {label: entry.get().split(" - ")[0] if " - " in entry.get() else entry.get() for label, entry in self.entries.items()}
        print("Datos enviados:", datos)
        
        # Validación del campo Cantidad
        try:
            cantidad = float(datos["Cantidad"])
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido.")
            return
        if cantidad < 0:
            messagebox.showerror("Error", "La cantidad no puede ser negativa.")
            return
        if cantidad > 999999999999999999.99:
            messagebox.showerror("Error", "La cantidad excede el valor máximo permitido (999999999999999999.99).")
            return
        if round(cantidad, 2) != cantidad:
            messagebox.showerror("Error", "La cantidad no puede tener más de dos decimales.")
            return

        if self.modo_formulario == "agregar":
            success, error_message = self.controlador.agregar_pan_insumo(datos["ID Pan"], datos["ID Insumo"], datos["Cantidad"], datos["Unidad de Medida"])
            if success:
                messagebox.showinfo("Éxito", "Registro agregado con éxito.")
                self.cargar_panes_insumos()
            else:
                messagebox.showerror("Error", error_message)
        elif self.modo_formulario == "actualizar":
            success, error_message = self.controlador.actualizar_pan_insumo(datos["ID Registro"], datos["ID Pan"], datos["ID Insumo"], datos["Cantidad"], datos["Unidad de Medida"])
            if success:
                messagebox.showinfo("Éxito", "Registro actualizado con éxito.")
                self.cargar_panes_insumos()
            else:
                messagebox.showerror("Error", error_message)


        self.ocultar_formulario()

    def cargar_panes_insumos(self):
        self.tree.delete(*self.tree.get_children())
        panes_insumos = self.controlador.cargar_panes_insumos()
        self.tree_data = {}  # Diccionario para guardar datos completos con iid

        for i, registro in enumerate(panes_insumos):
            iid = f"item_{i}"
            # Extraer solo las descripciones para mostrar
            desc_pan = registro.get("id_pan").split(" - ")[1]
            desc_ins = registro.get("id_ins").split(" - ")[1]
            desc_uni = registro.get("id_uni").split(" - ")[1]

            # Guardar datos completos en el diccionario con iid
            self.tree_data[iid] = {
                "id_pan": registro.get("id_pan"),
                "id_ins": registro.get("id_ins"),
                "id_uni": registro.get("id_uni"),
                "id_panins": registro.get("id_panins"),
                "can_ins": registro.get("can_ins")
            }

            # Insertar en Treeview solo las descripciones
            self.tree.insert("", "end", iid=iid, values=(
                registro.get("id_panins"),
                desc_pan,
                desc_ins,
                registro.get("can_ins"),
                desc_uni
            ))


