import argparse
from map import Map
from bfs import BreadthFirstSearch
from ids import IterativeDeepeningSearch

def main(args):
    map = Map.from_file(args.map_file)

    search = IterativeDeepeningSearch(map)
    result = search.search("brest", "nice")

    print(result.path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map_file", help="The name of the file containing the map to run searches on.")
    parser.add_argument("-S", "--search", default="bfs", choices=["bfs",  "dls", "ucs", "astar"], help="The search method to perform on the map.")
    parser.add_argument("-A", "--origin", help="The origin of the search.")
    parser.add_argument("-B", "--destination", help="The destination of the search.")

    args = parser.parse_args()

    if args.origin and not args.destination or args.destination and not args.origin:
        parser.error("Origin and destination must be specified together.")

    main(args)
