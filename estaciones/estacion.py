from abc import ABC, abstractmethod

class Estacion(ABC):
    def __init__(self, nombre, pos_x=0, pos_y=0, ingredientes_aceptados=None):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes_aceptados or []
        self.ingrediente_actual = None      # lo que está sobre la estación

        #posición en el grid
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    def acepta_ingrediente(self, ingrediente):
        #Verifica si la estación puede procesar ese tipo de ingrediente
        return type(ingrediente) in self.ingredientes_aceptados
    
    @abstractmethod
    def interactuar(self, chef):
        #Lógica principal al presionar el botón de acción
        pass