from src.graph import Zone, Connection


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
