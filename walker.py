"""
Comportamiento generalizado para caminar por la cuadrícula, una celda a la vez.
"""

import mesa

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

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)