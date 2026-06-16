from src.graph import Zone


class Drone:
    def __init__(self, drone_id: int, current_zone: Zone,
                 path: list[Zone] | None = None) -> None:
        self.drone_id = drone_id
        self.current_zone = current_zone

        if path is None:
            self.path: list[Zone] = []
        else:
            self.path = path
