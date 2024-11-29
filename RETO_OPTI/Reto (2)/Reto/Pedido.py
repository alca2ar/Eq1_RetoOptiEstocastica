import datetime
from operator import attrgetter

class Pedido:
    def __init__(self, id_pedido, tipo_producto, cantidad_litros, fecha_entrega, importancia_cliente, fecha_ingreso):
        self.id_pedido = id_pedido
        self.tipo_producto = tipo_producto
        self.cantidad_litros = cantidad_litros
        self.fecha_entrega = datetime.datetime.strptime(fecha_entrega, '%Y-%m-%d %H:%M:%S')
        self.importancia_cliente = importancia_cliente
        self.fecha_ingreso = datetime.datetime.strptime(fecha_ingreso, '%Y-%m-%d %H:%M:%S.%f')
        self.prioridad = 0
        self.tiempo_total = 0
        self.tiempo_fin_etapa_previa = {'K1' : datetime.datetime.now()}  # Guardará los tiempos de fin por etapa
        self.fecha_entrega_real = None

    def calcular_prioridad(self):
        dias_restantes = (self.fecha_entrega - self.fecha_ingreso).days
        self.prioridad = 1 / self.importancia_cliente + 1 / dias_restantes if dias_restantes > 0 else float('inf')
        
    def pedido_a_tiempo(self):
        return self.fecha_entrega >= self.fecha_entrega_real
