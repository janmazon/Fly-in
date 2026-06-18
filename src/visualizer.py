import tkinter as tk
from src.graph import Graph


class Visualizer:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.window = tk.Tk()
        self.window.attributes("-zoomed", True)
        self.canvas = tk.Canvas(self.window, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.update()

        width: int = self.window.winfo_width()
        height: int = self.window.winfo_height()
        max_x: int = 0
        max_y: int = 0
        for zone in self.graph.zones.values():
            if zone.x > max_x:
                max_x = zone.x
            if zone.y > max_y:
                max_y = zone.y
        if max_x == 0:
            max_x = 1
        if max_y == 0:
            max_y = 1

        offset: int = 100

        scale_x = (width - (offset * 2)) / max_x
        scale_y = (height - (offset * 2)) / max_y
        self.scale = min(scale_x, scale_y)

        drawing_width = max_x * self.scale
        drawing_height = max_y * self.scale

        self.offset_x = (width - drawing_width) / 2
        self.offset_y = (height - drawing_height) / 2

        self.draw_graph()

    def get_coordinates(self, x: int, y: int) -> tuple[int, int]:
        return (int(x * self.scale + self.offset_x),
                int(y * self.scale + self.offset_y))

    def draw_graph(self) -> None:
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

    def show(self) -> None:
        self.window.mainloop()
