import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Panificadora")
        self.root.geometry("900x500")
        self.setup_ui()
        
    def setup_ui(self):
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        sidebar = tk.Frame(main_paned, width=200, bg="#34495e")
        main_paned.add(sidebar)
        self.create_sidebar(sidebar)
        
        content_frame = tk.Frame(main_paned, bg="#f0f0f0")
        main_paned.add(content_frame)
        self.create_content(content_frame)
        
    def create_sidebar(self, parent):
        tk.Label(
            parent,
            text="Menú Principal",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=10
        ).pack(fill=tk.X, pady=(10, 15))
        
        menu_buttons = [
            ("Gestión de Insumos", None),
            ("Unidades de Medida", None), 
            ("Tipos de Panes", None),
            ("Panes Insumos", None),
            ("Salir", self.root.quit)
        ]
        
        for text, command in menu_buttons:
            btn = tk.Button(
                parent,
                text=text,
                bg="#2980b9",
                fg="white",
                activebackground="#3498db",
                activeforeground="white",
                relief=tk.FLAT,
                font=("Arial", 10),
                anchor="w",
                command=command,
                padx=15
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
    
    def create_content(self, parent):
        tk.Label(
            parent, 
            text="Panes Insumos",  # Título actualizado
            bg="#f0f0f0",
            fg="#333333",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")
        
        tk.Label(
            parent, 
            text="Registro de insumos por pan",  # Subtítulo actualizado
            bg="#f0f0f0",
            fg="#555555",
            font=("Arial", 11)
        ).pack(pady=(0, 10), padx=10, anchor="w")
        
        self.create_table(parent)
        
    def create_table(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview",
                      background="#ffffff",
                      foreground="#000000",
                      fieldbackground="#ffffff",
                      bordercolor="#cccccc",
                      font=("Arial", 10),
                      rowheight=25)
                      
        style.configure("Treeview.Heading",
                     background="#e1e1e1",
                     foreground="#000000",
                     font=("Arial", 10, "bold"),
                     padding=5)
        
        style.map("Treeview", background=[], foreground=[])
        
        # COLUMNAS PARA PANES INSUMOS
        columns = ("id_registro", "id_pan", "id_insumo", "cant_insumo", "id_und_med")
        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=5
        )
        
        tree.heading("id_registro", text="ID Registro", anchor="center")
        tree.heading("id_pan", text="ID Pan", anchor="center")
        tree.heading("id_insumo", text="ID Insumo", anchor="center")
        tree.heading("cant_insumo", text="Cantidad", anchor="center")
        tree.heading("id_und_med", text="Unidad de Medida", anchor="center")
        
        tree.column("id_registro", width=100, anchor="center")
        tree.column("id_pan", width=100, anchor="center")
        tree.column("id_insumo", width=100, anchor="center")
        tree.column("cant_insumo", width=100, anchor="center")
        tree.column("id_und_med", width=150, anchor="center")
        
        for _ in range(4):
            tree.insert("", "end", values=("", "", "", "", ""))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
