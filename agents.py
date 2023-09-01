import mesa
from walker import Walker

class Aeropuerto(Walker):
    """
    Origen y destino de cada vuelo
    """

    def __init__(self, unique_id, pos, pistas, tiempo_despegue_aterrizaje, model, moore):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.id = unique_id  # Identificador del aeropuerto
        self.pos = pos
        self.pistas = pistas
        self.pistas_disponibles = pistas
        self.tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje

    def imprimir_agente(self):
        return "AEROPUERTO ID: "+ str(self.id) + " | Num. pistas: " + str(self.pistas) +\
            " | Tiempo desp/aterr.: " + str(self.tiempo_despegue_aterrizaje) +\
            " | Coord.: " + str(self.pos)

    def step(self):
        return None


class Avion(Walker):
    """
    Avion que cubirá la misma ruta entre aeropuerto de origen y destino
    """

    def __init__(self, unique_id, pos, origen, destino, pos_destino, tiempo_espera, model, moore=False):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.id = unique_id # id del avion
        self.origen = origen # aeropuero de origen
        self.destino = destino # aeropuerto de destino
        self.pos = pos # posicion del avion
        self.pos_origen = pos  # posicion de aeropuerto de destino
        self.pos_destino = pos_destino # posicion de aeropuerto de destino
        self.tiempo_espera = tiempo_espera
        # true: vuelo aeropuerto de origen -> destino
        # false: vuelo aeropuerto de destino -> origen
        self.viaje_ida = True

    def step(self):
        self.volar_aeropuerto()

    def imprimir_agente(self):
        return "AVION ID: " + str(self.id) + " | origen: " + str(self.origen) + " | destino: " +\
            str(self.destino) + " | Tiempo espera: " + str(self.tiempo_espera) +\
            " | Coord. origen: " + str(self.pos) + " | Coord. destino: " + str(self.pos_destino)
