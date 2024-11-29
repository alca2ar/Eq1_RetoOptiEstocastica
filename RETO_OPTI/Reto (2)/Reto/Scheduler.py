from operator import attrgetter
import datetime
from Pedido import Pedido
from Maquina import Maquina
import pandas as pd

class Scheduler:
    def __init__(self):
        self.pedidos = []
        self.maquinas = {"K1": [], "K2": [], "K3": []}        

    def agregar_pedido(self, pedido):
        pedido.calcular_prioridad()
        self.pedidos.append(pedido)

    def agregar_maquina(self, maquina):
        self.maquinas[maquina.etapa].append(maquina)

    def realizar_scheduling(self):
    # Ordenar pedidos por prioridad descendente
        self.pedidos.sort(key=attrgetter('prioridad'), reverse=True)

        for etapa in sorted(self.maquinas.keys()):
            maquinas_etapa = self.maquinas[etapa]
            # print(f"\nScheduling para {etapa}:")
            for pedido in self.pedidos:
                asignado = False
                for maquina in maquinas_etapa:
                    if maquina.asignar_pedido(pedido, etapa):
                        asignado = True
                        break
                if not asignado:
                    print(f"Pedido {pedido.id_pedido} no pudo ser asignado en {etapa}.")

    def generar_tabla_scheduling(self):
    # Lista que almacenará las filas para la tabla
        tabla = []

        # Iterar sobre las máquinas y sus etapas
        for etapa, maquinas_etapa in self.maquinas.items():
            for maquina in maquinas_etapa:
                for pedido, fecha_inicio, fecha_fin in maquina.cola_pedidos:
                    # Agregar cada fila como una lista de valores
                    tabla.append([
                        pedido.id_pedido,
                        maquina.id_maquina,
                        etapa,
                        pedido.id_pedido,
                        pedido.tipo_producto,
                        fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                        fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
                        pedido.cantidad_litros
                    ])
        
        # Retornar la tabla completa
        return tabla

    def pedidos_a_tiempo(self):
        aTiempo = []
        delayed = []
        for pedido in self.pedidos:
            if pedido.pedido_a_tiempo():
                aTiempo.append(pedido.id_pedido)
            else:
                delayed.append(pedido.id_pedido)
            # aTiempo = pedido.pedido_a_tiempo()
        print('Pedidos a tiempo: ', aTiempo)
        print('\nPedidos atrasados: ', delayed)