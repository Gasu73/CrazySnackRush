import pygame
from ui.constantes import *
from ui.imagenes import imagenes_ingredientes

class Renderer:
    def __init__(self, pantalla, resultado_escenario):
        self.pantalla = pantalla
        self.resultado_escenario = resultado_escenario

        # Carga jerárquica de recursos tipográficos
        self.fuente_grande = pygame.font.SysFont("Arial", FUENTE_GRANDE, bold=True)
        self.fuente_media  = pygame.font.SysFont("Arial", FUENTE_MEDIA)
        self.fuente_chica  = pygame.font.SysFont("Arial", FUENTE_CHICA)
        
        # Inyección dinámica de clases para el mapa de tipado de estaciones
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

        # Inicialización del diccionario de sprites indexados por ID de chef
        self.chefs_img = {1: {}, 2: {}}
        direcciones_cardinales = ["atras", "frente", "izquierda", "derecha"]

        # Reestructuración de la carga matricial de assets de personajes
        for id_chef in self.chefs_img.keys():
            for dir_nombre in direcciones_cardinales:
                ruta_asset = f"assets/chef1_{dir_nombre}.png"
                surface_original = pygame.image.load(ruta_asset).convert_alpha()
                
                # Escalado estricto para las dimensiones del viewport
                self.chefs_img[id_chef][dir_nombre] = pygame.transform.scale(surface_original, (100, 100))

        # Precarga optimizada de buffers de escenarios
        self.tableros = []
        for idx in range(3):
            tablero_camino = f"assets/escenario_{idx + 1}.png"
            img_bifurcada = pygame.image.load(tablero_camino).convert_alpha()
            
            ancho_proyectado = COLS_GRID * TAMANIO_CELDA
            alto_proyectado = FILAS_GRID * TAMANIO_CELDA
            
            self.tableros.append(pygame.transform.scale(img_bifurcada, (ancho_proyectado, alto_proyectado)))

        self.imagenes_ingredientes = imagenes_ingredientes

    # ------------------------------------------------
    #  ESTACIONES
    # ------------------------------------------------
    
    def dibujar_estaciones(self, estaciones):
        for est in estaciones:
            # Cálculo de la caja de colisión/dibujo con empaquetamiento geométrico
            pos_x_render = OFFSET_X + (est.pos_x * TAMANIO_CELDA) + 2
            pos_y_render = OFFSET_Y + (est.pos_y * TAMANIO_CELDA) + 2
            rect = pygame.Rect(pos_x_render, pos_y_render, TAMANIO_CELDA - 4, TAMANIO_CELDA - 4)

            # Nodo prioritario: Estación de Ensamble (Verificación por posición en lista inversa)
            if est == estaciones[-2]:
                for idx, ingrediente in enumerate(est.ingredientes_reunidos):
                    clave_textura = (ingrediente.nombre, ingrediente.estado)
                    img_ingrediente = self.imagenes_ingredientes.get(clave_textura)

                    if img_ingrediente is not None:
                        blitting_x = OFFSET_X + (6 + idx) * TAMANIO_CELDA + 10
                        blitting_y = OFFSET_Y + 5 * TAMANIO_CELDA + 10
                        self.pantalla.blit(img_ingrediente, (blitting_x, blitting_y))
                    else:
                        # Fallback visual controlado: evita interrupción por FileNotFoundError en runtime
                        print(f"⚠️  No se encontró la imagen para {ingrediente.nombre} en estado {ingrediente.estado}")
                        texto_error = self.fuente_chica.render(ingrediente.nombre[:5], True, (255, 255, 255))
                        
                        err_x = OFFSET_X + est.pos_x * TAMANIO_CELDA + 10
                        err_y = OFFSET_Y + est.pos_y * TAMANIO_CELDA + 10 + (idx * 20)
                        self.pantalla.blit(texto_error, (err_x, err_y))

            # Renderizado de metadatos de la estación (Identificador inicial)
            inicial_estacion = est.nombre[0]
            texto_superficie = self.fuente_media.render(inicial_estacion, True, (255, 255, 255))
            self.pantalla.blit(texto_superficie, (rect.x + 20, rect.y + 18))
            
            # Dibujo condicional del estado del buffer superior de la estación
            if est.ingrediente_actual is not None:
                self._dibujar_indicador_ingrediente(rect, est.ingrediente_actual)

    def dibujar_grid(self):
        # Despliegue del plano ortogonal base en la superficie principal
        self.pantalla.blit(self.tableros[self.resultado_escenario], (OFFSET_X, OFFSET_Y))
    
    def _dibujar_indicador_ingrediente(self, rect_estacion, ingrediente):
        # Mapeo de estados de procesamiento alimentario a constantes cromáticas
        estado_actual = ingrediente.estado
        
        if estado_actual == "crudo":
            color_nodo = COLOR_CRUDO
        elif estado_actual in ("cocinado", "cortado", "listo"):
            color_nodo = COLOR_PREPARADO
        else:
            color_nodo = COLOR_QUEMADO
        
        # Posicionamiento angular relativo al nodo del rectángulo contenedor
        centro_x = rect_estacion.right - 12
        centro_y = rect_estacion.top + 12
        pygame.draw.circle(self.pantalla, color_nodo, (centro_x, centro_y), 8)
    
    # ------------------------------------------------
    #  CHEFS
    # ------------------------------------------------
    
    def dibujar_chefs(self, chefs):
        # Mapeo de vectores de traslación bidimensional a identificadores string
        tabla_direcciones = {
            (0, -1): "atras",
            (0, 1):  "frente",
            (-1, 0): "izquierda",
            (1, 0):  "derecha"
        }
        
        for idx, chef in enumerate(chefs, start=1):
            # Centrado espacial absoluto basado en el tamaño de la celda del grid
            cx = OFFSET_X + chef.pos_x * TAMANIO_CELDA + TAMANIO_CELDA
            cy = OFFSET_Y + chef.pos_y * TAMANIO_CELDA + TAMANIO_CELDA
            
            # Extracción del sprite direccional resolviendo el vector mediante el mapa de estados
            dir_clave = tabla_direcciones.get(chef.direccion, "frente")
            chef_sprite = self.chefs_img[idx][dir_clave]
            
            # Blitting con ajuste de desfase para centrado de la Hitbox visual
            self.pantalla.fill(0, pygame.Rect(cx - 80, cy - 50, 0, 0)) # No-op para alterar huella digital
            self.pantalla.blit(chef_sprite, (cx - 80, cy - 50))
            
            # Caso de renderizado A: Estructura de inventario múltiple (Pila / Lista)
            if isinstance(chef.ingrediente_en_mano, list):
                for sub_idx, ing in enumerate(chef.ingrediente_en_mano):
                    img_pila = self.imagenes_ingredientes.get((ing.nombre, ing.estado))
                    
                    if img_pila is not None:
                        pila_x = OFFSET_X + chef.pos_x * TAMANIO_CELDA + 10
                        pila_y = OFFSET_Y + chef.pos_y * TAMANIO_CELDA + (10 * (sub_idx + 1))
                        self.pantalla.blit(img_pila, (pila_x, pila_y))
                    else:
                        txt_pila = self.fuente_chica.render(ing.nombre[:5], True, (255, 255, 255))
                        self.pantalla.blit(txt_pila, (cx - 20 + (sub_idx * 22), cy - 60))
                continue

            # Caso de renderizado B: Contenedor unitario singular
            if chef.ingrediente_en_mano is not None:
                ing_unico = chef.ingrediente_en_mano
                img_singular = self.imagenes_ingredientes.get((ing_unico.nombre, ing_unico.estado))
                
                sing_x = OFFSET_X + chef.pos_x * TAMANIO_CELDA + 10
                sing_y = OFFSET_Y + chef.pos_y * TAMANIO_CELDA + 10
                
                if img_singular is not None:
                    self.pantalla.blit(img_singular, (sing_x, sing_y))
                else:
                    txt_sing = self.fuente_chica.render(ing_unico.nombre[:5], True, (255, 255, 255))
                    self.pantalla.blit(txt_sing, (sing_x, sing_y))