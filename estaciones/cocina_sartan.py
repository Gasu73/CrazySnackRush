# estaciones/cocina_sartan.py
from estaciones.estacion import Estacion
from modelo.proteina import Proteina
import time
import threading

TIEMPO_COCCION = 5       # segundos mínimos para cocinar
TIEMPO_QUEMADO = 4       # segundos adicionales antes de quemarse

class CocinaSartan(Estacion):
    def __init__(self):
        super().__init__(
            nombre="Cocina / Sartén",
            ingredientes_aceptados=[Proteina]
        )
        self.en_proceso = False
        self.cocinado = False
        self._timer_quemado = None
    
    def _iniciar_coccion(self):
        """Hilo interno que maneja los dos timers"""
        print(f"Cocinando {self.ingrediente_actual.nombre}...")
        time.sleep(TIEMPO_COCCION)
        
        if self.ingrediente_actual:
            self.ingrediente_actual.preparar()
            self.cocinado = True
            print(f"✅ {self.ingrediente_actual.nombre} está cocinado. ¡Recógelo pronto!")
            
            # Segundo timer: si no lo recogen, se quema
            time.sleep(TIEMPO_QUEMADO)
            if self.ingrediente_actual and self.cocinado:
                self.ingrediente_actual.quemar()
                print(f"🔥 {self.ingrediente_actual.nombre} se quemó!")
        
        self.en_proceso = False
    
    def interactuar(self, chef):
        # CASO 1: chef deja proteína en el sartén
        if chef.ingrediente_en_mano is not None:
            ingrediente = chef.ingrediente_en_mano

            if not self.acepta_ingrediente(ingrediente):
                print(f"El sartén no acepta {ingrediente.nombre}.")
                return
            
            if self.ingrediente_actual is not None:
                print("El sartén ya está ocupado.")
                return
            
            self.ingrediente_actual = chef.soltar_ingrediente()
            self.cocinado = False
            self.en_proceso = True

            # Iniciar cocción en hilo separado para no bloquear el juego
            hilo = threading.Thread(target=self._iniciar_coccion, daemon=True)
            hilo.start()
            return
        
        # CASO 2: chef recoge con manos vacías
        if self.ingrediente_actual is None:
            print("El sartén está vacío.")
            return
        
        if self.ingrediente_actual.estado == "quemado":
            print(f"⚠️ {self.ingrediente_actual.nombre} está quemado, hay que tirarlo.")
            self.ingrediente_actual = None
            self.en_proceso = False
            return
        
        if self.ingrediente_actual.estado == "cocinado":
            chef.recoger_ingrediente(self.ingrediente_actual)
            print(f"{chef.nombre} recogió {self.ingrediente_actual.nombre} (cocinado).")
            self.ingrediente_actual = None
            self.cocinado = False
            return
        
        print(f"Espera, {self.ingrediente_actual.nombre} aún se está cocinando...")