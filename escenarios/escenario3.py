from escenarios.cocina_escenario import CocinaEscenario
from modelo.receta import Receta
from modelo.proteina import Proteina
from modelo.vegetal_fruta import VegetalesYFrutas
from modelo.pan_base import PanesYBases
from estaciones.despensa import Despensa
from estaciones.tabla_cortar import TablaDeCortar
from estaciones.cocina_sartan import CocinaSartan
from estaciones.freidora import Freidora
from estaciones.estacion_basura import EstacionBasura
from estaciones.estacion_ensamble import EstacionEnsamble
from estaciones.estacion_entrega import EstacionEntrega


def crear_escenario3(chefs):

    # --- Ingredientes ---

    Pollo = Proteina("Pollo")
    Pepperoni = Proteina("Pepperoni")

    Pimiento = VegetalesYFrutas("Pimiento")
    Cebolla = VegetalesYFrutas("Cebolla")

    Masa = PanesYBases("Masa")
    Queso = PanesYBases("Queso")

    # --- Recetas posibles ---

    pizza_margherita = Receta(
        nombre="Pizza Margherita",
        ingredientes=[
            Masa,
            Queso
        ],
        puntos_base=130,
        tiempo_max=45
    )

    pizza_pollo = Receta(
        nombre="Pizza Pollo",
        ingredientes=[
            Masa,
            Queso,
            Pollo,
            Pimiento
        ],
        puntos_base=220,
        tiempo_max=65
    )

    pizza_vegetal = Receta(
        nombre="Pizza Vegetal",
        ingredientes=[
            Masa,
            Queso,
            Pimiento,
            Cebolla
        ],
        puntos_base=200,
        tiempo_max=60
    )

    pizza_suprema = Receta(
        nombre="Pizza Suprema",
        ingredientes=[
            Masa,
            Queso,
            Pepperoni,
            Pollo,
            Pimiento,
            Cebolla
        ],
        puntos_base=350,
        tiempo_max=90
    )

    recetas_posibles = [
        pizza_margherita,
        pizza_pollo,
        pizza_vegetal,
        pizza_suprema
    ]

    entrega = EstacionEntrega()

    # --- Estaciones ---

    estaciones = [
        Despensa(Pollo),
        Despensa(Pepperoni),
        Despensa(Pimiento),
        Despensa(Cebolla),
        Despensa(Masa),
        Despensa(Queso),
        TablaDeCortar(),
        CocinaSartan(),
        EstacionBasura(),
        EstacionEnsamble(),
        entrega
    ]

    # Posiciones en el grid
    posiciones = [
        (2, 2), (2, 3), (2, 5), (2, 7), (2, 8), (2, 10),
        (6, 3), (10, 3),
        (13, 3),
        (10, 6),
        (14, 6) 
    ]

    for est, pos in zip(estaciones, posiciones):
        est.pos_x, est.pos_y = pos

    # Posiciones iniciales de chefs
    chefs[0].pos_x, chefs[0].pos_y = 5, 5
    chefs[1].pos_x, chefs[1].pos_y = 7, 5

    # --- Crear escenario ---

    escenario = CocinaEscenario(
        nombre="Restaurante Pizza 🍕",
        chefs=chefs,
        estaciones=estaciones,
        recetas_posibles=recetas_posibles,
        tiempo_juego=180,
        intervalo_recetas=15,
        max_recetas_activas=4
    )

    # Conectar la estación de entrega con el escenario
    entrega.cocina = escenario

    # Conectar las órdenes activas
    entrega.recetas_activas = escenario.ordenes

    return escenario