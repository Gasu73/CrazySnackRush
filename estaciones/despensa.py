from estaciones.estacion import Estacion

class Despensa(Estacion):
    def __init__(self, tipo_ingrediente):
        super().__init__(
            nombre=f"Despensa de {tipo_ingrediente.__name__}",
            ingredientes_aceptados=[]       # no procesa, solo entrega
        )
        self.tipo_ingrediente = tipo_ingrediente
        self.nombre_ingrediente = tipo_ingrediente.__name__
    
    def interactuar(self, chef):
        """
        Si el chef tiene las manos vacías,
        le entrega un ingrediente nuevo.
        """
        if chef.ingrediente_en_mano is not None:
            print(f"{chef.nombre} ya tiene algo en mano, suéltalo primero.")
            return
        
        nuevo = self.tipo_ingrediente(self.nombre_ingrediente)
        chef.recoger_ingrediente(nuevo)
        print(f"{chef.nombre} tomó {nuevo.nombre} de la despensa.")