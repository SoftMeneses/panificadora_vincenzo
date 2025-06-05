import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controllers.insumos_controller import InsumoControlador

class InsumosView(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#EDE0D4")
        self.controlador = controlador
        self.formulario_visible = False
        self.modo_formulario = None  
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Insumos", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")
        self.create_crud_bar()
        self.create_table()
        self.create_formulario()
        self.cargar_insumos()  
        self.cargar_unidades()

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
        columns = ("id_insumo", "descr", "id_und_med", "exist_min", "exist_max", "stock")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headings = [
            ("id_insumo", "ID Insumo"),
            ("descr", "Descripción"),
            ("id_und_med", "Unidad Medida"),
            ("exist_min", "Existencia Mínima"),
            ("exist_max", "Existencia Máxima"),
            ("stock", "Stock")
        ]

        for col, title in headings:
            self.tree.heading(col, text=title, anchor="center")
            self.tree.column(col, anchor="center", width=130)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def create_formulario(self):
        self.form_frame = tk.Frame(self, bg="#DCC9B6", bd=2, relief=tk.GROOVE)
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.form_frame.pack_forget()

        labels = ["ID Insumo", "Descripción", "Unidad de Medida", "Existencia Mínima", "Existencia Máxima", "Stock"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(self.form_frame, text=label_text, bg="#DCC9B6", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            if label_text == "Unidad de Medida":
                self.combo_und_med = ttk.Combobox(self.form_frame, font=("Arial", 12), width=37, state='readonly')
                self.combo_und_med.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(self.form_frame, font=("Arial", 12), width=40)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries[label_text] = entry

        self.boton_guardar = tk.Button(self.form_frame, text="Guardar", bg="#6D3914", fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=5, command=self.guardar_formulario)
        self.boton_guardar.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def cargar_unidades(self):
        unidades = self.controlador.obtener_unidades()
        self.unidades_dict = {u['descr_und']: u['id_und_med'] for u in unidades}
        self.combo_und_med['values'] = list(self.unidades_dict.keys())
        if self.combo_und_med['values']:
            self.combo_und_med.current(0)

    def handle_crud(self, action):
        if action == "AGREGAR":
            self.modo_formulario = "agregar"
            self.limpiar_formulario()
            siguiente_id = self.controlador.obtener_siguiente_id_insumo()
            if siguiente_id is not None:
                self.entries["ID Insumo"].config(state='normal')
                self.entries["ID Insumo"].delete(0, tk.END)
                self.entries["ID Insumo"].insert(0, str(siguiente_id))
                self.entries["ID Insumo"].config(state='readonly')
            if self.combo_und_med['values']:
                self.combo_und_med.current(0)
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
            if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el insumo '{values[1]}'?"):
                success, error_message = self.controlador.eliminar_insumo(values[0])
                if success:
                    messagebox.showinfo("Éxito", "Insumo eliminado con éxito.")
                    self.cargar_insumos()
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
        if self.combo_und_med['values']:
            self.combo_und_med.current(0)

    def rellenar_formulario_con_fila(self, item_id):
        valores = self.tree.item(item_id, "values")

        for (entry, valor) in zip(self.entries.values(), [valores[0], valores[1], valores[3], valores[4], valores[5]]):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, valor)
        
        id_und_med = valores[2]
        descr_und = None
        for descr, id_u in self.unidades_dict.items():
            if id_u == id_und_med:
                descr_und = descr
                break
        if descr_und and descr_und in self.combo_und_med['values']:
            self.combo_und_med.set(descr_und)
        else:
            if self.combo_und_med['values']:
                self.combo_und_med.current(0)

        self.fila_seleccionada = item_id

    def guardar_formulario(self):
        id_insumo = self.entries["ID Insumo"].get()
        descr = self.entries["Descripción"].get()
        und_descr = self.combo_und_med.get()
        id_und_med = self.unidades_dict.get(und_descr, None)
        exist_min = self.entries["Existencia Mínima"].get()
        exist_max = self.entries["Existencia Máxima"].get()
        stock = self.entries["Stock"].get()

        if id_und_med is None:
            messagebox.showerror("Error", "Seleccione una Unidad de Medida válida.")
            return

        if self.modo_formulario == "agregar":
            success, error_message = self.controlador.agregar_insumo(id_insumodescr, id_und_med, exist_min, exist_max, stock)
            if success:
                messagebox.showinfo("Éxito", "Insumo agregado con éxito.")
                self.cargar_insumos()
            else:
                messagebox.showerror("Error", error_message)
        elif self.modo_formulario == "actualizar":
            success, error_message = self.controlador.actualizar_insumo(id_insumo, descr, id_und_med, exist_min, exist_max, stock)
            if success:
                messagebox.showinfo("Éxito", "Insumo actualizado con éxito.")
                self.cargar_insumos()
            else:
                messagebox.showerror("Error", error_message)

        self.ocultar_formulario()

    def cargar_insumos(self):
        self.tree.delete(*self.tree.get_children())
        insumos = self.controlador.cargar_insumos()
        for insumo in insumos:
            self.tree.insert("", "end", values=(
                insumo["id_insumo"], insumo["descr"],
                insumo["id_und_med"], insumo["exist_min"],
                insumo["exist_max"], insumo["stock"]))
