from mesa import Agent


class FloorTile(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)


class Roomba(Agent):

    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.direction = 4
        self.moves = 0

    def move(self):
        possibleStep = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True)

        freeSpaces = list(map(self.model.grid.is_cell_empty, possibleStep))

        directions = len(freeSpaces)

        if self.direction in range(0, directions):
            self.model.grid.move_agent(self, possibleStep[self.direction])
            # print(
            #     f"Se mueve de {self.pos} a {possibleStep[self.direction]}; direction {self.direction}")
            self.moves += 1

    def step(self):
        self.direction = self.random.randint(0, 8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()
