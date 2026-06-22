from estaciones.estacion import Estacion

class EstacionEnsamble(Estacion):
    def __init__(self, pos_x=0, pos_y=0):
        super().__init__(
            nombre="Mesa de Ensamble",
            pos_x=pos_x,
            pos_y=pos_y
        )
        self.ingredientes_reunidos = []   # van acumulando acá

    def interactuar(self, chef):
        # Chef deja un ingrediente

        if chef.ingrediente_en_mano is not None:

            if isinstance(chef.ingrediente_en_mano, list):
                self.ingredientes_reunidos.extend(chef.ingrediente_en_mano)
                chef.ingrediente_en_mano = None
                return


            ingrediente = chef.soltar_ingrediente()

            self.ingredientes_reunidos.append(ingrediente)


            print(f"{chef.nombre} puso {ingrediente.nombre} en la mesa.")

            print(f"En mesa: {', '.join([i.nombre for i in self.ingredientes_reunidos])}")

            return

        # Chef llega con manos vacías → recoge todo para entregar
        if not self.ingredientes_reunidos:
            print("La mesa de ensamble está vacía.")
            return

        print(f"{chef.nombre} recogió todos los ingredientes para entregar.")

        recogidos = self.ingredientes_reunidos.copy()
        self.ingredientes_reunidos = []

        chef.ingrediente_en_mano = recogidos   # ahora el chef lleva todo junto


    def limpiar(self):

        self.ingredientes_reunidos = []
        
        print("Mesa de ensamble limpiada.")