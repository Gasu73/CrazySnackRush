import pygame

class Controles:
    def __init__(self, escenario):
        self.escenario = escenario
        self.chef_activo_idx = 0          # índice del chef que se controla
    
    @property
    def chef_activo(self):
        # Desacopla el acceso al objeto chef actual utilizando la propiedad indexada
        return self.escenario.chefs[self.chef_activo_idx]
    
    def cambiar_chef(self):
        total = len(self.escenario.chefs)
        # Operación cíclica aritmética (módulo) para evitar desbordamiento de índice
        self.chef_activo_idx = (self.chef_activo_idx + 1) % total

        print(f"Ahora controlas a {self.chef_activo.nombre}")
    
    def procesar_evento(self, evento):
        # Early exit / Guard Clause: Descarta eventos que no correspondan a pulsación de teclas
        if evento.type != pygame.KEYDOWN:
            return
        
        tecla = evento.key
        
        # Estructura de control por mapeo de teclado lineal alternativo
        if tecla == pygame.K_TAB:
            self.cambiar_chef()
        elif tecla == pygame.K_UP or tecla == pygame.K_w:
            self._mover(0, -1)
        elif tecla == pygame.K_DOWN or tecla == pygame.K_s:
            self._mover(0, 1)
        elif tecla == pygame.K_LEFT or tecla == pygame.K_a:
            self._mover(-1, 0)
        elif tecla == pygame.K_RIGHT or tecla == pygame.K_d:
            self._mover(1, 0)
        elif tecla == pygame.K_e or tecla == pygame.K_SPACE:
            self.accion()
    
    def _mover(self, dx, dy):
        chef = self.chef_activo
        chef.direccion = (dx, dy)
        
        # Predicción posicional de la siguiente coordenada en el espacio bidimensional
        nueva_x = chef.pos_x + dx
        nueva_y = chef.pos_y + dy
        
        from ui.constantes import COLS_GRID, FILAS_GRID

        # Generación dinámica por comprensión del conjunto de colisiones rígidas (obstáculos)
        POSICIONES_BLOQUEADAS = {(x, y) for x in range(5, 12) for y in range(4, 6)}

        # Segmentación de la lógica booleana de límites para mejorar mantenibilidad
        dentro_limites = (2 <= nueva_x < COLS_GRID - 3) and (3 <= nueva_y < FILAS_GRID - 2)
        excepciones_validas = (nueva_x, nueva_y) in {(2, 2), (2, 10)}
        esta_bloqueado = (nueva_x, nueva_y) in POSICIONES_BLOQUEADAS

        # Evaluación final del espacio de estados transicional del personaje
        if (dentro_limites or excepciones_validas) and not esta_bloqueado:
            chef.pos_x = nueva_x
            chef.pos_y = nueva_y
    
    def accion(self):
        chef = self.chef_activo
        estacion = self.estacion_frente(chef)
        
        # Patrón de delegación de comportamiento basado en la presencia de una entidad interactuable
        if not estacion:
            print("No hay estación frente al chef.")
            return
            
        estacion.interactuar(chef)
    
    def estacion_frente(self, chef):
        # Región delimitada por Hash Set para optimización O(1) en la búsqueda de la zona de ensamble
        ESTACION_EMSAMBLE = {(x, y) for x in range(5, 12) for y in range(6, 7)}

        # Intercepción prioritaria en el grid de ensamble usando indexación inversa
        if (chef.pos_x, chef.pos_y) in ESTACION_EMSAMBLE:
            return self.escenario.estaciones[-2] 

        # Búsqueda lineal iterativa para estaciones con hitboxes puntuales coincidentes
        for estacion in self.escenario.estaciones:
            if estacion.pos_x == chef.pos_x and estacion.pos_y == chef.pos_y:
                return estacion
            
        return None