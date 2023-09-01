"""
Comportamiento generalizado para caminar por la cuadrícula, una celda a la vez.
"""
import math
import mesa


def get_distance(pos_1, pos_2):
    """
    Obtiene la distancia entre dos puntos según
    la distancia Euclidea entre dos puntos

    Args:
        pos_1, pos_2: Coodenadas de las tuplas de ambos puntos
    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)

class Walker(mesa.Agent):
    """
    Clase que implementa métodos de caminante (walker) de manera generalizada.
    No está diseñado para usarse por sí solo, sino para heredar sus métodos a muchos otros agentes.
    """

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=False):
        """
        grid: El objeto MultiGrid en el que vive el agente.
        x: La coordenada x actual del agente.
        y: La coordenada y actual del agente.
        moore: Si es Verdadero, puede moverse en las 8 direcciones.
                De lo contrario, sólo arriba, abajo, izquierda, derecha.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def esta_ocupado(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return any(isinstance(agent, Walker) for agent in this_cell)

    def volar_aeropuerto(self):
        # Si es viaje de ida se vuela aeropuerto de origen -> destino
        # Sino destino -> origen
        if self.viaje_ida:
            next_moves = self.model.grid.get_neighborhood(self.pos_destino, self.moore, True)
        else:
            next_moves = self.model.grid.get_neighborhood(self.pos_origen, self.moore, True)

        # Reducir a los más cercanos
        min_dist = min(get_distance(self.pos, pos) for pos in next_moves)
        if min_dist > 0:
            while min_dist > 0:
                final_candidates = [
                    pos for pos in next_moves if get_distance(self.pos, pos) == min_dist
                ]
                next_move = final_candidates[0]
                next_moves = self.model.grid.get_neighborhood(next_move, self.moore, True)
                min_dist = min(get_distance(self.pos, pos) for pos in next_moves)

            self.model.grid.move_agent(self, next_move)
            self.pos = next_move
        elif min_dist == 0: # ha llegado
            if self.viaje_ida: # vuelo origen -> destino
                self.model.grid.move_agent(self, self.pos_destino)
                self.pos = self.pos_destino
                self.viaje_ida = False
            else: # vuelo destino -> origen
                self.model.grid.move_agent(self, self.pos_origen)
                self.pos = self.pos_origen
                self.viaje_ida = True


    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)