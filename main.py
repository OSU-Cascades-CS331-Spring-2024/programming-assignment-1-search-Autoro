import argparse
from map import Map
from astar import Astar
from bfs import BreadthFirstSearch
from ids import IterativeDeepeningSearch
from ucs import UniformCostSearch
from search_result import SearchResult
from typing import List

search_methods = {
    BreadthFirstSearch.name: BreadthFirstSearch,
    IterativeDeepeningSearch.name: IterativeDeepeningSearch,
    UniformCostSearch.name: UniformCostSearch,
    Astar.name: Astar
}

default_queries = [
    ("brest", "nice"),
    ("montpellier", "calais"),
    ("strasbourg", "bordeaux"),
    ("paris", "grenoble"),
    ("brest", "grenoble"),
    ("grenoble", "brest"),
    ("nice", "nantes"),
    ("caen", "strasbourg")
]

def search_factory(search_method : str, map : Map):
    """
    Creates an instance of a search class based on the given name.

    Args:
        search_method (str): The name of the search method to create.
        map (Map): The map the search method will be initialized with.
    
    Returns:
        Search: One of the specialized search objects.
    """

    return search_methods[search_method](map)

def perform_search(search_method : str, start : str, target : str, map : Map) -> SearchResult:
    """
    Perform a given search for a given start city and target city.

    Args:
        search_method (str): The name of the search method to use.
        start (str): The name of the city to start the search at.
        target (str): The name of the target city to search for.
        map (Map): The map containing all cities to search through.
    
    Returns:
        SearchResult: The result of the search that was performed.
    """

    search = search_factory(search_method, map)
    
    return search.perform(start, target)

def perform_all_searches(map : Map) -> List[SearchResult]:
    """
    Performs all possible search methods for each of the default search queries.

    Args:
        map (Map): The name containing all the cities to search through.

    Returns:
        List[SearchResult]: The results of every search that was performed.
    """

    results = []

    for method in search_methods:
        for start, target in default_queries:
            result = perform_search(method, start, target, map)

            results.append(result)
        
    return results

def main(args):
    map = Map.from_file(args.map_file)

    if args.start and args.target:
        result = perform_search(args.search, args.start, args.target, map)

        print(result)
    else:
        results = perform_all_searches(map)

        for result in results:
            print(result)
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map_file", help="The name of the file containing the map to run searches on.")
    parser.add_argument("-S", "--search", default="bfs", choices=["bfs",  "dls", "ucs", "astar"], help="The search method to perform on the map.")
    parser.add_argument("-A", "--start", help="The start of the search.")
    parser.add_argument("-B", "--target", help="The target of the search.")

    args = parser.parse_args()

    if args.start and not args.target or args.target and not args.start:
        parser.error("Start and target must be specified together.")

    main(args)
