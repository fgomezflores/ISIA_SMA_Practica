import mesa
from mesa.visualization.modules import TextElement

import model
from agents import Aeropuerto, Avion
from model import TraficoAereo

def obtener_listado_aeropuertos(model):
    return f"<b>Listado de Aeropuertos:</b> <br> {model.listado_aeropuertos}"

def obtener_listado_aviones(model):
    return f"<b>Listado de Aviones:</b> <br> {model.listado_aviones}"

def obtener_mensaje_html(model):
    return f"<b>Avisos:</b> <br> {model.mensaje_html}"

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


canvas_element = mesa.visualization.CanvasGrid(TraficoAereoRepresentacion, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Aeropuertos", "Color": "#AA0000"},
        {"Label": "Aviones", "Color": "#666666"},
    ]
)

model_params = {
    "title": mesa.visualization.StaticText("Parámetros:"),
    "control_colisiones": mesa.visualization.Checkbox("Control de colisiones", False),
    "cuadricula": mesa.visualization.Slider("Tamaño de la cuadrícula", 20, 10, 30),
    "dias": mesa.visualization.Slider("Núm. días total", 5, 1, 10),
    "aeropuertos_inicial": mesa.visualization.Slider("Núm. de aeropuertos", 5, 1, 10),
    "aviones_inicial": mesa.visualization.Slider("Núm. de aviones", 5, 1, 10),
    "pistas_min": mesa.visualization.Slider("Núm. pistas mínimo", 1, 1, 5),
    "pistas_max": mesa.visualization.Slider("Núm. pistas máximo", 5, 1, 5),
    "tiempo_despegue_aterrizaje": mesa.visualization.Slider("Tiempo transcurre despegue / aterrizaje", 2, 1, 5),
    "tiempo_espera_avion": mesa.visualization.Slider("Tiempo de espera del avion", 1, 1, 5),
    "velocidad_media": mesa.visualization.Slider("Velocidad media aeronave", 5, 1, 5),
    "distancia_km": mesa.visualization.Slider("Distacia kms. de cada cuadrícula", 4, 1, 5),
}

server = mesa.visualization.ModularServer(
    TraficoAereo, [canvas_element, chart_element, obtener_mensaje_html, obtener_listado_aeropuertos, obtener_listado_aviones], "Simulación del Tráfico Aéreo", model_params
)
server.port = 8521
