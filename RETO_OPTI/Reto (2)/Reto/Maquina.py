from Pedido import Pedido
import datetime

class Maquina:
    def __init__(self, id_maquina, tipos_permitidos, etapa, matriz_setup, rates):
        self.id_maquina = id_maquina
        self.tipos_permitidos = tipos_permitidos
        self.etapa = etapa
        self.matriz_setup = matriz_setup
        self.rates = rates  # Diccionario: {producto: litros/hora}
        self.cola_pedidos = []
        self.ultimo_producto = None  # Último producto procesado en la máquina
        self.tiempo_disponible = datetime.datetime.now()  # Momento en que la máquina estará libre

    def asignar_pedido(self, pedido, etapa):
        if pedido.tipo_producto in self.tipos_permitidos:
            setup_time = self.obtener_tiempo_setup(pedido.tipo_producto)
            processing_time = self.obtener_tiempo_procesamiento(pedido.tipo_producto, pedido.cantidad_litros)
            tiempo_total_horas = setup_time + processing_time

            # Calcular fecha de inicio y fin
            fecha_inicio = max(self.tiempo_disponible, pedido.tiempo_fin_etapa_previa.get(list(pedido.tiempo_fin_etapa_previa.keys())[-1], datetime.datetime.min))
            # print(etapa)
            # print(pedido.tiempo_fin_etapa_previa)
            # print(pedido.tiempo_fin_etapa_previa.get(list(pedido.tiempo_fin_etapa_previa.keys())[-1], datetime.datetime.min))
            fecha_fin = fecha_inicio + datetime.timedelta(hours=tiempo_total_horas)
            if etapa == 'K3':
                pedido.fecha_entrega_real = fecha_fin

            # Actualizar la máquina
            self.ultimo_producto = pedido.tipo_producto
            self.tiempo_disponible = fecha_fin

            # Registrar en el pedido
            pedido.tiempo_total += tiempo_total_horas
            pedido.tiempo_fin_etapa_previa[etapa] = fecha_fin  # Registrar tiempo de fin de la etapa
            self.cola_pedidos.append((pedido, fecha_inicio, fecha_fin))
            return True
        return False

    def obtener_tiempo_setup(self, nuevo_producto):
        if self.ultimo_producto is None:
            return 0  # No hay tiempo de setup si la máquina está vacía
        if self.matriz_setup.get((self.ultimo_producto, nuevo_producto), 0) == 0:
            return 0
        return self.matriz_setup.get((self.ultimo_producto, nuevo_producto), 0) / 60.0  # Convertir a horas

    def obtener_tiempo_procesamiento(self, producto, cantidad_litros):
        rate = self.rates.get(producto, 0)
        if rate == 0:
            raise ValueError(f"La máquina {self.id_maquina} no puede procesar el producto {producto}.")
        return cantidad_litros / rate  # Tiempo en horas



