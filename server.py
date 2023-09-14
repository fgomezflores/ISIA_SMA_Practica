import mesa

from agents import Aeropuerto, Avion
from model import TraficoAereo

def obtener_listado_aeropuertos(model):
    return f"<b>Listado de Aeropuertos:</b> <br> {model.listado_aeropuertos}"

def obtener_listado_aviones(model):
    return f"<b>Listado de Aviones:</b> <br> {model.listado_aviones}"

# Función auxiliar para solicitar por pantalla el tamaño de la cuadricula
def winput(title, sentence):
    import tkinter as tk
    from tkinter import simpledialog
    tk.Tk().withdraw()
    y = simpledialog.askinteger(title, sentence)
    return y

# Clase auxiliar para poder mostrar texto explicativo en pantalla HTML
# sobre la gráfica ya que las leyendas de los valores aparecen como "undefined"
class TextoExplicativo(mesa.visualization.TextElement):
    def __init__(self):
        super().__init__()
        pass
    def render(self, model):
        return f"<label style='color:#0000FF; font-weight: bold'>Azul</label>: Tiempo espera total de aviones y en aeropuertos <br>" + \
            "<label style='color:#FF0000; font-weight: bold'>Rojo</label>: Tiempo total empleado en recorrer la distancia según velocidades de los aviones y tamaño de la cuadrícula"

def TraficoAereoRepresentacion(agent):

    if agent is None:
        return

    representacion = {}

    if type(agent) is Aeropuerto:
        #representacion["Shape"] = "recursos/aeropuerto.png"
        #representacion["scale"] = 0.9
        representacion["Shape"] = "rect"
        representacion["Filled"] = "true"
        representacion["Color"] = "Red"
        representacion["Layer"] = 1
        representacion["text"] = agent.id
        representacion["text_color"] = "White"
        representacion["w"] = 1
        representacion["h"] = 1
    elif type(agent) is Avion:
        representacion["Shape"] = "recursos/avion.png"
        representacion["scale"] = 0.9
        representacion["Layer"] = 2
        representacion["text"] = agent.id

    return representacion


# El tamaño de la cuadricula se establece al iniciar la simulacion
while True:
  try:
    cuadricula = winput("SMA", "Tamaño de la cuadrícula del mundo virtual (ancho x alto)\n\nIntroduce un número entre 10 y 30: ")
    if 10 <= cuadricula <= 30:
        break
    raise ValueError()
  except ValueError:
    print("La entrada tiene que se un número entre 10 y 30.")

print ("Se establece el tamaño de la cuadrícula en " + str(cuadricula))

model_params = {
    "title": mesa.visualization.StaticText("Parámetros:"),
    #"cuadricula": mesa.visualization.Slider("Tamaño de la cuadrícula", 20, 10, 30),
    "cuadricula": cuadricula,
    "dias": mesa.visualization.Slider("Núm. días total", 1, 1, 3),
    "aeropuertos_inicial": mesa.visualization.Slider("Núm. de aeropuertos", 5, 1, 10),
    "aviones_inicial": mesa.visualization.Slider("Núm. de aviones", 5, 1, 10),
    "pistas_min": mesa.visualization.Slider("Núm. pistas mínimo", 1, 1, 5),
    "pistas_max": mesa.visualization.Slider("Núm. pistas máximo", 1, 1, 5),
    "tiempo_despegue_aterrizaje": mesa.visualization.Slider("Tiempo transcurre despegue / aterrizaje", 2, 1, 5),
    "tiempo_espera_avion": mesa.visualization.Slider("Tiempo de espera del avion", 1, 1, 5),
    "velocidad_media": mesa.visualization.Slider("Velocidad media avión (kms./min)",
                                                 int((TraficoAereo.VELOCIDAD_MIN+TraficoAereo.VELOCIDAD_MAX)/2),
                                                 TraficoAereo.VELOCIDAD_MIN, TraficoAereo.VELOCIDAD_MAX, 100),
    "velocidad_diferente": mesa.visualization.Checkbox("Cada avión tendrá velocidad diferente", False),
    "control_colisiones": mesa.visualization.Checkbox("Control de colisiones", False),
    "distancia_km": mesa.visualization.Slider("Distacia kms. de cada cuadrícula", TraficoAereo.DISTANCIA_KM, 500, 1500, 100),
}

canvas_element = mesa.visualization.CanvasGrid(TraficoAereoRepresentacion, cuadricula, cuadricula, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Espera", "Color": "#0000FF"},
        {"Label": "Velocidad", "Color": "#FF0000"}
    ]
)

texto_explicativo=TextoExplicativo()

server = mesa.visualization.ModularServer(
    TraficoAereo,
    [canvas_element, chart_element, texto_explicativo, obtener_listado_aeropuertos, obtener_listado_aviones],
    "Simulación del Tráfico Aéreo",
    model_params,
)
server.port = 8521