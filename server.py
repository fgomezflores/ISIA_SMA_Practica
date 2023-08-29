import mesa

from agents import Aeropuerto, Avion
from model import TraficoAereo

def TraficoAereoRepresentacion(agent):

    if agent is None:
        return

    representacion = {}

    if type(agent) is Aeropuerto:
        representacion["Shape"] = "recursos/aeropuerto.png"
        representacion["scale"] = 0.9
        representacion["Layer"] = 1
    elif type(agent) is Avion:
        representacion["Shape"] = "recursos/avion.png"
        representacion["scale"] = 0.9
        representacion["Layer"] = 2
        #representacion["text"] = round(agent.energy, 1)
        #representacion["text_color"] = "Blue"

    return representacion


canvas_element = mesa.visualization.CanvasGrid(TraficoAereoRepresentacion, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Aeropuertos", "Color": "#AA0000"},
        {"Label": "Aviones", "Color": "#666666"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parámetros:"),
    "aeropuertos_inicial": mesa.visualization.Slider(
        "Aeropuertos inicial", 100, 10, 300
    ),
    "aviones_inicial": mesa.visualization.Slider("Aviones inicial", 50, 10, 300),
}

server = mesa.visualization.ModularServer(
    TraficoAereo, [canvas_element, chart_element], "Simulación del Tráfico Aéreo", model_params
)
server.port = 8521
