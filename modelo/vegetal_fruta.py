from modelo.ingrediente import Ingrediente

class VegetalesYFrutas(Ingrediente):
    def __init__(self, nombre: str, tiempo_preparacion_req: int = 0):
        super().__init__(nombre, tiempo_preparacion_req)

    # Polimorfismo: Implementación específica para vegetales
    def preparar(self, tiempo_invertido: int):
        if self._estado == "crudo":
            self._tiempo_actual += tiempo_invertido
            if self._tiempo_actual >= self._tiempo_preparacion_req:
                self._estado = "cortado"