import random

import mesa

import model
from agents import Aeropuerto, Avion
from scheduler import RandomActivationByTypeFiltered


class TraficoAereo(mesa.Model):

    listado_aeropuertos = ""
    listado_aviones = ""

    verbose = False  # Print-monitoring

    description = (
        "Modelo para la simulación del tráfico aéreo."
    )

    def __init__(
            self,
            cuadricula=20,
            dias=5,
            aeropuertos_inicial=5,
            aviones_inicial=5,
            pistas_min=1,
            pistas_max=5,
            tiempo_despegue_aterrizaje=2,
            velocidad_media=4,
            distancia_km=3,
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
        self.velocidad_media = velocidad_media
        self.distancia_km = distancia_km
        self.control_colisiones = control_colisiones

        self.schedule = RandomActivationByTypeFiltered(self)
        # self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Aeropuertos": lambda m: m.schedule.get_type_count(Aeropuerto),
                "Aviones": lambda m: m.schedule.get_type_count(Avion),
            }
        )

        # Creacion de los aeropuertos:
        for i in range(self.aeropuertos_inicial):
            x = self.random.randrange(self.width)  # posicionamiento aleatorio
            y = self.random.randrange(self.height)
            numero_pistas = random.randint(pistas_min, pistas_max)
            tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje
            aeropuerto = Aeropuerto(self.next_id(), (x, y), numero_pistas, tiempo_despegue_aterrizaje, self, False)
            # Mostramos por consola las variables
            print(aeropuerto.imprimir_agente())
            self.listado_aeropuertos += aeropuerto.imprimir_agente() + '<br>'

            self.grid.place_agent(aeropuerto, (x, y))
            self.schedule.add(aeropuerto)

        # Creacion de los aviones:
        for i in range(self.aviones_inicial):
            # Seleccion de aeropuerto salida y llegada
            salida = self.random.randint(1, aeropuertos_inicial)
            # Determinación aeropuerto de llegada distinto que el de salida
            llegada = self.random.randint(1, aeropuertos_inicial)
            while llegada == salida:
                llegada = self.random.randint(1, aeropuertos_inicial)
            # posicionamiento según aeropuerto de salida
            #x = self.random.randrange(self.width)  # posicionamiento aleatorio
            #y = self.random.randrange(self.height)
            x = self.schedule._agents[salida].pos[0]
            y = self.schedule._agents[salida].pos[1]
            avion = Avion(self.next_id(), (x, y), salida, llegada, tiempo_despegue_aterrizaje, self, False)

            # Mostramos por consola las variables
            print(avion.imprimir_agente())
            self.listado_aviones += avion.imprimir_agente() + "<br>"

            self.grid.place_agent(avion, (x, y))
            self.schedule.add(avion)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
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

    def run_model(self, step_count=200):
        if self.verbose:
            print("Número de aeropuertos: ", self.schedule.get_type_count(Aeropuerto))
            print("Número de aviones : ", self.schedule.get_type_count(Avion))

        for i in range(step_count):
            self.step()
