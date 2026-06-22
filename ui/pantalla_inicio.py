# ui/pantalla_inicio.py
import pygame
from ui.constantes import *

class PantallaInicio:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        # Fuentes estándar pero con tamaños limpios
        self.fuente_titulo  = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_sub     = pygame.font.SysFont("Arial", 22, bold=True)
        self.fuente_chica   = pygame.font.SysFont("Arial", 16)
        self.seleccion      = 0       

        self.opciones = [
            "Restaurante Hamburguesas  (Fácil)",
            "Restaurante Sushi          (Medio)",
            "Restaurante Pizza          (Difícil)",
        ]

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.seleccion = (self.seleccion - 1) % len(self.opciones)
            elif evento.key == pygame.K_DOWN:
                self.seleccion = (self.seleccion + 1) % len(self.opciones)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.seleccion
        return None

    def dibujar(self):
        # Fondo completamente negro para dar atmósfera limpia/oscura
        self.pantalla.fill((15, 15, 15))

        # ── TÍTULO ASIMÉTRICO (Estilo FNAF / Menú de lado) ──
        # Lo tiramos arriba a la izquierda en lugar del centro aburrido
        titulo = self.fuente_titulo.render("Crazy Snack Rush", True, (220, 220, 220))
        self.pantalla.blit(titulo, (50, 100))

        subtitulo = self.fuente_sub.render("SUB-SISTEMA TEC", True, (100, 100, 100))
        self.pantalla.blit(subtitulo, (50, 155))

        # ── BOTONES ALINEADOS A UN COSTADO ──
        # En lugar de cajas centradas, son líneas limpias alineadas a la derecha
        X_BOTONES = ANCHO - 450  # Desplazados hacia la derecha de la pantalla
        
        for i, opcion in enumerate(self.opciones):
            es_activa = (i == self.seleccion)
            
            # Si está seleccionado, brilla en rojo/naranja y se desplaza un poco a la izquierda
            if es_activa:
                color_texto = (255, 70, 70)
                offset_x = -15  # Efecto visual de selección básica
                marcador = "> "
            else:
                color_texto = (130, 130, 130)
                offset_x = 0
                marcador = "  "

            # Renderizado de la opción de texto plano
            texto = self.fuente_sub.render(f"{marcador}{opcion}", True, color_texto)
            self.pantalla.blit(texto, (X_BOTONES + offset_x, 260 + i * 70))

        # ── INSTRUCCIONES ABAJO A LA IZQUIERDA ──
        inst = self.fuente_chica.render("[W/S o Flechas para mover  •  ENTER para ejecutar]", True, (70, 70, 70))
        self.pantalla.blit(inst, (50, ANCHO // 2 + 120))