from estaciones.estacion import Estacion

class EstacionEntrega(Estacion):
    def __init__(self, cocina=None, pos_x=0, pos_y=0):
        super().__init__(nombre="Estacion de Entrega", pos_x=pos_x, pos_y=pos_y)
        
        self.cocina = cocina   # referencia a CocinaEscenario

    def interactuar(self, chef):
        # El chef intenta entregar los ingredientes que tiene en mano a la cocina

        ingredientes = chef.ingrediente_en_mano
        
        if not ingredientes:
            print("No hay ingredientes para entregar.")
            return

        exito = self.cocina.intentar_entrega(chef, ingredientes)
        if exito:
            chef.ingrediente_en_mano = None 
        
        if not exito:
            print("Los ingredientes no coinciden con ninguna receta.")