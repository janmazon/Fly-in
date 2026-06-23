from src.graph import Graph
from src.drone import Drone
from src.pathfinder import Pathfinder
from src.visualizer import Visualizer
import time


class Simulation:
    def __init__(self, graph: Graph, visualizer: Visualizer) -> None:
        self.graph = graph
        self.visualizer = visualizer
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
            self.turn += 1
            moves: list[str] = []
            drones_to_remove: list[Drone] = []

            for drone in self.drones:
                if not drone.path:
                    drone.path = self.pathfinder.get_path(drone.current_zone)

                if drone.move(self.graph):
                    if (drone.target_zone is not None and
                            drone.current_connection is not None):
                        moves.append(f"D{drone.drone_id}-"
                                     f"{drone.current_connection.zone_a.name}-"
                                     f"{drone.current_connection.zone_b.name}")
                    elif drone.current_zone is not None:
                        moves.append(f"D{drone.drone_id}-"
                                     f"{drone.current_zone.name}")

                if drone.current_zone is self.graph.end_hub:
                    drones_to_remove.append(drone)

            if moves:
                print(" ".join(moves))

            try:
                self.visualizer.draw_drones(self.drones)
                self.visualizer.window.update()
                time.sleep(1.0)
            except Exception:
                pass

            for d in drones_to_remove:
                if d.current_zone is not None:
                    d.current_zone.current_drones -= 1
                if d.current_connection is not None:
                    d.current_connection.current_traffic -= 1
                self.drones.remove(d)

        return self.turn
