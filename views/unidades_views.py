import tkinter as tk
from tkinter import ttk, messagebox

class UnidadesView(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#EDE0D4")
        self.controlador = controlador
        self.formulario_visible = False
        self.modo_formulario = None  
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Unidades de Medida", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")
        self.create_crud_bar()
        self.create_table()
        self.create_formulario()

    def create_crud_bar(self):
        crud_frame = tk.Frame(self, bg="#EDE0D4")
        crud_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        button_style = {"bg": "#8B4A1A", "fg": "#EDE0D4", "activebackground": "#B56A3A",
                        "font": ("Arial", 14, "bold"), "relief": tk.FLAT,
                        "padx": 25, "pady": 12, "bd": 0, "width": 12}

        for text in ["CONSULTAR", "AGREGAR", "ACTUALIZAR", "ELIMINAR"]:
            tk.Button(crud_frame, text=text, command=lambda t=text: self.handle_crud(t), **button_style).pack(side=tk.LEFT, padx=(0, 10), ipady=5)

    def create_table(self):
        columns = ("id_unidad", "descripcion")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headings = [
            ("id_unidad", "ID Unidad"),
            ("descripcion", "Descripción")
        ]

        for col, title in headings:
            self.tree.heading(col, text=title, anchor="center")
            self.tree.column(col, anchor="center", width=150 if col == "id_unidad" else 400)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def create_formulario(self):
        self.form_frame = tk.Frame(self, bg="#D6CCC2", bd=2, relief=tk.GROOVE)
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.form_frame.pack_forget() 

        labels = ["ID Unidad", "Descripción"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(self.form_frame, text=label_text, bg="#D6CCC2", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            entry = tk.Entry(self.form_frame, font=("Arial", 12), width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        self.boton_guardar = tk.Button(self.form_frame, text="Guardar", bg="#6D3914", fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=5, command=self.guardar_formulario)
        self.boton_guardar.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def handle_crud(self, action):
        if action == "AGREGAR":
            self.modo_formulario = "agregar"
            self.limpiar_formulario()
            siguiente_id = self.controlador.obtener_siguiente_id_unidad()
            if siguiente_id is not None:
                self.entries["ID Unidad"].config(state='normal')
                self.entries["ID Unidad"].delete(0, tk.END)
                self.entries["ID Unidad"].insert(0, str(siguiente_id))
                self.entries["ID Unidad"].config(state='readonly')
            else:
                self.entries["ID Unidad"].config(state='normal')
                self.entries["ID Unidad"].delete(0, tk.END)

            self.mostrar_formulario()
        elif action == "ACTUALIZAR":
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Debe seleccionar una fila para actualizar.")
                return
            self.modo_formulario = "actualizar"
            self.rellenar_formulario_con_fila(seleccion[0])
            self.entries["ID Unidad"].config(state='readonly') 
            self.mostrar_formulario()
        elif action == "ELIMINAR":
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Debe seleccionar una fila para eliminar.")
                return
            values = self.tree.item(seleccion[0], "values")
            if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar la unidad '{values[1]}'?"):
                success, error_message = self.controlador.eliminar_unidad(values[0])
                if success:
                    messagebox.showinfo("Éxito", "Unidad eliminada con éxito.")
                    self.cargar_unidades() 
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
        valores = self.tree.item(item_id, "values")
        for (entry, valor) in zip(self.entries.values(), valores):
            entry.config(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, valor)
        self.fila_seleccionada = item_id

    def guardar_formulario(self):
        datos = [entry.get() for entry in self.entries.values()]

        if self.modo_formulario == "agregar":
            id_unidad = datos[0]
            descripcion = datos[1]
            success, error_message = self.controlador.agregar_unidad(id_unidad, descripcion)
            if success:
                messagebox.showinfo("Éxito", "Unidad agregada con éxito.")
                self.cargar_unidades()
            else:
                messagebox.showerror("Error", error_message)
                
        elif self.modo_formulario == "actualizar":
            success, error_message = self.controlador.actualizar_unidad(self.entries["ID Unidad"].get(), datos[1])
            if success:
                messagebox.showinfo("Éxito", "Unidad actualizada con éxito.")
                self.cargar_unidades()
            else:
                messagebox.showerror("Error", error_message)

        self.ocultar_formulario()

    def cargar_unidades(self):
        self.tree.delete(*self.tree.get_children()) 
        unidades = self.controlador.cargar_unidades()
        for unidad in unidades:
            self.tree.insert("", "end", values=(unidad["id_und_med"], unidad["descr_und"]))
