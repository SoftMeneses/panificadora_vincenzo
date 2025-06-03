import tkinter as tk
from tkinter import ttk

class InsumosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#EDE0D4")
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="Insumos", bg="#EDE0D4", fg="#6D3914", font=("Arial", 16, "bold")).pack(pady=(15, 10), padx=15, anchor="w")

        self.create_crud_bar()
        self.create_table()

    def create_crud_bar(self):
        crud_frame = tk.Frame(self, bg="#EDE0D4")
        crud_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        button_style = {"bg": "#8B4A1A", "fg": "#EDE0D4", "activebackground": "#B56A3A",
                        "font": ("Arial", 14, "bold"), "relief": tk.FLAT,
                        "padx": 25, "pady": 12, "bd": 0, "width": 12}

        for text in ["CONSULTAR", "AGREGAR", "ACTUALIZAR", "ELIMINAR"]:
            tk.Button(crud_frame, text=text, **button_style).pack(side=tk.LEFT, padx=(0, 10), ipady=5)

    def create_table(self):
        columns = ("id_insumo", "descr", "id_und_med", "exist_min", "exist_max", "stock")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=8)

        headings = [
            ("id_insumo", "ID Insumo"),
            ("descr", "Descripción"),
            ("id_und_med", "Unidad Medida"),
            ("exist_min", "Existencia Mínima"),
            ("exist_max", "Existencia Máxima"),
            ("stock", "Stock")
        ]

        for col, title in headings:
            tree.heading(col, text=title, anchor="center")
            tree.column(col, anchor="center", width=130)

        for _ in range(4):
            tree.insert("", "end", values=("", "", "", "", "", ""))

        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)