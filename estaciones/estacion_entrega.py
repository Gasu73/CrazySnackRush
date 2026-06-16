from estaciones.estacion import Estacion #Importación clase madre

class EstacionEntrega(Estacion):    #Hereda de clase madre
    def __init__(self, recetas_activas):
        super().__init__(nombre="Estación de Entrega")
        self.recetas_activas = recetas_activas   
    
    def interactuar(self, chef):
        if chef.ingrediente_en_mano is None:
            print("No has agarrado nada")
            return
        #Se entrega de a un elemento, esto se cambiará posteriormente
        print(f"Entregando {chef.ingrediente_en_mano.nombre}...")
        print("(La validación completa de recetas se conecta en Etapa 3)")