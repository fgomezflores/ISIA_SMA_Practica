import random
import mesa
from agents import Aeropuerto, Avion

def calcular_kms(model):
    agent_wealths = [agent.id for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.aeropuertos_inicial
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

class TraficoAereo(mesa.Model):
    # Variables con texto que se mostrará en la visualización HTML del modelo
    listado_aeropuertos = ""
    listado_aviones = ""

    verbose = False  # Print-monitoring

    description = (
        "Modelo para la simulación del tráfico aéreo."
    )

    def __init__(
            self,
            cuadricula=20,
            dias=1,
            aeropuertos_inicial=5,
            aviones_inicial=5,
            pistas_min=1,
            pistas_max=1,
            tiempo_despegue_aterrizaje=2,
            tiempo_espera_avion=2,
            velocidad_media=4,
            distancia_km=100,
            control_colisiones=False,
    ):
        """
        Creación de un modelo para el tráfico aéreo para los siguientes parámetros
        :param cuadricula: Alto y ancho de la cuadrícula del mundo virtual
        :param dias: Número de días total que se simularán
        :param aeropuertos_inicial: Número de aeropuertos que se modelarán
        :param aviones_inicial: Número de aviones que se modelarán
        :param pistas_min: Número mínimo de pistas de aterrizado/despegue
        :param pistas_max: Número máximo de pistas de aterrizado/despegue
        :param tiempo_despegue_aterrizaje: Tiempo que debe transcurrir entre el despegue/aterrizaje entre aviones en cada pista
                (es siempre el mismo para todas las pistas de todos los aeropuertos)
        :param velocidad_media: Velocidad media de cada aeronave en km/min
        :param distancia_km: Distancia en kilómetros de cada cuadrícula
        :param control_colisiones: Controla la posibilidad de que dos o más aviones colisionen en el aire
        """

        super().__init__()

        # Se establecen los parámetros
        self.height = cuadricula
        self.width = cuadricula
        self.dias = dias
        self.aeropuertos_inicial = aeropuertos_inicial
        self.aviones_inicial = aviones_inicial
        self.pistas_min = pistas_min
        self.pistas_max = pistas_max
        self.tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje
        self.tiempo_espera_avion = tiempo_espera_avion
        self.velocidad_media = velocidad_media
        self.distancia_km = distancia_km
        self.control_colisiones = control_colisiones

        self.schedule = mesa.time.RandomActivation(self)

        # Indicamos que el grid tenga la propiedad torus a false
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.datacollector = mesa.DataCollector(
            {
                "Aviones": calcular_kms,
            }
        )

        # Numero total de días
        # self.countdown = self.dias * 1440  # minutos que tiene un día
        self.countdown = self.dias * 100  # minutos que tiene un día

        # Creacion de los aeropuertos:
        for i in range(self.aeropuertos_inicial):
            x = self.random.randrange(self.width)  # posicionamiento aleatorio
            y = self.random.randrange(self.height)
            pistas = random.randint(pistas_min, pistas_max)
            tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje
            aeropuerto = Aeropuerto(self.next_id(), (x, y), pistas, tiempo_despegue_aterrizaje, self, False)
            # Mostramos por consola las variables
            print(aeropuerto.imprimir_agente())
            self.listado_aeropuertos += aeropuerto.imprimir_agente() + '<br>'

            self.grid.place_agent(aeropuerto, (x, y))
            self.schedule.add(aeropuerto)

        # Creacion de los aviones:
        for i in range(self.aviones_inicial):
            # Seleccion de aeropuerto origen de forma aleatoria
            origen = self.random.randint(1, aeropuertos_inicial)
            # Seleccion aeropuerto de destino distinto que el de origen
            destino = self.random.randint(1, aeropuertos_inicial)
            while destino == origen:
                destino = self.random.randint(1, aeropuertos_inicial)
            # posicionamiento según aeropuerto de origen que se le ha asignado
            x = self.schedule._agents[origen].pos[0]
            y = self.schedule._agents[origen].pos[1]
            x_destino = self.schedule._agents[destino].pos[0]
            y_destino = self.schedule._agents[destino].pos[1]
            avion = Avion(self.next_id(), (x, y), origen, destino, (x_destino, y_destino), tiempo_espera_avion, self, False)
            # Mostramos por consola las variables
            print(avion.imprimir_agente())
            self.listado_aviones += avion.imprimir_agente() + "<br>"

            self.grid.place_agent(avion, (x, y))
            self.schedule.add(avion)

        self.running = True
        self.datacollector.collect(self)

    def step(self):

        if self.schedule.time < self.countdown:
            self.schedule.step()
            # Recogida de los datos
            self.datacollector.collect(self)
            if self.verbose:
                print(
                    [
                        self.schedule.time,
                        self.schedule.get_type_count(Aeropuerto),
                        self.schedule.get_type_count(Avion),
                    ]
                )
        else:
            # Se termina la simulacion
            print("--------> FIN DE LA SIMULACION")
            exit()


