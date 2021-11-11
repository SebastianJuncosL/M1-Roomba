from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.datacollection import DataCollector


from model import Room, FloorTile


def roomPortrayal(roomba):
    if roomba is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(roomba, FloorTile)):
        portrayal["Color"] = "Brown"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2

    return portrayal


grid = CanvasGrid(roomPortrayal, 10, 10, 500, 500)

chart = ChartModule([{"Label": "Total Steps", "Color": "Pink"}],
                    data_collector_name='datacollector')

cells = ChartModule([{"Label": "Dirty Tiles", "Color": "Blue"}],
                    data_collector_name='datacollector')


model_params = {
    "height": 10,
    "width": 10,
    "noOfAgents": UserSettableParameter("slider", "Roombas", 3, 1, 15, 1),
    "dirtyTiles": UserSettableParameter("slider", "Dirty tiles", 5, 1, 40, 1),
    "limit": UserSettableParameter("slider", "Time", 60, 10, 180, 1)
}

server = ModularServer(Room, [grid, chart, cells],
                       "Roomba Simulation", model_params)

server.port = 8521
server.launch()
