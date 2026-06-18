from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 zone_type: ZoneType = ZoneType.NORMAL,
                 color: str | None = None, max_drones: int = 1) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.zone_type = zone_type
        self.max_drones = max_drones
        self.current_drones: int = 0


class Connection:
    def __init__(self, zone_a: Zone, zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        self.current_traffic: int = 0


class Graph:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.num_drones: int = 0
