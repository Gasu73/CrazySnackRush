from modelo.ingrediente import Ingrediente

class PanesYBases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
    
    def preparar(self):
        self.estado = "listo"     # los panes no se cocinan, van directo