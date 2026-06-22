import pygame
import sys
from ui.constantes import *
from ui.renderer import Renderer
from ui.hud import HUD
from ui.controles import Controles
from ui.pantalla_inicio import PantallaInicio
from ui.pantalla_fin import PantallaFin
from modelo.chef import Chef
from escenarios.escenario1 import crear_escenario1
from escenarios.escenario2 import crear_escenario2
from escenarios.escenario3 import crear_escenario3
from ui.imagenes import cargar_imagenes



FABRICAS_ESCENARIO = [crear_escenario1, crear_escenario2, crear_escenario3]


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()

    estado = "inicio"       # inicio | jugando | fin
    escenario = None
    renderer = controles = hud = None
    pantalla_inicio = PantallaInicio(pantalla)
    pantalla_fin    = PantallaFin(pantalla)
    cargar_imagenes()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if escenario:
                    escenario.detener()
                pygame.quit()
                sys.exit()

            # ---- MENÚ DE INICIO ----
            if estado == "inicio":
                resultado = pantalla_inicio.manejar_evento(evento)


                if resultado is not None:
                    chefs = [Chef("Mario", 2, 4), Chef("Luigi", 8, 4)]

                    fabrica = FABRICAS_ESCENARIO[resultado]  #Guarda la función de creación del escenario elegido

                    escenario = fabrica(chefs) #Crea el escenario con los chefs (y sus puntos acumulados)


                    escenario.iniciar()
                    
                    renderer  = Renderer(pantalla, resultado)
                    hud       = HUD(pantalla)
                    controles = Controles(escenario)
                    estado    = "jugando"

            # ---- JUGANDO ----
            elif estado == "jugando":
                controles.procesar_evento(evento)

            # ---- FIN DE PARTIDA ----
            elif estado == "fin":
                resultado = pantalla_fin.manejar_evento(evento)
                if resultado == "menu":
                    estado = "inicio"
                    escenario = None
                elif resultado == "salir":
                    pygame.quit()
                    sys.exit()

        # ---- DIBUJAR ----
        if estado == "inicio":
            pantalla_inicio.dibujar()

        elif estado == "jugando":
            pantalla.fill(COLOR_FONDO)
            renderer.dibujar_grid()
            renderer.dibujar_estaciones(escenario.estaciones)
            renderer.dibujar_chefs(escenario.chefs)
            hud.dibujar(escenario, controles.chef_activo)

            if not escenario.activo:
                estado = "fin"

        elif estado == "fin":
            pantalla_fin.dibujar(escenario)

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()