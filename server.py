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
    # "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    # "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    # "initial_sheep": mesa.visualization.Slider(
    #     "Initial Sheep Population", 100, 10, 300
    # ),
    # "sheep_reproduce": mesa.visualization.Slider(
    #     "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    # ),
    # "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 50, 10, 300),
    # "wolf_reproduce": mesa.visualization.Slider(
    #     "Wolf Reproduction Rate",
    #     0.05,
    #     0.01,
    #     1.0,
    #     0.01,
    #     description="The rate at which wolf agents reproduce.",
    # ),
    # "wolf_gain_from_food": mesa.visualization.Slider(
    #     "Wolf Gain From Food Rate", 20, 1, 50
    # ),
    # "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    TraficoAereo, [canvas_element, chart_element], "Simulación del Tráfico Aéreo", model_params
)
server.port = 8521
