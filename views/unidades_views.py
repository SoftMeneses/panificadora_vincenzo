import tkinter as tk
from tkinter import ttk, messagebox

class UnidadesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EDE0D4")
        self.form_frame = None
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Unidades de Medida", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")
        self.create_crud_bar()
        self.create_table()

    def create_crud_bar(self):
        frame = tk.Frame(self, bg="#EDE0D4")
        frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        for text in ["CONSULTAR", "AGREGAR", "ACTUALIZAR", "ELIMINAR"]:
            tk.Button(frame, text=text, command=lambda t=text: self.handle_crud(t),
                      font=("Arial", 14, "bold"), bg="#8B4A1A",
                      fg="#EDE0D4", activebackground="#B56A3A", relief=tk.FLAT,
                      padx=25, pady=12, bd=0, width=12).pack(side=tk.LEFT, padx=(0, 10), ipady=5)

    def create_table(self):
        columns = ("id_unidad", "descripcion")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        tree.heading("id_unidad", text="ID Unidad", anchor="center")
        tree.heading("descripcion", text="Descripción", anchor="w")

        tree.column("id_unidad", anchor="center", width=150)
        tree.column("descripcion", anchor="w", width=400)

        # Filas ejemplo
        example_data = [
            ("1", "Kilogramo"),
            ("2", "Unidad"),
            ("3", "Litro"),
            ("4", "Metro"),
        ]

        for item in example_data:
            tree.insert("", "end", values=item)

        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.tree = tree

    def handle_crud(self, action):
        if self.form_frame:
            self.form_frame.destroy()
            self.form_frame = None

        if action == "ACTUALIZAR":
            selected = self.tree.selection()
            if not selected:
                messagebox.showerror("Error", "Por favor, seleccione una fila para actualizar.")
                return
            values = self.tree.item(selected[0], "values")
            self.show_form(action, values)
        elif action == "AGREGAR":
            self.show_form(action)
        else:
            print(f"Botón {action} presionado en UnidadesView")

    def show_form(self, action, values=None):
        self.form_frame = tk.Frame(self, bg="#D6CCC2")
        self.form_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        fields = ["ID Unidad", "Descripción"]
        self.entries = {}

        for idx, label in enumerate(fields):
            tk.Label(self.form_frame, text=label, bg="#D6CCC2").grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(self.form_frame, width=50)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.entries[label] = entry
            if values:
                entry.insert(0, values[idx])

        tk.Button(self.form_frame, text=action, bg="#8B4A1A", fg="white", font=("Arial", 12, "bold"),
                  command=self.submit_form).grid(row=len(fields), columnspan=2, pady=10)

    def submit_form(self):
        data = {label: entry.get() for label, entry in self.entries.items()}
        print("Datos enviados:", data)
        # Aquí la lógica para guardar o actualizar
        self.form_frame.destroy()
        self.form_frame = None
