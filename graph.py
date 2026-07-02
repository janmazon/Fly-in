from enum import Enum


class ZoneType(Enum):
    """A list of the different zones that can exist on the map.

    Members:
        NORMAL: A normal zone. Nothing special happens here.
        BLOCKED: A zone that no drone is allowed to enter.
        RESTRICTED: A zone that costs more to fly through.
        PRIORITY: A zone that costs less to fly through, so the pathfinder
            likes to use it.
    """

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    """A single point on the map where drones can be.

    A zone has a name, a position (x, y), a type, a color to draw it with,
    and a maximum number of drones it can hold at the same time.
    """

    def __init__(self, name: str, x: int, y: int,
                 zone_type: ZoneType = ZoneType.NORMAL,
                 color: str | None = None, max_drones: int = 1) -> None:
        """Builds a new Zone.

        Args:
            name: The unique name of the zone.
            x: The X position of the zone on the map grid.
            y: The Y position of the zone on the map grid.
            zone_type: What kind of zone this is. Defaults to NORMAL.
            color: The color used to draw this zone on screen. If None, it will
                be drawn light gray.
            max_drones: How many drones can be in this zone. Defaults to 1.
        """

        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.zone_type = zone_type
        self.max_drones = max_drones
        self.current_drones: int = 0


class Connection:
    """A link between two zones that drones can travel through.

    A connection works in both directions and has a limit on how many drones
    can be traveling through it at the same time.
    """

    def __init__(self, zone_a: Zone, zone_b: Zone,
                 max_link_capacity: int = 1) -> None:
        """Builds a new Connection between two zones.

        Args:
            zone_a: One end of the connection.
            zone_b: The other end of the connection.
            max_link_capacity: How many drones can travel on this connection
                at the same time. Defaults to 1.
        """

        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        self.current_traffic: int = 0


class Graph:
    """The whole map: every zone and every connection between them.
    """

    def __init__(self) -> None:
        """Builds an empty Graph, ready to be filled by the parser.
        """

        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.num_drones: int = 0
