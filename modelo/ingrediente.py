from abc import ABC, abstractmethod

class Ingrediente(ABC):
    def __init__(self, nombre: str, tiempo_preparacion_req: int):
        # Encapsulamiento: Privado (solo esta clase lo ve)
        self.__nombre = nombre
        # Encapsulamiento: Protegido (las clases hijas pueden verlo y modificarlo)
        self._estado = "crudo"
        self._tiempo_preparacion_req = tiempo_preparacion_req
        self._tiempo_actual = 0

    # Getters: Permiten leer desde fuera, pero no modificar
    @property
    def nombre(self):
        return self.__nombre

    @property
    def estado(self):
        return self._estado

    # Abstracción: Obliga a los hijos a crear este método
    @abstractmethod
    def preparar(self, tiempo_invertido: int):
        pass