# chef.py
class Chef:
    def __init__(self, nombre, pos_x=0, pos_y=0):
        self.nombre = nombre
        self.puntos = 0
        self.ingrediente_en_mano = None    # solo puede cargar 1 o una lista de ingredientes (ensamble)


        #NUEVO — posición en el grid
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direccion = (1, 0)     # mira a la derecha por defecto
    
    def _mover(self, dx, dy):
        # La dirección se actualiza con cada movimiento
        self.direccion = (dx, dy)
    
    def recoger_ingrediente(self, ingrediente):
        if self.ingrediente_en_mano is None:
            self.ingrediente_en_mano = ingrediente
            return True
        print(f"{self.nombre} ya tiene un ingrediente en mano.")
        return False
    
    def soltar_ingrediente(self):
        soltado = self.ingrediente_en_mano
        self.ingrediente_en_mano = None
        return soltado
    
    def agregar_puntos(self, puntos):
        self.puntos += puntos
        if self.puntos < 0:
            self.puntos = 0           # mínimo es 0 según el enunciado
    
    def __str__(self):
        mano = self.ingrediente_en_mano or "vacía"
        return f"Chef {self.nombre} | Puntos: {self.puntos} | Mano: {mano}"