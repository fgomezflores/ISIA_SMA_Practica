import mesa
from walker import Walker
import math
def get_distance(pos_1, pos_2):
    """Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.
    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class Aeropuerto(Walker):
    """
    Origen y destino de cada vuelo
    """

    def __init__(self, unique_id, pos, numero_pistas, tiempo_despegue_aterrizaje, model, moore):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.id = unique_id  # Identificador del aeropuerto
        self.pos = pos
        self.numero_pistas = numero_pistas
        self.tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje

    def imprimir_agente(self):
        return "AEROPUERTO ID: "+ str(self.id) + " | Num. pistas: " + str(self.numero_pistas) +\
            " | Tiempo desp/aterr.: " + str(self.tiempo_despegue_aterrizaje) +\
            " | Coord.: " + str(self.pos)


class Avion(Walker):
    """
    Avion que cubirá la misma ruta entre aeropuerto de salida y llegada
    """

    def __init__(self, unique_id, pos, salida, llegada, tiempo_espera, model, moore=False):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.id = unique_id
        self.pos = pos
        self.salida = salida
        self.llegada = llegada
        self.tiempo_espera = tiempo_espera

    def step(self):
        self.random_move()

    def imprimir_agente(self):
        return "AVION ID: " + str(self.id) + " | Salida: " + str(self.salida) + " | Llegada: " +\
            str(self.llegada) + " | Tiempo espera: " + str(self.tiempo_espera) +\
            " | Coord.: " + str(self.pos)
