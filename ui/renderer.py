import pygame
from ui.constantes import *
from ui.imagenes import imagenes_ingredientes

class Renderer:
    def __init__(self, pantalla, resultado_escenario):
        self.pantalla = pantalla
        self.resultado_escenario = resultado_escenario

        self.fuente_grande = pygame.font.SysFont("Arial", FUENTE_GRANDE, bold=True)
        self.fuente_media  = pygame.font.SysFont("Arial", FUENTE_MEDIA)
        self.fuente_chica  = pygame.font.SysFont("Arial", FUENTE_CHICA)
        
        # Colores por tipo de estación
        from estaciones.despensa        import Despensa
        from estaciones.cocina_sartan   import CocinaSartan
        from estaciones.tabla_cortar    import TablaDeCortar
        from estaciones.freidora        import Freidora
        from estaciones.estacion_entrega import EstacionEntrega
        
        self.colores_estacion = {
            Despensa:         COLOR_DESPENSA,
            CocinaSartan:     COLOR_SARTAN,
            TablaDeCortar:    COLOR_TABLA,
            Freidora:         COLOR_FREIDORA,
            EstacionEntrega:  COLOR_ENTREGA,
        }

        self.chefs_img = {}

        for i in [1, 2]:
            self.chefs_img[i] = {}
            for direccion in ["atras", "frente", "izquierda", "derecha"]:
                img = pygame.image.load(
                    f"assets/chef1_{direccion}.png"
                ).convert_alpha()

                img = pygame.transform.scale(img, (100, 100))

                self.chefs_img[i][direccion] = img

        self.tableros = []

        for i in range(3):
            img = pygame.image.load(f"assets/escenario_{i + 1}.png").convert_alpha()
            img = pygame.transform.scale(
                img,
                (COLS_GRID * TAMANIO_CELDA, FILAS_GRID * TAMANIO_CELDA)
            )
            self.tableros.append(img)


        self.imagenes_ingredientes = imagenes_ingredientes


    #ESTACIONES
    
    def dibujar_estaciones(self, estaciones):
        for est in estaciones:
            color = self.colores_estacion.get(type(est), (100, 100, 100))
            rect = pygame.Rect(
                OFFSET_X + est.pos_x * TAMANIO_CELDA + 2,
                OFFSET_Y + est.pos_y * TAMANIO_CELDA + 2,
                TAMANIO_CELDA - 4, TAMANIO_CELDA - 4
            )
            #pygame.draw.rect(self.pantalla, color, rect, border_radius=8)

            if est == estaciones[-2]:  # Estación de Ensamble
                for i, ingrediente  in enumerate(est.ingredientes_reunidos):

                    try:
                        img = self.imagenes_ingredientes[(ingrediente.nombre, ingrediente.estado)]
                        self.pantalla.blit(img, ((OFFSET_X + (6 + i) * TAMANIO_CELDA + 10, OFFSET_Y + 5 * TAMANIO_CELDA + 10)))

                    except FileNotFoundError:
                        print(f"⚠️  No se encontró la imagen para {ingrediente.nombre} en estado {ingrediente.estado}")

                        texto = self.fuente_chica.render(
                            ingrediente.nombre[:5],
                            True, (255, 255, 255)
                        )
                        self.pantalla.blit(texto, (OFFSET_X + est.pos_x * TAMANIO_CELDA + 10, OFFSET_Y + est.pos_y * TAMANIO_CELDA + 10 + i * 20))

            
            # Nombre abreviado
            inicial = est.nombre[0]
            texto = self.fuente_media.render(inicial, True, (255, 255, 255))
            self.pantalla.blit(texto, (rect.x + 20, rect.y + 18))
            
            # Indicador de ingrediente encima
            if est.ingrediente_actual:
                self._dibujar_indicador_ingrediente(rect, est.ingrediente_actual)


    def dibujar_grid(self):

        tablero_img = self.tableros[self.resultado_escenario]
        self.pantalla.blit(tablero_img, (OFFSET_X, OFFSET_Y))
    
    def _dibujar_indicador_ingrediente(self, rect_estacion, ingrediente):
        estado = ingrediente.estado
        if estado == "crudo":
            color = COLOR_CRUDO
        elif estado in ("cocinado", "cortado", "listo"):
            color = COLOR_PREPARADO
        else:
            color = COLOR_QUEMADO
        
        circulo_x = rect_estacion.right - 12
        circulo_y = rect_estacion.top + 12
        pygame.draw.circle(self.pantalla, color, (circulo_x, circulo_y), 8)
    

    # CHEFS
    def dibujar_chefs(self, chefs):
        colores = [COLOR_CHEF1, COLOR_CHEF2]
        
        for i, chef in enumerate(chefs, start=1):
            # color = colores[i % len(colores)]
            cx = OFFSET_X + chef.pos_x * TAMANIO_CELDA + TAMANIO_CELDA
            cy = OFFSET_Y + chef.pos_y * TAMANIO_CELDA + TAMANIO_CELDA
            

            if chef.direccion == (0, -1):
                direccion = "atras"
            elif chef.direccion == (0, 1):
                direccion = "frente" 
            elif chef.direccion == (-1, 0):
                direccion = "izquierda" 
            elif chef.direccion == (1, 0):
                direccion = "derecha" 
            

            chef_img = self.chefs_img[i][direccion]
            self.pantalla.blit(chef_img, (cx - 80, cy - 50))
            
            
            # Ingrediente en mano (lista)
            if isinstance(chef.ingrediente_en_mano, list):
                for j, ing in enumerate(chef.ingrediente_en_mano):
                    try:
                        img = self.imagenes_ingredientes[(ing.nombre, ing.estado)]
                        self.pantalla.blit(img, ((OFFSET_X + chef.pos_x * TAMANIO_CELDA + 10, OFFSET_Y + chef.pos_y * TAMANIO_CELDA + 10*(j + 1))))

                    except FileNotFoundError:
                        print(f"⚠️  No se encontró la imagen para {ing.nombre} en estado {ing.estado}")

                        texto = self.fuente_chica.render(
                            ing.nombre[:5],
                            True, (255, 255, 255)
                        )
                        self.pantalla.blit(texto, (cx - 20 + j * 22, cy - 60))
                continue

            # Ingrediente en mano (único)
            if chef.ingrediente_en_mano:

                try:
                    img = self.imagenes_ingredientes[(chef.ingrediente_en_mano.nombre, chef.ingrediente_en_mano.estado)]
                    self.pantalla.blit(img, ((OFFSET_X + chef.pos_x * TAMANIO_CELDA + 10, OFFSET_Y + chef.pos_y * TAMANIO_CELDA + 10)))


                except FileNotFoundError:
                    print(f"⚠️  No se encontró la imagen para {chef.ingrediente_en_mano.nombre} en estado {chef.ingrediente_en_mano.estado}")

                    texto = self.fuente_chica.render(
                        chef.ingrediente_en_mano.nombre[:5],
                        True, (255, 255, 255)
                    )
                    self.pantalla.blit(texto, (OFFSET_X + chef.pos_x * TAMANIO_CELDA + 10, OFFSET_Y + chef.pos_y * TAMANIO_CELDA + 10))