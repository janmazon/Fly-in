from src.graph import Zone, Connection, Graph, ZoneType


class Drone:
    def __init__(self, drone_id: int, current_zone: Zone | None,
                 path: list[Zone] | None = None) -> None:
        self.drone_id = drone_id
        self.current_zone = current_zone
        self.current_connection: Connection | None = None
        self.target_zone: Zone | None = None
        self.transit_timer: int = 0

        if path is None:
            self.path: list[Zone] = []
        else:
            self.path = path

    def move(self, graph: Graph) -> bool:
        if (self.transit_timer == 0 and self.current_connection is not None and
                self.target_zone is None):
            self.current_connection.current_traffic -= 1
            self.current_connection = None

        if self.transit_timer > 0:
            self.transit_timer -= 1
            if self.transit_timer == 0:
                self.current_zone = self.target_zone
                self.target_zone = None
                if self.current_connection is not None:
                    self.current_connection.current_traffic -= 1
                    self.current_connection = None
            return True

        if not self.path:
            return False

        if self.current_zone is None:
            return False

        next_zone = self.path[0]
        target_connection = None

        for connection in graph.connections:
            if (self.current_zone is connection.zone_a and
                    next_zone is connection.zone_b):
                target_connection = connection
            elif (self.current_zone is connection.zone_b and
                    next_zone is connection.zone_a):
                target_connection = connection

        if not target_connection:
            return False

        if (target_connection.current_traffic >=
                target_connection.max_link_capacity):
            return False
        if (next_zone.current_drones >= next_zone.max_drones and
                next_zone is not graph.end_hub):
            return False

        self.path.pop(0)
        self.current_zone.current_drones -= 1
        target_connection.current_traffic += 1
        next_zone.current_drones += 1

        if next_zone.zone_type is ZoneType.RESTRICTED:
            self.target_zone = next_zone
            self.current_connection = target_connection
            self.transit_timer = 1
            self.current_zone = None
        else:
            self.current_zone = next_zone
            self.current_connection = target_connection

        return True
