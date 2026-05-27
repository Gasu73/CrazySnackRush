from modelo.ingrediente import Ingrediente

class Proteina(Ingrediente):
    def __init__(self, nombre: str, tiempo_preparacion_req: int, tiempo_max_cocina: int):
        super().__init__(nombre, tiempo_preparacion_req)
        # Atributos exclusivos de la proteína
        self.__tiempo_max_cocina = tiempo_max_cocina
        self.__cocinada = False

    # Polimorfismo: Implementación específica para proteínas
    def preparar(self, tiempo_invertido: int):
        self._tiempo_actual += tiempo_invertido
        
        if self._tiempo_actual >= self.__tiempo_max_cocina:
            self._estado = "quemado"
            self.__cocinada = False
        elif self._tiempo_actual >= self._tiempo_preparacion_req:
            self._estado = "cocinado"
            self.__cocinada = True