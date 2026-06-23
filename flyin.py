import sys
from src.graph import Graph
from src.parser import ParseError, MapParser
from src.simulation import Simulation
from src.visualizer import Visualizer


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: you must include 'flyin.py' <map.txt>")
        sys.exit(1)

    graph = Graph()
    parser = MapParser()

    try:
        parser.parse_file(sys.argv[1], graph)
        visualizer = Visualizer(graph)
        simulation = Simulation(graph, visualizer)
        turns = simulation.run()
        print(turns)
        visualizer.show()

    except ParseError:
        print("Error: Map file argument is required.")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nError: Simulation aborted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
