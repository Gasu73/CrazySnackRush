#ui/imagenes.py
import pygame


TAM_INGREDIENTE = (48, 48)

INGREDIENTES = [
    "Carne",
    "Salchicha",
    "Lechuga",
    "Tomate",
    "Pan",
    "Pan_Hotdog",
    "Salmón",
    "Atún",
    "Pepino",
    "Aguacate",
    "Arroz",
    "Alga_nori",
    "Pollo",
    "Pepperoni",
    "Pimiento",
    "Cebolla",
    "Masa",
    "Queso"
]

ESTADOS = [
    "crudo",
    "cortado",
    "cocinado",
    "listo"
]

imagenes_ingredientes = {}


TAM_RECETA = (48, 48)

RECETAS = [
    "Hamburguesa",
    "Hotdog",
    "Ensalada",
    "Nigiri Salmón",
    "Roll Pepino",
    "Sashimi Atún",
    "Roll Especial",
    "Pizza Margherita",
    "Pizza Pollo",
    "Pizza Vegetal",
    "Pizza Suprema"
]

imagenes_recetas = {}



def cargar_imagenes():
    for nombre in RECETAS:

        nombre_archivo = (
            nombre.lower()
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
            .replace(" ", "_")
        )
        try:
            imagenes_recetas[nombre] = pygame.transform.scale(
                pygame.image.load(
                    f"assets/ingredientes/receta_{nombre_archivo}.png"
                ).convert_alpha(),
                TAM_RECETA
            )

        except FileNotFoundError:
            print(f"⚠️  No se encontró la imagen para la receta {nombre} (assets/ingredientes/receta_{nombre_archivo}.png)")


    for nombre in INGREDIENTES:

        nombre_archivo = (
            nombre.lower()
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
            .replace(" ", "_")
        )

        for estado in ESTADOS:

            if estado == "listo":
                ruta = f"assets/ingredientes/ingrediente_{nombre_archivo}.png"
            else:
                ruta = f"assets/ingredientes/ingrediente_{nombre_archivo}_{estado}.png"

            try:
                imagenes_ingredientes[(nombre, estado)] = pygame.transform.scale(
                    pygame.image.load(ruta).convert_alpha(),
                    TAM_INGREDIENTE
                )   
            except FileNotFoundError:
                print(f"⚠️  No se encontró la imagen para {nombre} en estado {estado} ({ruta})")




    







