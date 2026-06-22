import pygame
from ui.constantes import *
from ui.imagenes import imagenes_ingredientes, imagenes_recetas

class HUD:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        # Inicialización de fuentes tipográficas con variaciones de escala jerárquica
        self.fuente_grande = pygame.font.SysFont("Arial", FUENTE_GRANDE, bold=True)
        self.fuente_media  = pygame.font.SysFont("Arial", FUENTE_MEDIA)
        self.fuente_chica  = pygame.font.SysFont("Arial", FUENTE_CHICA)

        # Mapeos de recursos gráficos indexados (Assets)
        self.imagenes_ingredientes = imagenes_ingredientes
        self.imagenes_recetas = imagenes_recetas

    def dibujar(self, escenario, chef_activo):
        # Renderizado de la región geométrica base que delimita el HUD
        dimensiones_fondo = (0, 0, ANCHO, OFFSET_Y - 10)
        pygame.draw.rect(self.pantalla, COLOR_HUD_FONDO, dimensiones_fondo)

        # Delegación secuencial del renderizado de componentes de la interfaz
        self._dibujar_tiempo(escenario.tiempo_restante)
        self._dibujar_puntaje(escenario.chefs)
        self._dibujar_ordenes(escenario.ordenes)
        self._dibujar_chef_activo(chef_activo)

    def _dibujar_tiempo(self, tiempo):
        # Operador ternario para la asignación dinámica de estados cromáticos basados en criticidad
        color = COLOR_TIEMPO_OK if tiempo > 30 else COLOR_TIEMPO_POCO
        texto = self.fuente_grande.render(f"{tiempo}s", True, color)
        
        # Cálculo de centrado horizontal relativo al ancho de la pantalla
        pos_x = (ANCHO // 2) - 50
        self.pantalla.blit(texto, (pos_x, 10))

    def _dibujar_puntaje(self, chefs):
        # Desplazamiento iterativo horizontal para la representación del estado de los jugadores
        for idx, chef in enumerate(chefs):
            formato_texto = f"{chef.nombre}: {chef.puntos}pts"
            texto = self.fuente_media.render(formato_texto, True, COLOR_HUD_TEXTO)
            
            # Cálculo de la matriz de espaciado lineal en el eje X
            desplazamiento_x = 20 + (idx * 220)
            self.pantalla.blit(texto, (desplazamiento_x, 15))

    def _dibujar_ordenes(self, ordenes):
        """
        Dibuja cada receta activa como una tarjeta vertical:
        """
        # Guard clause: Aborta el procedimiento de dibujo si la cola de órdenes está vacía
        if not ordenes:
            return

        TARJETA_ANCHO = 130
        TARJETA_ALTO  = 100
        MARGEN        = 8
        ICONO_RECETA  = 32
        ICONO_ING     = 22

        # Acotamiento estricto de renderizado simultáneo para optimizar el espacio en el viewport
        cantidad = min(len(ordenes), 4)
        
        # Inversión del cálculo posicional: alineación horizontal con anclaje a la derecha
        x_inicio = ANCHO - ((TARJETA_ANCHO + MARGEN) * cantidad) - MARGEN

        for i, receta in enumerate(ordenes[:4]):
            x = x_inicio + i * (TARJETA_ANCHO + MARGEN)
            y = MARGEN

            # ── Contenedor base de la tarjeta (Border Radius suavizado) ──
            rect = pygame.Rect(x, y, TARJETA_ANCHO, TARJETA_ALTO)
            pygame.draw.rect(self.pantalla, COLOR_RECETA_FONDO, rect, border_radius=6)
            pygame.draw.rect(self.pantalla, COLOR_RECETA_BORDE, rect, 1, border_radius=6)

            # ── Región Izquierda: Iconografía principal del entregable ──
            col_izq_x = x + 6
            img_receta = self.imagenes_recetas.get(receta.nombre)
            
            if img_receta is not None:
                img_escalada = pygame.transform.scale(img_receta, (ICONO_RECETA, ICONO_RECETA))
                self.pantalla.blit(img_escalada, (col_izq_x, y + 8))
            else:
                # Renderizado alternativo (Fallback visual) si el asset no está cargado
                dimensiones_fb = (col_izq_x, y + 8, ICONO_RECETA, ICONO_RECETA)
                pygame.draw.rect(self.pantalla, COLOR_RECETA_BORDE, dimensiones_fb, 1, border_radius=4)

            # ── Separador Estructural del Componente ──
            linea_x = col_izq_x + ICONO_RECETA + 8
            punto_inicio = (linea_x, y + 6)
            punto_fin = (linea_x, y + TARJETA_ALTO - 6)
            pygame.draw.line(self.pantalla, COLOR_RECETA_BORDE, punto_inicio, punto_fin, 1)

            # ── Sub-componente: Lista apilada de requerimientos (Ingredientes) ──
            ing_x = linea_x + 8
            ing_y = y + 6
            for ingrediente in receta.lista_ingredientes:
                # Recuperación por clave compuesta (Tupla de Identificador y Estado)
                clave_asset = (ingrediente.nombre, ingrediente.estado)
                img_ing = self.imagenes_ingredientes.get(clave_asset)
                
                if img_ing is not None:
                    img_ing_escalada = pygame.transform.scale(img_ing, (ICONO_ING, ICONO_ING))
                    self.pantalla.blit(img_ing_escalada, (ing_x, ing_y))
                else:
                    pygame.draw.rect(self.pantalla, COLOR_RECETA_BORDE, (ing_x, ing_y, ICONO_ING, ICONO_ING), 1, border_radius=3)
                
                # Desplazamiento lineal acumulativo para evitar colisión de texturas en la pila
                ing_y += (ICONO_ING + 3)

            # ── Bloque Metrométrico e Información de Recompensa ──
            progreso = receta.max_time_receta - receta.tiempo_transcurrido
            color_tiempo = COLOR_TIEMPO_OK if progreso > 15 else COLOR_TIEMPO_POCO

            tiempo_texto = self.fuente_chica.render(f"{progreso}s", True, color_tiempo)
            puntos_texto = self.fuente_chica.render(f"{receta.puntos_receta}pt", True, COLOR_HUD_TEXTO)

            # Inyección de superficies de texto en base a offsets relativos del contenedor izquierdo
            self.pantalla.blit(tiempo_texto, (col_izq_x, y + ICONO_RECETA + 12))
            self.pantalla.blit(puntos_texto, (col_izq_x, y + ICONO_RECETA + 28))

    def _dibujar_chef_activo(self, chef):
        # Etiqueta indicadora del foco de control actual (Polimorfismo / Estado de la UI)
        formato_indicador = f"Controlando: {chef.nombre} | TAB para cambiar"
        texto = self.fuente_chica.render(formato_indicador, True, (180, 180, 180))
        self.pantalla.blit(texto, (20, OFFSET_Y - 25))