from src.graph import Graph, Zone, ZoneType


class Pathfinder:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def get_path(self, current_zone: Zone | None) -> list[Zone]:
        if current_zone is None:
            return []

        if self.graph.end_hub is None:
            return []

        open_list: list[Zone] = [current_zone]
        came_from: dict[Zone, Zone] = {}
        real_cost: dict[Zone, float] = {current_zone: 0.0}
        total_cost: dict[Zone, float] = {current_zone: 0.0}

        while open_list:
            current = min(open_list, key=lambda z:
                          total_cost.get(z, float('inf')))

            if current is self.graph.end_hub:
                final_path: list[Zone] = [current]
                while current in came_from:
                    current = came_from[current]
                    final_path.append(current)
                return final_path[::-1][1:]

            open_list.remove(current)

            for connection in self.graph.connections:
                if connection.zone_a is current:
                    neighbor = connection.zone_b
                elif connection.zone_b is current:
                    neighbor = connection.zone_a
                else:
                    continue

                if neighbor.zone_type is ZoneType.BLOCKED:
                    continue

                if neighbor.zone_type is ZoneType.RESTRICTED:
                    base_cost = 2.0
                else:
                    base_cost = 1.0

                cost_to_neighbor = (real_cost[current] + base_cost +
                                    connection.current_traffic)

                if (neighbor not in real_cost or
                        cost_to_neighbor < real_cost[neighbor]):
                    came_from[neighbor] = current
                    real_cost[neighbor] = cost_to_neighbor

                    heuristic = (abs(neighbor.x - self.graph.end_hub.x) +
                                 abs(neighbor.y - self.graph.end_hub.y))
                    total_cost[neighbor] = cost_to_neighbor + heuristic

                    if neighbor not in open_list:
                        open_list.append(neighbor)

        return []
