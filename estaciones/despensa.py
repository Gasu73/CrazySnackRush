from estaciones.estacion import Estacion

class Despensa(Estacion):
    def __init__(self, ingrediente):
        super().__init__(
            nombre=f"Despensa de {ingrediente.nombre}",
            ingredientes_aceptados=[]       # no procesa, solo entrega

        )

        self.ingrediente = ingrediente
    
    def interactuar(self, chef):


        """
        Si el chef tiene las manos vacías,
        le entrega un ingrediente nuevo.
        """

        if chef.ingrediente_en_mano is not None:

            print(f"{chef.nombre} ya tiene algo en mano, suéltalo primero.")
            return
        
        nuevo = self.ingrediente
        chef.recoger_ingrediente(nuevo)
        print(f"{chef.nombre} tomó {nuevo.nombre} de la despensa.")