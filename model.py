import random
import mesa

from agents import Aeropuerto, Avion

VERBOSE = False # Print-monitoring

# Función auxiliar para el datacollector y su visualización gráfica
def calcular_tiempo_espera_total(model):
    total = 0
    for a in model.schedule.agents:
        if type(a) is Avion:
            total += a.tiempo_espera_total
    return total

def calcular_tiempo_velocidad_total(model):
    total = 0
    for a in model.schedule.agents:
        if type(a) is Avion:
            total += a.tiempo_velocidad_total
    return total


class TraficoAereo(mesa.Model):

    # Variables auxiliares con texto que se mostrará en la visualización HTML del modelo
    listado_aeropuertos = ""
    listado_aviones = ""

    verbose = VERBOSE  # Print-monitoring

    description = (
        "Modelo para la simulación del tráfico aéreo"
    )


    # VELOCIDAD MÍNIMA Y MAXIMA DEL AVIÓN
    VELOCIDAD_MIN = 500
    VELOCIDAD_MAX = 1000
    # DISTANCIA KM CUADRICULA
    DISTANCIA_KM = 750

    def __init__(
            self,
            cuadricula = 20,
            dias=1,
            aeropuertos_inicial=5,
            aviones_inicial=5,
            pistas_min=1,
            pistas_max=1,
            tiempo_despegue_aterrizaje=2,
            tiempo_espera_avion=2,
            velocidad_media=int((VELOCIDAD_MIN+VELOCIDAD_MAX)/2),
            distancia_km=DISTANCIA_KM,
            control_colisiones=False,
            velocidad_diferente = False,
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
        :param velocidad_diferente: Cada avión tendrá una velocidad diferente
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
        self.control_colisiones = control_colisiones # booleano
        self.velocidad_diferente = velocidad_diferente # booleano

        self.schedule = mesa.time.RandomActivation(self)
        #self.schedule = mesa.time.StagedActivation(self)

        # Indicamos que el grid tenga la propiedad torus a false
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.datacollector = mesa.DataCollector(
            {
                "Espera": calcular_tiempo_espera_total,
                "Velocidad": calcular_tiempo_velocidad_total,
            }
        )

        # Numero total de días
        self.countdown = self.dias * 1440  # minutos que tiene un día

        # Creacion de los aeropuertos:
        for i in range(self.aeropuertos_inicial):
            # Posicionamiento aleatorio en la cuadrícula
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            # Número de pistas aleatorio entre los rangos de los parámetros
            pistas = random.randint(pistas_min, pistas_max)
            # Tiempo de aterrizaje y despegue establecido
            tiempo_despegue_aterrizaje = tiempo_despegue_aterrizaje
            #  Creación del agentge
            aeropuerto = Aeropuerto(self.next_id(), (x, y), pistas, tiempo_despegue_aterrizaje, self)
            # Mostramos por consola las variables
            print(aeropuerto.imprimir_agente())
            self.listado_aeropuertos += aeropuerto.imprimir_agente() + '<br>'
            # Se situa en la cuadrícula
            self.grid.place_agent(aeropuerto, (x, y))
            # Se añade al planificador
            self.schedule.add(aeropuerto)

        # Creacion de los aviones:
        for i in range(self.aviones_inicial):
            # Seleccion de aeropuerto salida de forma aleatoria
            salida = self.random.randint(1, aeropuertos_inicial)
            # Seleccion aeropuerto de llegada distinto que el de salida
            llegada = self.random.randint(1, aeropuertos_inicial)
            while llegada == salida:
                llegada = self.random.randint(1, aeropuertos_inicial)
            # posicionamiento según aeropuerto de salida que se le ha asignado
            x = self.schedule._agents[salida].pos[0]
            y = self.schedule._agents[salida].pos[1]
            x_llegada = self.schedule._agents[llegada].pos[0]
            y_llegada = self.schedule._agents[llegada].pos[1]
            # Velocidad: valor distancia cuadricula / velocidad del avion
            velocidad = 0
            # Si velocidad = 1 el avión recorre en 1 min (1 step) la distancia de la cuadricula
            # Si velocidad > 1 el avión no recorre en 1 minuto la distancia de la cuadricula
            # Si velocidad < 1 el avión recorre antes de 1 minuto la distancia de la cuadrícula
            if self.velocidad_diferente:
                # Para calcular la velocidad diferente, se opta por un número aleatorio
                # entre 50 y 150, valores minimo y máximo del slider en la visualizacion
                velocidad = round(self.DISTANCIA_KM / random.randrange(self.VELOCIDAD_MIN, self.VELOCIDAD_MAX), 1)
            else:
                velocidad = round(self.DISTANCIA_KM / self.velocidad_media, 1)
            avion = Avion(self.next_id(), (x, y), salida, llegada, (x_llegada, y_llegada), tiempo_espera_avion,
                          velocidad, self.control_colisiones, self, False)
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


