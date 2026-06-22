# main.py
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

# Vector de inicializadores abstractos (Fábricas de entornos funcionales)
CONSTRUCTORES_ESCENARIO = [crear_escenario1, crear_escenario2, crear_escenario3]

def _inicializar_entorno_juego(pantalla, indice_escenario):
    """
    Función utilitaria para el cambio de estado (State Transition Setup).
    Encapsula la instanciación de dependencias y el acoplamiento de entidades.
    """
    # Instanciación polimórfica de los personajes con sus coordenadas en el Grid base
    lista_chefs = [Chef("Mario", 2, 4), Chef("Luigi", 8, 4)]
    
    # Invocación dinámica mediante el patrón Factory Pattern indexado
    funcion_fabrica = CONSTRUCTORES_ESCENARIO[indice_escenario]
    escenario_activo = funcion_fabrica(lista_chefs)
    
    # Inicialización del hilo de ejecución del sub-sistema (Timer interno del escenario)
    escenario_activo.iniciar()
    
    # Orquestación de subsistemas de la capa visual y controlador
    motor_grafico = Renderer(pantalla, indice_escenario)
    interfaz_hud   = HUD(pantalla)
    manejador_io   = Controles(escenario_activo)
    
    return escenario_activo, motor_grafico, interfaz_hud, manejador_io

def main():
    # Inicialización del subsistema multimedia de Hardware (SDL backend)
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()

    # Variables de Control de Estado de la Máquina de Estados Finita (FSM)
    estado_fsm = "inicio"  # Estados válidos: 'inicio' | 'jugando' | 'fin'
    escenario = None
    renderer = controles = hud = None
    
    # Instanciación previa de las capas de presentación de las pantallas externas
    pantalla_inicio = PantallaInicio(pantalla)
    pantalla_fin    = PantallaFin(pantalla)
    
    # Carga masiva preventiva en memoria persistente de texturas de disco (Assets Cache)
    cargar_imagenes()

    # ------------------------------------------------------------------------
    #  BUCLE PRINCIPAL DE EJECUCIÓN (MAIN GAME LOOP)
    # ------------------------------------------------------------------------
    while True:
        
        # --- BLOQUE DE PROCESAMIENTO DE INTERRUPCIONES Y ENTRADAS (EVENT LOOP) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Cierre seguro: previene hilos huérfanos deteniendo los procesos del escenario
                if escenario is not None:
                    escenario.detener()
                pygame.quit()
                sys.exit()

            # Evaluación de comportamiento según el estado actual de la FSM
            if estado_fsm == "inicio":
                seleccion_indice = pantalla_inicio.manejar_evento(evento)
                
                # Verificación de confirmación por el usuario (Transition Trigger)
                if seleccion_indice is not None:
                    # Desacoplamiento de la inicialización de módulos mediante inyección controlada
                    escenario, renderer, hud, controles = _inicializar_entorno_juego(pantalla, seleccion_indice)
                    estado_fsm = "jugando"

            elif estado_fsm == "jugando":
                # Delegación de eventos de entrada por teclado al módulo IO especializado
                controles.procesar_evento(evento)

            elif estado_fsm == "fin":
                comando_retorno = pantalla_fin.manejar_evento(evento)
                
                # Gestión de bifurcación pos-partida
                if comando_retorno == "menu":
                    estado_fsm = "inicio"
                    escenario = None  # Liberación de memoria eliminando la referencia del objeto previo
                elif comando_retorno == "salir":
                    pygame.quit()
                    sys.exit()

        # --- BLOQUE DE DESPACHO GRÁFICO (PIPELINE DE RENDERIZADO PROCEDIMENTAL) ---
        # Definición de un diccionario de llamadas directas para desacoplar el dibujo de la lógica de negocio
        # Evita una cadena redundante de ifs anidados en el ciclo de reloj crítico
        if estado_fsm == "inicio":
            pantalla_inicio.dibujar()
            
        elif estado_fsm == "jugando":
            # Limpieza del buffer de pantalla previo para evitar ghosting de texturas
            pantalla.fill(COLOR_FONDO)
            
            # Dibujo secuencial por capas de profundidad (Layer-based compositing)
            renderer.dibujar_grid()                                      # Capa 0: Fondo ortogonal
            renderer.dibujar_estaciones(escenario.estaciones)             # Capa 1: Entidades rígidas
            renderer.dibujar_chefs(escenario.chefs)                       # Capa 2: Personajes dinámicos
            hud.dibujar(escenario, controles.chef_activo)                 # Capa 3: UI de monitoreo e información
            
            # Evaluación del ciclo de vida del escenario (Condición de fin de juego)
            if not escenario.activo:
                estado_fsm = "fin"

        elif estado_fsm == "fin":
            pantalla_fin.dibujar(escenario)

        # --- SINCRONIZACIÓN DE HARDWARE Y CONTROL DE FRAME RATE ---
        # Intercambio de buffers de video (Double Buffering) para prevenir screen tearing
        pygame.display.flip()
        
        # Limitador estricto de frecuencia de refresco basado en reloj de hardware
        reloj.tick(FPS)

if __name__ == "__main__":
    main()