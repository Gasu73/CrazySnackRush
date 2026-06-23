import time
import threading
import random

class CocinaEscenario:
    def __init__(self, nombre, chefs, estaciones, 
    recetas_posibles, tiempo_juego=120, intervalo_recetas=15, max_recetas_activas=3):
        
        self.nombre = nombre
        self.chefs = chefs                          # List[Chef]
        self.estaciones = estaciones                # List[Estacion] no se usa
        self.recetas_posibles = recetas_posibles    # recetas predefinidas del escenario
        self.ordenes = []                           # recetas activas en pantalla
        
        self.tiempo_juego = tiempo_juego            # segundos totales
        self.tiempo_restante = tiempo_juego
        self.intervalo_recetas = intervalo_recetas  # cada cuántos segundos aparece una receta
        self.max_recetas_activas = max_recetas_activas


        
        self.activo = False
        self._lock = threading.Lock()               # evita conflictos entre hilos
    


    #  GENERACIÓN DE RECETAS
    def generar_receta(self):
        #Retorna una copia aleatoria de las recetas posibles del escenario

        plantilla = random.choice(self.recetas_posibles) #Elige una receta de la lista de recetas posibles
        
        from modelo.receta import Receta
        
        nueva = Receta(
            nombre=plantilla.nombre,
            ingredientes=[type(i)(i.nombre) for i in plantilla.lista_ingredientes],
            puntos_base=plantilla.puntos_receta,
            tiempo_max=plantilla.max_time_receta
        )
        return nueva
    
    def _loop_generar_recetas(self):
        #Hilo que genera recetas periódicamente mientras quede tiempo

        while self.activo and self.tiempo_restante > 0:
            
            time.sleep(self.intervalo_recetas)
            
            if not self.activo:
                break
            
            with self._lock:
                if len(self.ordenes) < self.max_recetas_activas:
                    nueva = self.generar_receta()
                    self.ordenes.append(nueva) 
                    

    
  
    #  TEMPORIZADOR GLOBAL
    
    def _loop_temporizador(self):
        
        while self.activo and self.tiempo_restante > 0:
            time.sleep(1)
            self.tiempo_restante -= 1


        if self.tiempo_restante <= 0:
            self.activo = False
            self._fin_partida()



    

    #  PENALIZACIONES DE RECETAS
    def _loop_penalizaciones(self):


        while self.activo:
            time.sleep(1)
            
            with self._lock:
                eliminadas = []
                
                for receta in self.ordenes:
                    receta.tiempo_transcurrido += 1
                    
                    # Si supera el tiempo máximo, se penaliza a todos los chefs y se elimina la receta
                    if receta.tiempo_transcurrido >= receta.max_time_receta:

                        receta.reducir_puntos()
                        receta.tiempo_transcurrido = 0    # reinicia el contador
                        
                        if not receta.activa:
                            eliminadas.append(receta)
                            print(f"\nReceta '{receta.nombre}' expiró. "f"Se descuentan puntos.")
                            self._penalizar_chefs(receta)

                
                for r in eliminadas:
                    self.ordenes.remove(r)  #Elimina si la receta ya no es activa

                    
    
    def _penalizar_chefs(self, receta):
        #Descuenta a todos los chefs el valor original de la receta

        penalizacion = receta.puntos_receta

        for chef in self.chefs:
            chef.agregar_puntos(-penalizacion)
            print(f"{chef.nombre} pierde {penalizacion} puntos.")
    


    
    def intentar_entrega(self, chef, ingredientes_entregados):

        with self._lock:
         
            for receta in self.ordenes:
         
                if receta.comparar_receta(ingredientes_entregados):


                    puntos = receta.puntos_receta
                    chef.agregar_puntos(puntos)
                    
                    self.ordenes.remove(receta)

                    print(f"\nReceta '{receta.nombre}' entregada "f"+{puntos} puntos para {chef.nombre}.")


                    return True
            
            print(f"\nLos ingredientes no coinciden con ninguna receta activa.")
            return False
 

    #  INICIO Y FIN DE PARTIDA
    
    def iniciar(self):
        #Arranca todos los hilos y comienza la partida

        self.activo = True
        
        # Primera receta inmediata
        primera = self.generar_receta()
        self.ordenes.append(primera)

        
        # Lanzar hilos
        hilos = [
            threading.Thread(target=self._loop_temporizador,    daemon=True),
            threading.Thread(target=self._loop_generar_recetas, daemon=True),
            threading.Thread(target=self._loop_penalizaciones,  daemon=True),
        ]
        for h in hilos:
            h.start()
    
    def _fin_partida(self):
        print("\n¡Tiempo terminado! Fin de la partida.")
        self.mostrar_puntajes()
    
    def detener(self):
        self.activo = False
