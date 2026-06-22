from modelo.ingrediente import Ingrediente

class Proteina(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.cocinada = False      # atributo extra requerido por el enunciado
    
    def preparar(self):
        self.estado = "cocinado"
        self.cocinada = True
    
    def quemar(self):
        self.estado = "quemado"
        self.cocinada = False