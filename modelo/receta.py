# receta.py
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

        if len(ingredientes_entregados) != len(self.lista_ingredientes):
            return False
        
        # Comparar por nombre
        requeridos = []

        for ingrediente in self.lista_ingredientes:
            requeridos.append(ingrediente.nombre)

        entregados = []

        for ingrediente in ingredientes_entregados:
            entregados.append(ingrediente.nombre)

        # Ordenar listas
        requeridos.sort()
        entregados.sort()

        # Comparar
        return requeridos == entregados
    
    