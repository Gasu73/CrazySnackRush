class Chef:
    def __init__(self, nombre: str):
        self.__nombre = nombre
        self.__ingrediente_en_mano = None

    @property
    def nombre(self):
        return self.__nombre

    @property
    def ingrediente_en_mano(self):
        return self.__ingrediente_en_mano

    def agarrar_ingrediente(self, ingrediente):
        self.__ingrediente_en_mano = ingrediente

    def soltar_ingrediente(self):
        item = self.__ingrediente_en_mano
        self.__ingrediente_en_mano = None
        return item