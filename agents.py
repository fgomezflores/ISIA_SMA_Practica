import mesa

from walker import Walker
from threading import Timer

VERBOSE = False # Print-monitoring

class Aeropuerto(Walker):
    """
    Origen y destino de cada vuelo
    """

    verbose = VERBOSE  # Print-monitoring

    def __init__(self, unique_id, pos, pistas, tiempo_despegue_aterrizaje, model):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model)
        # Crea las variables del agente y establece los valores inciales
        self.id = unique_id  # Identificador del aeropuerto
        self.pos = pos
        self.pistas = pistas
        self.pistas_disponibles = pistas
        # Tiempo que debe transcurrir entre el despegue y aterrizaje de un avión y el siguiente
        self.tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje
        self.countdown = tiempo_despegue_aterrizaje # inciamos contador tipo cuenta atrás para poder asignar pista
        self.avion_autorizado = -1

     # Función que ejecuta el agente al moverse
    def step(self):
        if self.countdown < 0:
            # Listado de agentes en el aeropuerto
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            cellmates.pop(
                cellmates.index(self)
            )  # Nos aseguramos que no se autoriza al propio agente del aeropuerto (lo sacamos de la lista)
            if len(cellmates) > 0:
                for i in range(0, len(cellmates)):
                    if type(cellmates[i]) is Avion:
                        autorizado = cellmates[i].id
                        if  self.model.schedule._agents[autorizado].autorizacion_solicitada:
                            self.avion_autorizado = autorizado
                            if self.verbose:
                                print("AEROPUERTO " + str(self.id)+ " autoriza maniobra al AVION " + str(self.avion_autorizado))
                            self.countdown = self.tiempo_despegue_aterrizaje
                            break
        elif self.countdown >= 0:
            if self.verbose:
                print("Countdown del AEROPUERTO " + str(self.id) + " tiempo de espera " + str(self.countdown))
            self.countdown -= 1

   # Devuelve cadena con los principales datos del aeropuerto para mostrar por pantalla
    def imprimir_agente(self):
        return "AEROPUERTO ID: "+ str(self.id) + " | Num. pistas: " + str(self.pistas) +\
            " | Tiempo desp/aterr.: " + str(self.tiempo_despegue_aterrizaje) +\
            " | Coord.: " + str(self.pos)


class Avion(Walker):
    """
    Avion que cubirá la misma ruta entre aeropuerto de origen y destino
    """

    verbose = VERBOSE  # Print-monitoring

    def __init__(self, unique_id, pos, origen, destino, pos_destino, tiempo_espera, velocidad, distancia_km, control_colisiones, model, moore=False):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.id = unique_id # id del avion
        self.origen = origen # aeropuero de origen
        self.destino = destino # aeropuerto de destino
        self.pos = pos # posicion del avion
        self.pos_origen = pos  # posicion de aeropuerto de destino
        self.pos_destino = pos_destino # posicion de aeropuerto de destino
        # true: vuelo aeropuerto de origen -> destino
        # false: vuelo aeropuerto de destino -> origen
        self.viaje_ida = True
        # Tiempo de espera en el aeropuerto
        self.tiempo_espera = tiempo_espera
        # Pista asignada despegue / aterrizaje (-1 =No asignada)
        self.pista_asignada = -1
        # Contador tipo cuenta atrás para poder despegar / aterrizar
        self.countdown = tiempo_espera
        # Autorización para despegar / aterrizar al aeropuerto
        self.autorizacion_solicitada = False
        # El avion está en trayecto
        self.en_vuelo = False
        self.velocidad = velocidad
        self.distancia_km = distancia_km
        self.tiempo_vuelo = 0
        self.control_colisiones = control_colisiones

    # Función que ejecuta el agente al moverse
    def step(self):
        # Según el tipo de vuelo se selecciona el id del aeropuerto
        # El procedimiento volar_aeropuerto() del modelo actualiza esta variable (en walker.py)
        if self.viaje_ida:
            id_aeropuerto = self.origen
        else:
            id_aeropuerto = self.destino

        # 1. Tiempo de espera del avion completado, está en el aeropuerto y
        # no ha solicitado todavía la autorización al aeropuerto
        if self.countdown <= 0 and not self.en_vuelo and not self.autorizacion_solicitada:
            if self.pista_asignada == -1:
                # Se solicita pista al aeropuerto
                if self.model.schedule._agents[id_aeropuerto].pistas_disponibles > 0:
                    self.pista_asignada = self.model.schedule._agents[id_aeropuerto].pistas_disponibles
                    self.model.schedule._agents[id_aeropuerto].pistas_disponibles -= 1
                    if self.verbose:
                        print ("AVION " + str(self.id) + " en AEROPUERTO " + str(id_aeropuerto) +\
                               " la asigna PISTA "+ str(self.pista_asignada) +\
                               " -> Solicita despegue/aterrizaje - Viaje de ida: " + str(self.viaje_ida))
                    # Se solicita autorizacion despegue / aterrizaje
                    self.autorizacion_solicitada = True
        # 2. Descuento del contador de espera del avion
        elif self.countdown > 0 and not self.en_vuelo and not self.autorizacion_solicitada:
            if self.verbose:
                print("Countdown del AVION " + str(self.id) + " en AEROPUERTO " + str(id_aeropuerto) + " tiempo de espera " + str(self.countdown))
            self.countdown -= 1
        # 3. Tiempo de espera del avion completado, está en el aeropuerto y
        # sí ha solicitado todavía la autorización al aeropuerto
        elif self.countdown <= 0 and not self.en_vuelo and self.autorizacion_solicitada:
            if self.model.schedule._agents[id_aeropuerto].avion_autorizado == self.id:
                if self.verbose:
                    print("AVION " + str(self.id) + " autorizado por AEROPUERTO " + str(id_aeropuerto))
                # Se despega
                self.en_vuelo = True
                # Se restablecen variables
                self.autorizacion_solicitada = False
                self.countdown = self.tiempo_espera
                self.pista_asignada = -1
                self.model.schedule._agents[id_aeropuerto].pistas_disponibles += 1
        # 4. Se encuentra en trayecto (no está en aeropuerto)
        elif self.en_vuelo:
            # Función que hace que se mueva el agente
            # Este procedimiento ya controla si es ida o vuelta
            # y actualiza el valor de la variable self.viaje_ida
            self.volar_aeropuerto(self.velocidad, self.control_colisiones)
            self.tiempo_vuelo += self.velocidad # es un ratio distancia / velocidad

    # Devuelve cadena con los principales datos del avión para mostrar por pantalla
    def imprimir_agente(self):
        return "AVION ID: " + str(self.id) + " | origen: " + str(self.origen) + " | destino: " +\
            str(self.destino) + " | Tiempo espera: " + str(self.tiempo_espera) +\
            " | Coord. origen: " + str(self.pos_origen) + " | Coord. destino: " + str(self.pos_destino) +\
            " | Ratio Distancia Cuadricula / Velocidad avion: " + str(self.velocidad)
