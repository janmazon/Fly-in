from graph import Graph
from drone import Drone
from pathfinder import Pathfinder
from visualizer import Visualizer
import time
import sys


class Simulation:
    """Runs the drone simulation, turn by turn, until every drone has arrived
    at the end hub.
    """

    def __init__(self, graph: Graph, visualizer: Visualizer) -> None:
        """Builds a new Simulation and creates all the drones at the start hub.

        Args:
            graph: The graph (map) the simulation will run on.
            visualizer: The window used to draw the simulation on screen.
        """

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
        """Runs the simulation turn by turn until every drone has arrived at
        the end hub.

        On each turn, every drone that has no path tries to find one, then
        tries to move. If a drone cannot move for too long, its path is thrown
        away and it can try to find a new one. All the moves made on a turn are
        printed, and the screen is redrawn and paused for a second so a person
        can watch it happen.

        Returns:
            int: The total number of turns the simulation took to finish.
        """

        while self.drones:
            self.turn += 1
            moves: list[str] = []
            drones_to_remove: list[Drone] = []

            for drone in self.drones:
                if drone.wait_time > 1:
                    drone.path = []
                    drone.wait_time = 0

                if not drone.path:
                    drone.path = self.pathfinder.get_path(drone.current_zone)

                if not drone.path:
                    print("Error: this map is impossible")
                    sys.exit(1)

                if drone.move(self.graph):
                    drone.wait_time = 0
                    if (drone.target_zone is not None and
                            drone.current_connection is not None):
                        moves.append(f"D{drone.drone_id}-"
                                     f"{drone.current_connection.zone_a.name}-"
                                     f"{drone.current_connection.zone_b.name}")
                    elif drone.current_zone is not None:
                        moves.append(f"D{drone.drone_id}-"
                                     f"{drone.current_zone.name}")
                else:
                    drone.wait_time += 1

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
