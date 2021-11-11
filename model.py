from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
import time

from agents import FloorTile, Roomba


class Room(Model):
    def __init__(self, noOfAgents=3, dirtyTiles=20, width=50, height=50, limit=60):
        self.agents = noOfAgents
        self.dirty = dirtyTiles
        self.grid = Grid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.totalRoombaSteps = 0
        self.time = time.time()
        self.limit = limit

        for i in range(self.agents):
            roomba = Roomba(i, self)
            self.schedule.add(roomba)
            pos = (1, 1)
            self.grid.place_agent(roomba, pos)

        for i in range(self.dirty):
            def pos_gen(w, h): return (
                self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            tile = FloorTile(pos, self)
            self.schedule.add(tile)
            self.grid.place_agent(tile, pos)

        self.datacollector = DataCollector(
            {
                "DirtyTiles": self.count(),
                "Total Steps": lambda m: self.count_type(m, "totalRoombaSteps"),
                "Time": round(time.time() - self.time, 2)
            }
        )

    def countCleanTiles(self) -> int:
        # count = self.schedule.get_agent_count()
        # return self.schedule.get_agent_count()
        count = 0
        for tile in self.schedule.agents:
            if isinstance(tile, FloorTile):
                count += 1
        print(count)
        return count

    def count(self) -> int:
        count = 0
        for i, x, y in self.grid.coord_iter():
            if type(i).__name__ == "FloorTile":
                count += 1
        print(count)
        return count

    def step(self):
        self.totalRoombaSteps += self.agents
        self.schedule.step()
        if (time.time() - self.time >= self.limit) or (self.count() == 0):
            self.running = False
