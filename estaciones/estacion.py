from abc import ABC, abstractmethod

class Estacion(ABC):
    def __init__(self, nombre, ingredientes_aceptados=None):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes_aceptados or []
        self.ingrediente_actual = None      # lo que está sobre la estación
    
    def acepta_ingrediente(self, ingrediente):
        """Verifica si la estación puede procesar ese tipo de ingrediente"""
        return type(ingrediente) in self.ingredientes_aceptados
    
    @abstractmethod
    def interactuar(self, chef):
        """Lógica principal al presionar el botón de acción"""
        pass
    
    def __str__(self):
        return f"[{self.nombre}] | En mesa: {self.ingrediente_actual or 'vacío'}"