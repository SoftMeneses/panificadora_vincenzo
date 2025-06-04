import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class InsumosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EDE0D4")
        self.formulario_visible = False
        self.modo_formulario = None  # "agregar" o "actualizar"
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Insumos", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")
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

        for i in range(4):
            self.tree.insert("", "end", values=(f"INS00{i+1}", f"Desc {i+1}", "UND", 5, 10, 7))

        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def create_formulario(self):
        self.form_frame = tk.Frame(self, bg="#DCC9B6", bd=2, relief=tk.GROOVE)
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.form_frame.pack_forget()

        labels = ["ID Insumo", "Descripción", "Unidad de Medida", "Existencia Mínima", "Existencia Máxima", "Stock"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(self.form_frame, text=label_text, bg="#DCC9B6", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            entry = tk.Entry(self.form_frame, font=("Arial", 12), width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        self.boton_guardar = tk.Button(self.form_frame, text="Guardar", bg="#6D3914", fg="white",
                                       font=("Arial", 12, "bold"), padx=20, pady=5, command=self.guardar_formulario)
        self.boton_guardar.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def handle_crud(self, action):
        print(f"Botón {action} presionado en InsumosView")
        if action == "AGREGAR":
            self.modo_formulario = "agregar"
            self.limpiar_formulario()
            self.mostrar_formulario()
        elif action == "ACTUALIZAR":
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Debe seleccionar una fila para actualizar.")
                return
            self.modo_formulario = "actualizar"
            self.rellenar_formulario_con_fila(seleccion[0])
            self.mostrar_formulario()

    def mostrar_formulario(self):
        self.form_frame.pack(fill=tk.X, padx=15, pady=10)
        self.formulario_visible = True
        self.boton_guardar.config(text="Actualizar" if self.modo_formulario == "actualizar" else "Guardar")

    def ocultar_formulario(self):
        self.form_frame.pack_forget()
        self.formulario_visible = False

    def limpiar_formulario(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def rellenar_formulario_con_fila(self, item_id):
        valores = self.tree.item(item_id, "values")
        for (entry, valor) in zip(self.entries.values(), valores):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
        self.fila_seleccionada = item_id

    def guardar_formulario(self):
        datos = [entry.get() for entry in self.entries.values()]

        if self.modo_formulario == "agregar":
            self.tree.insert("", "end", values=datos)
        elif self.modo_formulario == "actualizar":
            self.tree.item(self.fila_seleccionada, values=datos)

        self.ocultar_formulario()
