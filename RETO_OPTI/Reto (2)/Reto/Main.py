
import tkinter as tk
from tkinter import filedialog, messagebox, ttk 
from Maquina import Maquina
from Pedido import Pedido
from Scheduler import Scheduler
import pandas as pd

class InterfazScheduler:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Interfaz Scheduler")
        self.ventana.geometry("600x400")

        # Botones para cargar archivos
        self.label_setup = tk.Label(ventana, text="Carga el archivo setup.csv:")
        self.label_setup.pack(pady=5)
        self.boton_setup = tk.Button(ventana, text="Cargar Setup", command=self.cargar_setup)
        self.boton_setup.pack(pady=5)
        
        self.label_maquinas = tk.Label(ventana, text="Carga el archivo maquinas.csv:")
        self.label_maquinas.pack(pady=5)
        self.boton_maquinas = tk.Button(ventana, text="Cargar Máquinas", command=self.cargar_maquinas)
        self.boton_maquinas.pack(pady=5)
        
        self.label_pedidos = tk.Label(ventana, text="Carga el archivo pedidos.csv:")
        self.label_pedidos.pack(pady=5)
        self.boton_pedidos = tk.Button(ventana, text="Cargar Pedidos", command=self.cargar_pedidos)
        self.boton_pedidos.pack(pady=5)

        # Botón para ejecutar scheduling
        self.boton_ejecutar = tk.Button(ventana, text="Ejecutar Scheduler", command=self.ejecutar_scheduler, bg="green", fg="white")
        self.boton_ejecutar.pack(pady=20)

        # Archivos cargados
        self.setup = None
        self.maquinas = None
        self.pedidos = None

        # Variable para almacenar los resultados generados
        self.resultados = ""

    def cargar_setup(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            try:
                self.setup = pd.read_csv(archivo)
                if self.setup.empty:
                    messagebox.showwarning("Advertencia", "El archivo setup.csv está vacío.")
                else:
                    messagebox.showinfo("Éxito", "Archivo setup.csv cargado correctamente.")
            except Exception as e:
                print(f"No se pudo cargar el archivo setup.csv: {e}")

    def cargar_maquinas(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            try:
                self.maquinas = pd.read_csv(archivo)
                if self.maquinas.empty:
                    messagebox.showwarning("Advertencia", "El archivo maquinas.csv está vacío.")
                else:
                    messagebox.showinfo("Éxito", "Archivo maquinas.csv cargado correctamente.")
            except Exception as e:
                print(f"No se pudo cargar el archivo maquinas.csv: {e}")

    def cargar_pedidos(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            try:
                self.pedidos = pd.read_csv(archivo)
                if self.pedidos.empty:
                    messagebox.showwarning("Advertencia", "El archivo pedidos.csv está vacío.")
                else:
                    messagebox.showinfo("Éxito", "Archivo pedidos.csv cargado correctamente.")
            except Exception as e:
                print(f"No se pudo cargar el archivo pedidos.csv: {e}")

    def ejecutar_scheduler(self):
        if self.setup is None or self.maquinas is None or self.pedidos is None:
            messagebox.showwarning("Advertencia", "Debes cargar todos los archivos antes de ejecutar.")
            print("Falta cargar archivos: ", self.setup, self.maquinas, self.pedidos)  # Depuración
            return

        try:
            # Crear instancia del Scheduler
            scheduler = Scheduler()

            # Procesar máquinas
            setups = {}
            maper = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
            for i in range(len(self.setup)):
                for j in range(len(self.setup)):
                    setups[(maper[i], maper[j])] = self.setup.iloc[i, j]

            for i in range(len(self.maquinas)):
                productos = [producto.strip() for producto in self.maquinas.loc[i, 'productos'].split(',')]
                rates = {productos[j]: int(self.maquinas.loc[i, 'rate'].split(',')[j]) for j in range(len(productos))}
                maquina = Maquina(self.maquinas.loc[i, 'maquina'], productos, self.maquinas.loc[i, 'stage'], setups, rates)
                scheduler.agregar_maquina(maquina)

            # Procesar pedidos
            for i in range(len(self.pedidos)):
                pedido = Pedido(
                    str(self.pedidos['Cliente ID'][i]),
                    self.pedidos['Producto'][i],
                    self.pedidos['Cantidad de litros'][i],
                    self.pedidos['Fecha de entrega'][i],
                    self.pedidos['Importancia de cliente'][i],
                    self.pedidos['Fecha de ingreso'][i]
                )
                scheduler.agregar_pedido(pedido)

            # Realizar scheduling
            scheduler.realizar_scheduling()

            # Capturar los resultados generados por el Scheduler
            tabla_scheduling = scheduler.generar_tabla_scheduling()

            # Mostrar los resultados en una nueva ventana
            self.mostrar_resultados(tabla_scheduling)
            pedidos_a_tiempo = scheduler.pedidos_a_tiempo()

            # Almacenar los resultados para mostrarlos y guardarlos
            self.resultados = f"Pedidos a tiempo: {pedidos_a_tiempo['a_tiempo']}\nPedidos atrasados: {pedidos_a_tiempo['atrasados']}"
            
            # Imprimir los resultados en la consola
            print(self.resultados)

        except Exception:
            # Si hay error, no mostrar nada ni en la interfaz ni en consola
            pass        

    def mostrar_resultados(self, tabla_scheduling):
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(self.ventana)
        ventana_resultados.title("Resultados del Scheduler")
        ventana_resultados.geometry("1000x400")

        # Crear un Treeview para mostrar la tabla de resultados
        tree = ttk.Treeview(ventana_resultados, columns=("ID","Maquina", "Etapa", "Pedido", "Producto", "Inicio", "Fin", "Cantidad"), show="headings")
        tree.pack(fill="both", expand=True)

        # Definir las columnas del Treeview
        tree.heading("ID", text="ID")
        tree.heading("Maquina", text="Maquina")
        tree.heading("Etapa", text="Etapa")
        tree.heading("Pedido", text="Pedido")
        tree.heading("Producto", text="Producto")
        tree.heading("Inicio", text="Inicio")
        tree.heading("Fin", text="Fin")
        tree.heading("Cantidad", text="Cantidad")

        # Agregar los datos fila por fila
        for row in tabla_scheduling:
            tree.insert("", "end", values=row)

        # Ajustar el ancho de las columnas
        for col in tree["columns"]:
            tree.column(col, width=150, anchor="center")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazScheduler(ventana)
    ventana.mainloop()

    
    
    