# estaciones/estacion_entrega.py
from estaciones.estacion import Estacion

class EstacionEntrega(Estacion):
    def __init__(self, recetas_activas):
        super().__init__(nombre="Estación de Entrega")
        self.recetas_activas = recetas_activas    # referencia a la lista de la cocina
    
    def interactuar(self, chef):
        if chef.ingrediente_en_mano is None:
            print("No tienes nada para entregar.")
            return
        
        # Por ahora el chef entrega de a un ingrediente
        # En etapas posteriores esto se manejará con una lista/bandeja
        print(f"Entregando {chef.ingrediente_en_mano.nombre}...")
        print("(La validación completa de recetas se conecta en Etapa 3)")