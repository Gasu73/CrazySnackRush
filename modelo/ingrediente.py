from abc import ABC, abstractmethod

class Ingrediente(ABC):
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "crudo"      # crudo | preparado | quemado
    
    @abstractmethod
    def preparar(self):
        pass