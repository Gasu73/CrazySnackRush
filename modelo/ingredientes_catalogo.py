from modelo.proteina import Proteina
from modelo.vegetal_fruta import VegetalesYFrutas
from modelo.pan_base import PanesYBases

#Escenario 1
def hacer_carne():        return Proteina("Carne")
def hacer_salchicha():    return Proteina("Salchicha")
def hacer_lechuga():      return VegetalesYFrutas("Lechuga")
def hacer_tomate():       return VegetalesYFrutas("Tomate")
def hacer_pan():          return PanesYBases("Pan")
def hacer_pan_hotdog():   return PanesYBases("Pan Hotdog")

#Escenario 2
def hacer_salmon():       return Proteina("Salmón")
def hacer_atun():         return Proteina("Atún")
def hacer_pepino():       return VegetalesYFrutas("Pepino")
def hacer_aguacate():     return VegetalesYFrutas("Aguacate")
def hacer_arroz():        return PanesYBases("Arroz")
def hacer_alga():         return PanesYBases("Alga Nori")

#Escenario 3
def hacer_pollo():        return Proteina("Pollo")
def hacer_pepperoni():    return Proteina("Pepperoni")
def hacer_pimiento():     return VegetalesYFrutas("Pimiento")
def hacer_cebolla():      return VegetalesYFrutas("Cebolla")
def hacer_masa():         return PanesYBases("Masa")
def hacer_queso():        return PanesYBases("Queso")