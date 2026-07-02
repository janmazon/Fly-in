import tkinter as tk
from graph import Graph
from drone import Drone


class Visualizer:
    """Draws the map and the drones on a window, using Tkinter, so a
    person can watch the simulation happen.
    """

    def __init__(self, graph: Graph) -> None:
        """Builds the window, works out how to scale the map so it fits
        the screen, and draws the map for the first time.

        Args:
            graph: The graph (map) that will be drawn.
        """

        self.graph = graph
        self.window = tk.Tk()
        self.window.attributes("-zoomed", True)
        self.canvas = tk.Canvas(self.window, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.update()

        width: int = self.window.winfo_width()
        height: int = self.window.winfo_height()

        self.min_x = min([zone.x for zone in self.graph.zones.values()])
        self.min_y = min([zone.y for zone in self.graph.zones.values()])
        max_x = max([zone.x for zone in self.graph.zones.values()])
        max_y = max([zone.y for zone in self.graph.zones.values()])
        diff_x = max_x - self.min_x
        diff_y = max_y - self.min_y

        if diff_x == 0:
            diff_x = 1
        if diff_y == 0:
            diff_y = 1

        offset: int = 100

        scale_x = (width - (offset * 2)) / diff_x
        scale_y = (height - (offset * 2)) / diff_y
        self.scale = min(scale_x, scale_y)

        drawing_width = diff_x * self.scale
        drawing_height = diff_y * self.scale

        self.offset_x = (width - drawing_width) / 2
        self.offset_y = (height - drawing_height) / 2

        self.draw_graph()

    def get_coordinates(self, x: int, y: int) -> tuple[int, int]:
        """Converts a zone's (x, y) position from the map file into the
        actual pixel position on the screen.

        Args:
            x: The X position of the zone, as written in the map file.
            y: The Y position of the zone, as written in the map file.

        Returns:
            The pixel position on screen where this point should be drawn.
        """

        return (int((x - self.min_x) * self.scale + self.offset_x),
                int((y - self.min_y) * self.scale + self.offset_y))

    def draw_graph(self) -> None:
        """Clears the screen and draws every connection (as lines) and
        every zone (as colored circles with their name) on the canvas.
        """

        self.canvas.delete("all")

        for connection in self.graph.connections:
            x1, y1 = self.get_coordinates(connection.zone_a.x,
                                          connection.zone_a.y)
            x2, y2 = self.get_coordinates(connection.zone_b.x,
                                          connection.zone_b.y)
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

        radio: int = int(self.scale * 0.25)
        if radio < 5:
            radio = 5
        if radio > 30:
            radio = 30

        for zone in self.graph.zones.values():
            x, y = self.get_coordinates(zone.x, zone.y)

            if zone.color is not None:
                circle_color = zone.color
            else:
                circle_color = "lightgray"

            try:
                self.canvas.create_oval(x - radio, y - radio, x + radio,
                                        y + radio, fill=circle_color,
                                        outline="black")
            except tk.TclError:
                self.canvas.create_oval(x - radio, y - radio, x + radio,
                                        y + radio, fill="lightgray",
                                        outline="black")

            if len(self.graph.zones) < 45:
                self.canvas.create_text(x, y + radio + 15, text=zone.name)

    def draw_drones(self, drones: list[Drone]) -> None:
        """Removes the drones drawn in the previous turn and draws all the
        drones again at their new positions.

        If more than one drone is in the same zone, they are placed next to
        each other in a small row so they don't overlap.

        Args:
            drones: The list of drones to draw on the map.
        """

        self.canvas.delete("drone")
        drones_in_zone: dict[str, int] = {}

        for drone in drones:
            if drone.current_zone is not None:
                x, y = self.get_coordinates(drone.current_zone.x,
                                            drone.current_zone.y)
                if drone.current_zone.name not in drones_in_zone:
                    drones_in_zone[drone.current_zone.name] = 0
                pos_in_line = drones_in_zone[drone.current_zone.name]
                new_x = (x - 10) + (pos_in_line * 18)
                self.canvas.create_oval(new_x - 8, y - 8, new_x + 8, y + 8,
                                        fill="black", tags="drone")
                self.canvas.create_text(new_x, y, text=str(drone.drone_id),
                                        fill="white", font=("Arial", 8),
                                        tags="drone")
                drones_in_zone[drone.current_zone.name] += 1

    def show(self) -> None:
        """Starts the Tkinter event loop so the window stays open and
        responds to events (like closing it).
        """

        self.window.mainloop()
