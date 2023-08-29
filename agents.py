import mesa
from walker import Walker

class Aeropuerto(Walker):
    """
    Origen y destino de cada vuelo
    """

    def __init__(self, unique_id, pos, model, moore):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.numero_pistas = 1

    def step(self):
        aeropuerto = Aeropuerto(
            self.model.next_id(), self.pos, self.model, self.moore
        )
        self.model.grid.place_agent(aeropuerto, self.pos)
        self.model.schedule.add(aeropuerto)


class Avion(Walker):
    """
    Avion que cubirá la misma ruta entre aeropuerto de salida y llegada
    """

    def __init__(self, unique_id, pos, model, moore):
        # Pasa los parámetros a la clase padre
        super().__init__(unique_id, pos, model, moore)
        # Crea las variables del agente y establece los valores inciales
        self.tiempo_espera = 5
