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
        self.tree.pack_forget()  # pack_forget() para ocultar la tabla
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
        columns = ("id_ins", "des_ins", "id_uni", "exi_min", "exi_max", "can_disp")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headings = [
            ("id_ins", "ID Insumo"),
            ("des_ins", "Descripción"),
            ("id_uni", "Unidad Medida"),
            ("exi_min", "Existencia Mínima"),
            ("exi_max", "Existencia Máxima"),
            ("can_disp", "Cantidad Disponible")
        ]

        for col, title in headings:
            self.tree.heading(col, text=title, anchor="center")
            self.tree.column(col, anchor="center", width=130)


    def create_formulario(self):
        self.form_frame = tk.Frame(self, bg="#DCC9B6", bd=2, relief=tk.GROOVE)
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.form_frame.pack_forget()

        labels = ["ID Insumo", "Descripción", "Unidad de Medida", "Existencia Mínima", "Existencia Máxima", "Cantidad Disponible"]
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
        self.unidades_dict = {u['des_uni']: u['id_uni'] for u in unidades}
        self.combo_und_med['values'] = list(self.unidades_dict.keys())
        if self.combo_und_med['values']:
            self.combo_und_med.current(0)

    def handle_crud(self, action):
        self.ocultar_formulario()
        self.tree.pack_forget()

        if action == "CONSULTAR":
            self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        elif action == "AGREGAR":
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
        
        id_uni = valores[2]
        des_uni = None
        for des_ins, id_u in self.unidades_dict.items():
            if id_u == id_uni:
                des_uni = des_ins
                break
        if des_uni and des_uni in self.combo_und_med['values']:
            self.combo_und_med.set(des_uni)
        else:
            if self.combo_und_med['values']:
                self.combo_und_med.current(0)

        self.fila_seleccionada = item_id

    def guardar_formulario(self):
        id_ins = self.entries["ID Insumo"].get()
        des_ins = self.entries["Descripción"].get()
        und_descr = self.combo_und_med.get()
        id_uni = self.unidades_dict.get(und_descr, None)
        exi_min = self.entries["Existencia Mínima"].get()
        exi_max = self.entries["Existencia Máxima"].get()
        can_disp = self.entries["Cantidad Disponible"].get()

        # Validación del campo ID Insumo
        if not id_ins.strip():
            messagebox.showerror("Error", "El ID de insumo no puede estar vacío.")
            return
        if not id_ins.isdigit():
            messagebox.showerror("Error", "El ID de insumo debe ser un número entero positivo.")
            return
        id_ins_int = int(id_ins)
        if not (0 <= id_ins_int <= 4294967295):
            messagebox.showerror("Error", "El ID de insumo debe estar entre 0 y 4294967295.")
            return

        # Validación del campo Descripcion
        if not des_ins.strip():
            messagebox.showerror("Error", "La descripción no puede estar vacía.")
            return
        if not all(c.isalpha() or c.isspace() for c in des_ins):
            messagebox.showerror("Error", "La descripción debe contener solo letras y espacios.")
            return
        if len(des_ins) > 50:
            messagebox.showerror("Error", "La descripción no debe exceder los 50 caracteres.")
            return

        # Validación del campo Unidad de Medida
        if id_uni is None:
            messagebox.showerror("Error", "Seleccione una Unidad de Medida válida.")
            return
        
        # Validación del campo Existencia Mínima
        if not exi_min.strip():
            messagebox.showerror("Error", "La existencia mínima no puede estar vacía.")
            return
        if not exi_min.isdigit():
            messagebox.showerror("Error", "La existencia mínima debe ser un número entero positivo.")
            return
        if int(exi_min) > int(exi_max):
            messagebox.showerror("Error", "La existencia mínima debe ser menor o igual a la existencia máxima.")
            return
        exi_min_int = int(exi_min)
        if not (0 <= exi_min_int <= 65535):
            messagebox.showerror("Error", "La existencia mínima debe estar entre 0 y 65535.")
            return

        # Validación del campo Existencia Maxima
        if not exi_max.strip():
            messagebox.showerror("Error", "La existencia máxima no puede estar vacía.")
            return
        if not exi_max.isdigit():
            messagebox.showerror("Error", "La existencia máxima debe ser un número entero positivo.")
            return
        if int(exi_max) < int(exi_min):
            messagebox.showerror("Error", "La existencia máxima debe ser mayor o igual a la existencia mínima.")
            return
        exi_max_int = int(exi_max)
        if not (0 <= exi_max_int <= 65535):
            messagebox.showerror("Error", "La existencia máxima debe estar entre 0 y 65535.")
            return

        # Validación del campo Cantidad Disponible
        if not can_disp.strip():
            messagebox.showerror("Error", "La cantidad disponible no puede estar vacía.")
            return
        if not can_disp.isdigit():
            messagebox.showerror("Error", "La cantidad disponible debe ser un número positivo.")
            return
        if int(can_disp) < int(exi_min):
            messagebox.showerror("Error", "La cantidad disponible debe ser mayor o igual a la existencia mínima.")
            return
        if int(can_disp) > int(exi_max):
            messagebox.showerror("Error", "La cantidad disponible debe ser menor o igual a la existencia máxima.")
            return

        if self.modo_formulario == "agregar":
            success, error_message = self.controlador.agregar_insumo(id_ins, des_ins, id_uni, exi_min, exi_max, can_disp)
            if success:
                messagebox.showinfo("Éxito", "Insumo agregado con éxito.")
                self.cargar_insumos()
            else:
                messagebox.showerror("Error", error_message)
        elif self.modo_formulario == "actualizar":
            success, error_message = self.controlador.actualizar_insumo(id_ins, des_ins, id_uni, exi_min, exi_max, can_disp)
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
                insumo["id_ins"], insumo["des_ins"],
                insumo["id_uni"], insumo["exi_min"],
                insumo["exi_max"], insumo["can_disp"]))
