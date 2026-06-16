class Chef:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.ingrediente_en_mano = None
        self.puntos = 0

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