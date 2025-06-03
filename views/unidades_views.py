import tkinter as tk
from tkinter import ttk

class UnidadesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EDE0D4")
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Unidades de Medida", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")
        self.create_crud_bar()
        self.create_table()

    def create_crud_bar(self):
        frame = tk.Frame(self, bg="#EDE0D4")
        frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        for text in ["CONSULTAR", "AGREGAR", "ACTUALIZAR", "ELIMINAR"]:
            tk.Button(frame, text=text, font=("Arial", 14, "bold"), bg="#8B4A1A",
                      fg="#EDE0D4", activebackground="#B56A3A", relief=tk.FLAT,
                      padx=25, pady=12, bd=0, width=12).pack(side=tk.LEFT, padx=(0, 10), ipady=5)

    def create_table(self):
        columns = ("id_unidad", "descripcion")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        tree.heading("id_unidad", text="ID Unidad", anchor="center")
        tree.heading("descripcion", text="Descripción", anchor="w")

        tree.column("id_unidad", anchor="center", width=150)
        tree.column("descripcion", anchor="w", width=400)

        for _ in range(4):
            tree.insert("", "end", values=("", ""))

        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
