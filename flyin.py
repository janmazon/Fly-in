import sys
from src.graph import Graph
from src.parser import ParseError, MapParser
from src.simulation import Simulation


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: you must include 'flyin.py' <map.txt>")
        sys.exit(1)

    graph = Graph()
    parser = MapParser()

    try:
        parser.parse_file(sys.argv[1], graph)
        simulation = Simulation(graph)
        turns = simulation.run()
        print(turns)

    except ParseError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
