import tkinter as tk
from views.insumos_views import InsumosView
from views.panes_views import PanesView
from views.panesInsumos_views import PanesInsumosView
from views.unidades_views import UnidadesView
from controllers.unidades_controller import UnidadControlador 
from controllers.insumos_controller import InsumoControlador 
from controllers.panes_insumos_controller import PanesInsumosControlador  

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Panificadora Dulce Hogar")
        self.root.geometry("1000x600")
        self.root.configure(bg="#EDE0D4")

        self.setup_ui()

    def setup_ui(self):
        self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=0, bd=0, relief='flat', bg="#EDE0D4")
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_paned, width=200, bg="#6C3915")
        self.main_paned.add(self.sidebar)

        self.content_frame = tk.Frame(self.main_paned, bg="#EDE0D4")
        self.main_paned.add(self.content_frame)

        self.create_sidebar()
        self.load_view("insumos")

    def create_sidebar(self):
        tk.Label(self.sidebar, text="🍞 Menú Principal", bg="#8B4A1A", fg="#EDE0D4", font=("Arial", 18, "bold"), pady=15).pack(fill=tk.X, pady=(0, 20))

        buttons = [
            ("🥖 Insumos", lambda: self.load_view("insumos")),
            ("🥄 Unidades", lambda: self.load_view("unidades")),
            ("🥐 Panes", lambda: self.load_view("panes")),
            ("🡢 Panes Insumos", lambda: self.load_view("panesinsumos")),
            ("❌ Salir", self.root.quit)
        ]

        for text, command in buttons:
            tk.Button(self.sidebar, text=text, command=command,
                      bg="#6C3915", fg="#EDE0D4", activebackground="#B56A3A",
                      font=("Segoe UI Emoji", 14), anchor="w", padx=20, pady=10,
                      relief=tk.FLAT, bd=0).pack(fill=tk.X, pady=5)

    def load_view(self, view_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if view_name == "insumos":
            controlador = InsumoControlador(None)  
            vista = InsumosView(self.content_frame, controlador)
            controlador.vista = vista  
            vista.cargar_insumos() 
            vista.pack(fill=tk.BOTH, expand=True)

        elif view_name == "unidades":
            controlador = UnidadControlador(None)  
            vista = UnidadesView(self.content_frame, controlador)
            controlador.vista = vista  
            vista.cargar_unidades()  
            vista.pack(fill=tk.BOTH, expand=True)
            
        elif view_name == "panes":
            PanesView(self.content_frame).pack(fill=tk.BOTH, expand=True)

        elif view_name == "panesinsumos":
            controlador = PanesInsumosControlador(None)  
            vista = PanesInsumosView(self.content_frame, controlador)
            controlador.vista = vista  
            vista.cargar_panes_insumos() 
            vista.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
