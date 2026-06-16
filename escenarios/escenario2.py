# escenarios/escenario2.py
from escenarios.cocina_escenario import CocinaEscenario
from modelo.chef import Chef
from modelo.receta import Receta
from modelo.ingredientes_catalogo import *
from estaciones.despensa import Despensa
from estaciones.tabla_cortar import TablaDeCortar
from estaciones.cocina_sartan import CocinaSartan
from estaciones.freidora import Freidora
from estaciones.estacion_entrega import EstacionEntrega
from modelo.proteina import Proteina
from modelo.vegetal_fruta import VegetalesYFrutas
from modelo.pan_base import PanesYBases

def crear_escenario2(chefs):

    # --- Ingredientes ---

    Salmon = Proteina("Salmón")
    Atun = Proteina("Atún")

    Pepino = VegetalesYFrutas("Pepino")
    Aguacate = VegetalesYFrutas("Aguacate")

    Arroz = PanesYBases("Arroz")
    Alga = PanesYBases("Alga")

    # --- Recetas posibles ---

    nigiri_salmon = Receta(
        nombre="Nigiri Salmón",
        ingredientes=[
            Salmon,
            Arroz
        ],
        puntos_base=120,
        tiempo_max=40
    )

    roll_pepino = Receta(
        nombre="Roll Pepino",
        ingredientes=[
            Pepino,
            Arroz,
            Alga
        ],
        puntos_base=160,
        tiempo_max=50
    )

    sashimi_atun = Receta(
        nombre="Sashimi Atún",
        ingredientes=[
            Atun,
            Aguacate
        ],
        puntos_base=140,
        tiempo_max=45
    )

    roll_especial = Receta(
        nombre="Roll Especial",
        ingredientes=[
            Salmon,
            Aguacate,
            Pepino,
            Arroz,
            Alga
        ],
        puntos_base=250,
        tiempo_max=70
    )

    recetas_posibles = [
        nigiri_salmon,
        roll_pepino,
        sashimi_atun,
        roll_especial
    ]

    # --- Estaciones ---

    estaciones = [
        Despensa(Salmon),
        Despensa(Atun),
        Despensa(Pepino),
        Despensa(Aguacate),
        Despensa(Arroz),
        Despensa(Alga),
        TablaDeCortar(),
        CocinaSartan(),
        Freidora(),
        EstacionEntrega([])      # la referencia a ordenes se conecta abajo
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

    escenario = CocinaEscenario(
        nombre="Restaurante Sushi 🍣",
        chefs=chefs,
        estaciones=estaciones,
        recetas_posibles=recetas_posibles,
        tiempo_juego=150,           # más tiempo por ser más difícil
        intervalo_recetas=18,
        max_recetas_activas=4
    )

    estaciones[-1].recetas_activas = escenario.ordenes
    return escenario