from escenarios.cocina_escenario import CocinaEscenario
from modelo.receta import Receta
from modelo.proteina import Proteina
from modelo.vegetal_fruta import VegetalesYFrutas
from modelo.pan_base import PanesYBases
from estaciones.despensa import Despensa
from estaciones.tabla_cortar import TablaDeCortar
from estaciones.cocina_sartan import CocinaSartan
from estaciones.freidora import Freidora
from estaciones.estacion_entrega import EstacionEntrega

def crear_escenario1(chefs):
    
    # --- Recetas posibles (plantillas) ---

    Carne = Proteina("Carne")
    Salchicha = Proteina("Salchicha")
    Lechuga = VegetalesYFrutas("Lechuga")
    Tomate = VegetalesYFrutas("Tomate")
    Pan = PanesYBases("Pan")
    Pan_Hotdog = PanesYBases("Pan Hotdog")


    hamburguesa = Receta(
        nombre="Hamburguesa",
        ingredientes=[
            Carne,
            Lechuga,
            Pan
        ],
        puntos_base=150,
        tiempo_max=60
    )
    
    hotdog = Receta(
        nombre="Hotdog",
        ingredientes=[
            Salchicha,
            Pan_Hotdog
        ],
        puntos_base=100,
        tiempo_max=45
    )
    
    ensalada = Receta(
        nombre="Ensalada",
        ingredientes=[
            Lechuga,
            Tomate
        ],
        puntos_base=80,
        tiempo_max=40
    )
    
    recetas_posibles = [hamburguesa, hotdog, ensalada]
    
    # --- Estaciones ---
    estaciones = [
        Despensa(Carne),
        Despensa(Salchicha),
        Despensa(Lechuga),
        Despensa(Tomate),
        Despensa(Pan),
        Despensa(Pan_Hotdog),
        TablaDeCortar(),
        CocinaSartan(),
        Freidora(),
        EstacionEntrega([])     # la referencia a ordenes se conecta abajo
    ]

        # Posiciones en el grid
    posiciones = [
        (2, 2), (2, 3), (2, 5), (2, 7), (2, 8), (2, 10),
        (6, 4), (10, 4),
        (13, 4),
        (15, 6)
    ]
    for est, pos in zip(estaciones, posiciones):
        est.pos_x, est.pos_y = pos

    # Posiciones iniciales de chefs
    chefs[0].pos_x, chefs[0].pos_y = 4, 6
    chefs[1].pos_x, chefs[1].pos_y = 6, 6


    # --- Crear escenario ---
    escenario = CocinaEscenario(
        nombre="Restaurante Hamburguesas",
        chefs=chefs,
        estaciones=estaciones,
        recetas_posibles=recetas_posibles,
        tiempo_juego=120,
        intervalo_recetas=20,
        max_recetas_activas=4
    )
    
    # Conectar la EstacionEntrega a las órdenes activas
    estaciones[-1].recetas_activas = escenario.ordenes
    
    return escenario