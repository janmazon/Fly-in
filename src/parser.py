from src.graph import Graph, Zone, ZoneType


class ParseError(Exception):
    pass


class MapParser:
    def parse_file(self, file: str, graph: Graph) -> None:
        with open(file, "r") as f:
            counter_line: int = 0
            has_read_drones = False

            for line in f:
                counter_line += 1
                stripped = line.strip()

                if stripped.startswith("#") or not stripped:
                    continue
                if not has_read_drones:
                    if stripped.startswith("nb_drones"):
                        parts = stripped.split(":")
                        try:
                            graph.num_drones = int(parts[1].strip())
                        except ValueError:
                            raise ParseError(counter_line, line, "Error: the "
                                             "number of drones must be "
                                             "an integer.")
                        has_read_drones = True
                        continue
                    else:
                        raise ParseError(counter_line, line, "Error: nb_drones"
                                         " must be defined on the first line.")
                if (stripped.startswith("hub:") or
                        stripped.startswith("start_hub:") or
                        stripped.startswith("end_hub:")):
                    parts = stripped.split()
                    try:
                        zone_name = parts[1]
                        coord_x = int(parts[2])
                        coord_y = int(parts[3])
                    except (ValueError, IndexError):
                        raise ParseError(counter_line, line, "Error: invalid "
                                         "zone format or missing coordinates.")
                    if zone_name in graph.zones:
                        raise ParseError(counter_line, line, f"Error: zone"
                                         f" '{zone_name}' is duplicated.")

                    z_type = ZoneType.NORMAL
                    z_color = None
                    z_max_drones = 1

                    if "[" in stripped and "]" in stripped:
                        pos_start = stripped.find("[") + 1
                        pos_fin = stripped.find("]")
                        inside_brackets = stripped[pos_start:pos_fin]
                        metadata_parts = inside_brackets.split()
                        for part in metadata_parts:
                            try:
                                key_value = part.split("=")
                                key = key_value[0]
                                value = key_value[1]

                                if not value:
                                    raise IndexError

                                if key == "zone":
                                    if value == "priority":
                                        z_type = ZoneType.PRIORITY
                                    elif value == "restricted":
                                        z_type = ZoneType.RESTRICTED
                                    elif value == "blocked":
                                        z_type = ZoneType.BLOCKED
                            except IndexError:
                                raise ParseError(counter_line, line, "Error: "
                                                 "metadata must be "
                                                 "in key=value format.")

                    new_zone = Zone(name=zone_name, x=coord_x, y=coord_y,
                                    zone_type=z_type, color=z_color,
                                    max_drones=z_max_drones)

                    graph.zones[zone_name] = new_zone
                    if stripped.startswith("start_hub:"):
                        graph.start_hub = new_zone
                    elif stripped.startswith("end_hub:"):
                        graph.end_hub = new_zone
