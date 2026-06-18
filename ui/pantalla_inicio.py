import pygame
from ui.constantes import *

class PantallaInicio:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo  = pygame.font.SysFont("Arial", 52, bold=True)
        self.fuente_sub     = pygame.font.SysFont("Arial", 28)
        self.fuente_chica   = pygame.font.SysFont("Arial", 20)
        self.seleccion      = 0       # escenario seleccionado (0, 1, 2)

        self.opciones = [
            "Restaurante Hamburguesas  (Fácil)",
            "Restaurante Sushi          (Medio)",
            "Restaurante Pizza          (Difícil)",
        ]

    def manejar_evento(self, evento):
        """
        Retorna el índice del escenario elegido,
        o None si el jugador no confirmó aún.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.seleccion = (self.seleccion - 1) % len(self.opciones)
            elif evento.key == pygame.K_DOWN:
                self.seleccion = (self.seleccion + 1) % len(self.opciones)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.seleccion
        return None

    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)

        # Título
        titulo = self.fuente_titulo.render(
            "Crazy Snack Rush TEC", True, (255, 200, 60)
        )
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 80))

        subtitulo = self.fuente_sub.render(
            "Selecciona un escenario", True, COLOR_HUD_TEXTO
        )
        self.pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 160))

        # Opciones
        for i, opcion in enumerate(self.opciones):
            es_seleccionada = i == self.seleccion
            color_fondo = COLOR_RECETA_BORDE if es_seleccionada else COLOR_RECETA_FONDO
            color_texto = (255, 255, 255) if es_seleccionada else (180, 180, 180)

            rect = pygame.Rect(ANCHO // 2 - 280, 240 + i * 80, 560, 60)
            pygame.draw.rect(self.pantalla, color_fondo, rect, border_radius=10)
            pygame.draw.rect(self.pantalla, COLOR_RECETA_BORDE, rect, 2, border_radius=10)

            texto = self.fuente_sub.render(opcion, True, color_texto)
            self.pantalla.blit(
                texto,
                (rect.x + 20, rect.y + 15)
            )

        # Instrucciones
        inst = self.fuente_chica.render(
            "↑↓ para navegar   |   ENTER para jugar", True, (120, 120, 120)
        )
        self.pantalla.blit(inst, (ANCHO // 2 - inst.get_width() // 2, 530))