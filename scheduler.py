from typing import Callable, Optional, Type

import mesa

class RandomActivationByTypeFiltered(mesa.time.RandomActivationByType):
    """
    Programador que anula el método get_type_count para permitir el filtrado de agentes mediante una función antes de contar

    Ejemplo:
    >>> scheduler = RandomActivationByTypeFiltered(model)
    >>> scheduler.get_type_count(AgentA, lambda agent: agent.some_attribute > 10)

    """

    def get_type_count(
            self,
            type_class: Type[mesa.Agent],
            filter_func: Optional[Callable[[mesa.Agent], bool]] = None,
    ) -> int:
        """
        Returns the current number of agents of certain type in the queue
        that satisfy the filter function.
        """
        count = 0
        for agent in self.agents_by_type[type_class].values():
            if filter_func is None or filter_func(agent):
                count += 1
        return count