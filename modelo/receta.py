class Receta:
    def __init__(self, nombre, ingredientes, puntos_base, tiempo_max):
        self.nombre = nombre
        self.lista_ingredientes = ingredientes   # List[Ingrediente]
        self.puntos_receta = puntos_base
        self.max_time_receta = tiempo_max
        self.tiempo_transcurrido = 0
        self.activa = True
    
    def reducir_puntos(self):
        #Se llama cuando se vence el tiempo máximo
        self.puntos_receta = self.puntos_receta // 2
        if self.puntos_receta == 0:
            self.activa = False     # receta expirada

    
    def comparar_receta(self, ingredientes_entregados):
        #Compara los ingredientes entregados con los requeridos por la receta.

        if not isinstance(ingredientes_entregados, list):
            print("Los ingredientes entregados no están en el formato correcto.")
            return False

        for ingrediente in ingredientes_entregados:
            if ingrediente.estado == "crudo":
                print(f"El ingrediente {ingrediente.nombre} está crudo. No se acepta.")
                return False    # no se aceptan ingredientes crudos

        if len(ingredientes_entregados) != len(self.lista_ingredientes):
            print("La cantidad de ingredientes no coincide.")
            return False
        
        # Comparar por nombre y estado
        requeridos = sorted([i.nombre for i in self.lista_ingredientes])
        entregados = sorted([i.nombre for i in ingredientes_entregados])
        
        return requeridos == entregados