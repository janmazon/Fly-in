from src.graph import Graph
from src.drone import Drone
from src.pathfinder import Pathfinder


class Simulation:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.turn: int = 0
        self.drones: list[Drone] = []
        self.pathfinder: Pathfinder = Pathfinder(self.graph)

        if self.graph.start_hub is not None:
            for i in range(1, self.graph.num_drones + 1):
                new_drone = Drone(drone_id=i,
                                  current_zone=self.graph.start_hub)
                self.drones.append(new_drone)

    def run(self) -> int:
        while self.drones:
            pass

        return self.turn
