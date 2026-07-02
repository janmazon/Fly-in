import sys
from graph import Graph
from parser import ParseError, MapParser
from simulation import Simulation
from visualizer import Visualizer


def main() -> None:
    """The entry point of the program.

    Checks that a map file was given as an argument, parses it into a graph,
    then creates the visualizer and the simulation and runs it. If anything
    goes wrong (bad map, or the user stops the program), it prints an error
    message and exits.
    """

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

    except ParseError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nError: Simulation aborted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
