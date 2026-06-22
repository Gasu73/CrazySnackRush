from modelo.ingrediente import Ingrediente

class VegetalesYFrutas(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
    
    def preparar(self):
        self.estado = "cortado"