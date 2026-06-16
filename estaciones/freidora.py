# estaciones/freidora.py
from estaciones.estacion import Estacion
from modelo.pan_base import PanesYBases       # las papas serán PanesYBases o una subclase
import time
import threading

TIEMPO_FRITURA = 6

class Freidora(Estacion):
    def __init__(self):
        super().__init__(
            nombre="Freidora",
            ingredientes_aceptados=[PanesYBases]
        )
        self.en_proceso = False
    
    def _freir(self):
        print(f"Friendo {self.ingrediente_actual.nombre}...")
        time.sleep(TIEMPO_FRITURA)
        if self.ingrediente_actual:
            self.ingrediente_actual.preparar()
            print(f"🍟 {self.ingrediente_actual.nombre} listo!")
        self.en_proceso = False
    
    def interactuar(self, chef):
        # Chef deja el ingrediente
        if chef.ingrediente_en_mano is not None:
            ingrediente = chef.ingrediente_en_mano

            if not self.acepta_ingrediente(ingrediente):
                print(f"La freidora no acepta {ingrediente.nombre}.")
                return
            
            if self.ingrediente_actual is not None:
                print("La freidora ya está ocupada.")
                return
            
            self.ingrediente_actual = chef.soltar_ingrediente()
            self.en_proceso = True
            hilo = threading.Thread(target=self._freir, daemon=True)
            hilo.start()
            return
        
        # Chef recoge
        if self.ingrediente_actual is None:
            print("La freidora está vacía.")
            return
        
        if self.ingrediente_actual.estado == "listo":
            chef.recoger_ingrediente(self.ingrediente_actual)
            print(f"{chef.nombre} recogió {self.ingrediente_actual.nombre} (frito).")
            self.ingrediente_actual = None
            return
        
        print("Aún se está friendo, espera...")