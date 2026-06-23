from estaciones.estacion import Estacion
from modelo.vegetal_fruta import VegetalesYFrutas
import time

TIEMPO_CORTE = 3     # segundos, ajustable por el desarrollador

class TablaDeCortar(Estacion):
    def __init__(self):
        super().__init__(
            nombre="Tabla de Cortar",
            ingredientes_aceptados=[VegetalesYFrutas]
        )
        self.en_proceso = False
    
    def interactuar(self, chef):
        # CASO 1: el chef trae un ingrediente para dejar
        if chef.ingrediente_en_mano is not None:
            ingrediente = chef.ingrediente_en_mano

            if not self.acepta_ingrediente(ingrediente):
                return
            
            if self.ingrediente_actual is not None:
                print("La tabla ya tiene un ingrediente encima.")
                return
            
            # Dejar el ingrediente sobre la tabla
            self.ingrediente_actual = chef.soltar_ingrediente()
            print(f"{chef.nombre} dejó {self.ingrediente_actual.nombre} en la tabla.")
            return
        
        # CASO 2: el chef llega con manos vacías
        if self.ingrediente_actual is None:
            print("No hay nada en la tabla.")
            return
        
        # Si ya está preparado, el chef lo recoge
        if self.ingrediente_actual.estado == "cortado":
            chef.recoger_ingrediente(self.ingrediente_actual)
            print(f"{chef.nombre} recogió {self.ingrediente_actual.nombre} (cortado).")
            self.ingrediente_actual = None
            return
        
        # Si está crudo, iniciar el proceso de corte
        if not self.en_proceso:
            print(f"Cortando {self.ingrediente_actual.nombre}")
            self.en_proceso = True        # esto cambiará por un timer en la UI
            self.ingrediente_actual.preparar()
            self.en_proceso = False
            print(f"{self.ingrediente_actual.nombre} listo para recoger.")