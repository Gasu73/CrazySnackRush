# ui/pantalla_fin.py
import pygame
from ui.constantes import *

class PantallaFin:
    def __init__(self, pantalla):
        self.pantalla     = pantalla
        
        # Consistencia en la escala tipográfica no-lineal
        self.fuente_big   = pygame.font.SysFont("Arial", 48, bold=True)
        self.fuente_med   = pygame.font.SysFont("Arial", 26, bold=True)
        self.fuente_chica = pygame.font.SysFont("Arial", 16)

    def manejar_evento(self, evento):
        """
        Retorna:
          'menu'    → volver al menú
          'salir'   → cerrar el juego
          None      → sin acción
        """
        # Cláusula de guarda para eventos de teclado
        if evento.type != pygame.KEYDOWN:
            return None
            
        tecla_pulsada = evento.key
        
        # Mapeo directo de flujos de interrupción de estados
        if tecla_pulsada == pygame.K_r:
            return "menu"
        elif tecla_pulsada == pygame.K_ESCAPE:
            return "salir"
            
        return None

    def dibujar(self, escenario):
        # Lienzo oscuro para mantener la atmósfera minimalista
        self.pantalla.fill((15, 15, 15))

        # ── CABECERA ASIMÉTRICA DE FINALIZACIÓN ──
        # Desplazado a la izquierda superior en lugar de centrado absoluto
        titulo = self.fuente_big.render("SESIÓN FINALIZADA", True, (240, 70, 70))
        self.pantalla.blit(titulo, (60, 90))

        # Indicador secundario del entorno de simulación ejecutado
        metadato_entorno = f"Módulo: {escenario.nombre.upper()}"
        nombre_esc = self.fuente_chica.render(metadato_entorno, True, (110, 110, 110))
        self.pantalla.blit(nombre_esc, (60, 145))

        # ── PANEL DE METRICAS (PUNTAJES ALINEADOS A LA DERECHA) ──
        # Movimiento de los resultados hacia un bloque lateral derecho para balance de pesos
        X_PANEL_PUNTOS = ANCHO - 450
        
        for idx, chef in enumerate(escenario.chefs):
            color_etiqueta = COLOR_CHEF1 if idx == 0 else COLOR_CHEF2
            formato_registro = f"Chef {idx + 1} ({chef.nombre}): {chef.puntos} pts"
            
            texto_render = self.fuente_med.render(formato_registro, True, color_etiqueta)
            self.pantalla.blit(texto_render, (X_PANEL_PUNTOS, 240 + (idx * 60)))

        # ── SECCIÓN DE AGREGACIÓN DE RESULTADOS (TOTALES) ──
        conteo_chefs = len(escenario.chefs)
        
        if conteo_chefs > 1:
            # Cálculo procedimental acumulativo del espacio de estados
            puntaje_acumulado = sum(c.puntos for c in escenario.chefs)
            
            linea_total = self.fuente_med.render(f"Rendimiento Global: {puntaje_acumulado} pts", True, (220, 220, 220))
            y_offset_total = 240 + (conteo_chefs * 60) + 20
            
            # Línea divisoria minimalista para el totalizador horizontal
            pygame.draw.line(self.pantalla, (40, 40, 40), (X_PANEL_PUNTOS, y_offset_total - 10), (ANCHO - 60, y_offset_total - 10), 1)
            self.pantalla.blit(linea_total, (X_PANEL_PUNTOS, y_offset_total))

        # ── REGISTRO DE INSTRUCCIONES DEL TERMINAL (BAJO A LA IZQUIERDA) ──
        leyenda_sistema = "[ R: REINICIAR MENÚ ]   •   [ ESC: TERMINAR PROCESO ]"
        inst = self.fuente_chica.render(leyenda_sistema, True, (70, 70, 70))
        self.pantalla.blit(inst, (60, ANCHO // 2 + 120))