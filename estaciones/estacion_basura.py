from estaciones.estacion import Estacion

class EstacionBasura(Estacion):
    def __init__(self, pos_x=0, pos_y=0):
        super().__init__(
            nombre="Basura",
            pos_x=pos_x,
            pos_y=pos_y
        )

    def interactuar(self, chef):
        if chef.ingrediente_en_mano is None:
            print("No tenés nada que tirar.")
            return

        descartado = chef.soltar_ingrediente()
        print(f" {chef.nombre} tiró a la basura.")