from src.graph import Graph, Zone, ZoneType, Connection


class ParseError(Exception):
    """An error raised when the map file has a mistake in it
    (bad format, missing data, duplicated names, etc).
    """

    pass


class MapParser:
    """Reads a map file and fills a Graph with the zones and connections
    described inside it.
    """

    def parse_file(self, file: str, graph: Graph) -> None:
        """Reads the given map file line by line and builds the graph.

        It checks that the file starts with the number of drones, then reads
        zone lines (hub, start_hub, end_hub) and connection lines, and raises
        a ParseError if anything is written in the wrong format.

        Args:
            file: The path to the map file to read.
            graph: The Graph object that will be filled with the zones and
                connections found in the file.

        Raises:
            ParseError: If the file cannot be opened, or if any line in the
                file does not follow the expected format.
        """

        try:
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
                                if graph.num_drones <= 0:
                                    raise ValueError
                            except (ValueError, IndexError):
                                raise ParseError(counter_line, line, "Error: "
                                                 "the number of drones must "
                                                 "be a positive integer.")
                            has_read_drones = True
                            continue
                        else:
                            raise ParseError(counter_line, line, "Error: nb_"
                                             "drones must be defined on the "
                                             "first line.")

                    if (stripped.startswith("hub:") or
                            stripped.startswith("start_hub:") or
                            stripped.startswith("end_hub:")):
                        parts = stripped.split()
                        try:
                            zone_name = parts[1]
                            if "-" in zone_name:
                                raise ValueError
                            coord_x = int(parts[2])
                            coord_y = int(parts[3])
                        except (ValueError, IndexError):
                            raise ParseError(counter_line, line, "Error: "
                                             "invalid zone format or missing "
                                             "coordinates.")

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
                                        elif value == "normal":
                                            z_type = ZoneType.NORMAL
                                        else:
                                            raise ValueError

                                    if key == "color":
                                        z_color = value

                                    if key == "max_drones":
                                        z_max_drones = int(value)
                                        if z_max_drones <= 0:
                                            raise ValueError

                                except (IndexError, ValueError):
                                    raise ParseError(counter_line, line,
                                                     "Error: invalid metadata "
                                                     "format.")

                        new_zone = Zone(name=zone_name, x=coord_x, y=coord_y,
                                        zone_type=z_type, color=z_color,
                                        max_drones=z_max_drones)
                        graph.zones[zone_name] = new_zone

                        if stripped.startswith("start_hub:"):
                            if graph.start_hub is not None:
                                raise ParseError(counter_line, line, "Error: "
                                                 "multiple start hubs "
                                                 "defined.")
                            graph.start_hub = new_zone
                        elif stripped.startswith("end_hub:"):
                            if graph.end_hub is not None:
                                raise ParseError(counter_line, line, "Error: "
                                                 "multiple end hubs defined.")
                            graph.end_hub = new_zone

                    elif stripped.startswith("connection:"):
                        parts = stripped.split()
                        try:
                            zones_split = parts[1].split("-")
                            zone1 = zones_split[0]
                            zone2 = zones_split[1]
                        except IndexError:
                            raise ParseError(counter_line, line, "Error: "
                                             "invalid connection format.")

                        c_max = 1

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

                                    if key == "max_link_capacity":
                                        c_max = int(value)
                                        if c_max <= 0:
                                            raise ValueError

                                except (IndexError, ValueError):
                                    raise ParseError(counter_line, line,
                                                     "Error: invalid metadata "
                                                     "format.")

                        if (zone1 not in graph.zones or
                                zone2 not in graph.zones):
                            raise ParseError(counter_line, line, "Error: "
                                             "connection uses a non-existent "
                                             "zone.")

                        for conn in graph.connections:
                            conn_zones = {conn.zone_a.name, conn.zone_b.name}
                            if conn_zones == {zone1, zone2}:
                                raise ParseError(counter_line, line, "Error: "
                                                 "duplicate connection.")

                        zone_a1 = graph.zones[zone1]
                        zone_b2 = graph.zones[zone2]

                        new_connection = Connection(zone_a=zone_a1,
                                                    zone_b=zone_b2,
                                                    max_link_capacity=c_max)
                        graph.connections.append(new_connection)

                    else:
                        raise ParseError(counter_line, line, "Error: "
                                         "unrecognized line format.")

            if not graph.start_hub or not graph.end_hub:
                raise ParseError(counter_line, "EOF", "Error: map must "
                                 "contain both start_hub and end_hub.")

        except (OSError, UnicodeError):
            raise ParseError(0, file, f"Error: could not read map '{file}'.")
