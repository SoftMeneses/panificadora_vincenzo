import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.insumos_modelo import InsumoModelo

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Panificadora")
        self.root.geometry("800x500")
        self.setup_ui()
        self.insumo_modelo = InsumoModelo()

    def consultar_insumos(self):
        insumos = self.insumo_modelo.obtener_insumos()
    
        # Limpiar la tabla
        for item in self.tree_insumos.get_children():
            self.tree_insumos.delete(item)
        
        # Insertar datos reales
        for insumo in insumos:
            self.tree_insumos.insert("", "end", values=(
                insumo["id_insumo"],
                insumo["descr"],
                insumo["id_und_med"],
                insumo["exist_min"],
                insumo["exist_max"],
                insumo["stock"]
            ))
    
    def insertar_insumo(self):
        ventana_insertar = tk.Toplevel(self.root)
        ventana_insertar.title("Insertar Insumo")
        ventana_insertar.geometry("400x400")
    
        campos = {
            "Descripción": tk.StringVar(),
            "Unidad de Medida": tk.StringVar(),
            "Existencia Mínima": tk.StringVar(),
            "Existencia Máxima": tk.StringVar(),
            "Stock": tk.StringVar()
        }
    
        for i, (label, var) in enumerate(campos.items()):
            tk.Label(ventana_insertar, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            tk.Entry(ventana_insertar, textvariable=var).grid(row=i, column=1, padx=10, pady=5)
    
        def guardar_insumo():
            self.insumo_modelo.insertar_insumo(
            campos["Descripción"].get(),
            campos["Unidad de Medida"].get(),
            int(campos["Existencia Mínima"].get()),
            int(campos["Existencia Máxima"].get()),
            int(campos["Stock"].get())
        )

            ventana_insertar.destroy()
            self.consultar_insumos()
    
        tk.Button(ventana_insertar, text="Guardar", command=guardar_insumo, bg="#2980b9", fg="white").grid(row=len(campos), column=0, columnspan=2, pady=20)

    
    def actualizar_insumo(self):
        item_seleccionado = self.tree_insumos.focus()
        if not item_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un insumo para actualizar.")
            return

        datos = self.tree_insumos.item(item_seleccionado, "values")

        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Insumo")
        ventana.geometry("400x400")

        etiquetas = [
            "ID", "Descripción", "Unidad de Medida",
            "Existencia Mínima", "Existencia Máxima", "Stock"
        ]
        campos = {}

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(ventana, text=etiqueta).grid(row=i, column=0, pady=5, padx=10, sticky="w")
            entry = tk.Entry(ventana)
            entry.grid(row=i, column=1, pady=5, padx=10)
            entry.insert(0, datos[i])
            if etiqueta == "ID":
                entry.config(state="disabled")  # ID no editable
            campos[etiqueta] = entry

        btn_guardar = tk.Button(
            ventana,
            text="Guardar Cambios",
            command=lambda: self.guardar_cambios_insumo(campos, ventana),
            bg="#2980b9",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        btn_guardar.grid(row=len(etiquetas), columnspan=2, pady=15)

    def guardar_cambios_insumo(self, campos, ventana):
        id_insumo = campos["ID"].get()
        descr = campos["Descripción"].get()
        id_und_med = campos["Unidad de Medida"].get()
        exist_min = campos["Existencia Mínima"].get()
        exist_max = campos["Existencia Máxima"].get()
        stock = campos["Stock"].get()

        try:
            exist_min = int(exist_min)
            exist_max = int(exist_max)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Los valores de existencia y stock deben ser numéricos.")
            return

        self.insumo_modelo.actualizar_insumo(
            id_insumo, descr, id_und_med, exist_min, exist_max, stock
        )

        ventana.destroy()
        self.consultar_insumos()
        messagebox.showinfo("Éxito", "Insumo actualizado correctamente.")
    
    def eliminar_insumo(self):
        selected_item = self.tree_insumos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un insumo para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este insumo?")
        if not respuesta:
            return

        item = self.tree_insumos.item(selected_item)
        id_insumo = item["values"][0]

        try:
            self.insumo_modelo.eliminar_insumo(id_insumo)
            self.consultar_insumos()
            messagebox.showinfo("Éxito", "Insumo eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el insumo:\n{e}")

        
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
            text="Insumos",
            bg="#f0f0f0",
            fg="#333333",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")
    
        # Contenedor de botones
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(padx=10, pady=(0, 10), anchor="w")
    
        botones = [
            ("Consultar", self.consultar_insumos),
            ("Insertar", self.insertar_insumo),
            ("Actualizar", self.actualizar_insumo),
            ("Eliminar", self.eliminar_insumo),
        ]
    
        for texto, comando in botones:
            btn = tk.Button(
                btn_frame,
                text=texto,
                command=comando,
                bg="#2980b9",
                fg="white",
                font=("Arial", 10),
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
    
        self.create_table(parent)

        
    def create_table(self, parent):
        columns = ("id_insumo", "descr", "id_und_med", "exist_min", "exist_max", "stock")
    
        self.tree_insumos = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=10
        )
    
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
    
        for col in columns:
            self.tree_insumos.heading(col, text=col.replace("_", " ").title(), anchor="center")
            self.tree_insumos.column(col, width=130, anchor="center")
    
        self.tree_insumos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
