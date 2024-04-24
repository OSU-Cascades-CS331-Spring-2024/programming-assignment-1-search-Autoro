import argparse
from map import Map
from astar import AstarSearch
from bfs import BreadthFirstSearch
from ids import IterativeDeepeningSearch
from ucs import UniformCostSearch
from search_result import SearchResult

search_methods = {
    BreadthFirstSearch.name: BreadthFirstSearch,
    IterativeDeepeningSearch.name: IterativeDeepeningSearch,
    UniformCostSearch.name: UniformCostSearch,
    AstarSearch.name: AstarSearch
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

def perform_all_searches(map : Map) -> list[SearchResult]:
    """
    Performs all possible search methods for each of the default search queries.

    Args:
        map (Map): The name containing all the cities to search through.

    Returns:
        list[SearchResult]: The results of every search that was performed.
    """

    results = []

    for method in search_methods:
        for start, target in default_queries:
            result = perform_search(method, start, target, map)

            results.append(result)
        
    return results

def compute_averages(results : list[SearchResult]) -> tuple[int, int, int]:
    """
    Computes the average explored, expanded, and maintained values of a given search result.

    Args:
        results (list[SearchResult]): The search result to compute averages for.
    
    Returns:
        tuple[int, int, int]: A tuple of the average explored, expanded, and maintained values in that order.
    """

    explored = 0
    expanded = 0
    maintained = 0
    count = len(results)

    for result in results:
        explored += result.explored
        expanded += result.expanded
        maintained += result.maintained
    
    explored /= count
    expanded /= count
    maintained /= count

    return (explored, expanded, maintained)

def compute_optimals(results : list[SearchResult]) -> dict[str, int]:
    """
    Computes the number of times each search method found the best result. If multiple
    search methods find the best result, then they both get counted.

    Args:
        results (list[SearchResult]): The list of search results to find optimal results in.
    
    Returns:
        dict[str, int]: A dictionary of the results for each method keyed of their name.
    """

    bfs_optimal = 0
    dls_optimal = 0
    ucs_optimal = 0
    astar_optimal = 0

    for start, target in default_queries:
        # Get all search results for the current query.
        query_results = [ r for r in results if r.start == start and r.target == target ]
        # Find the minimum cost found in all the searches.
        min_cost = min([ r.cost for r in query_results ])
        # Get all results that had that cost in case there are ties.
        optimal_results = [ r for r in query_results if r.cost == min_cost ]

        for optimal_result in optimal_results:
            if optimal_result.method == BreadthFirstSearch.name:
                bfs_optimal += 1
            elif optimal_result.method == IterativeDeepeningSearch.name:
                dls_optimal += 1
            elif optimal_result.method == UniformCostSearch.name:
                ucs_optimal += 1
            else:
                astar_optimal += 1
    
    return {
        BreadthFirstSearch.name: bfs_optimal,
        IterativeDeepeningSearch.name: dls_optimal,
        UniformCostSearch.name: ucs_optimal,
        AstarSearch.name: astar_optimal
    }

def print_stats(results : list[SearchResult]) -> None:
    """
    For each search method, prints the averages of the results, as well as the number
    of times that method found the optimal result. If multiple methods found the optimal result,
    then they both get counted as having found the optimal result.

    Args:
        results (list[SearchResult]): The list of results to print stats for.
    """

    filtered_results = {
        BreadthFirstSearch.name: [r for r in results if r.method == BreadthFirstSearch.name],
        IterativeDeepeningSearch.name: [r for r in results if r.method == IterativeDeepeningSearch.name],
        UniformCostSearch.name: [r for r in results if r.method == UniformCostSearch.name],
        AstarSearch.name: [r for r in results if r.method == AstarSearch.name]
    }

    optimal_results = compute_optimals(results)

    for method in filtered_results:
        method_results = filtered_results[method]
        optimal_count = optimal_results[method]
        average_explored, average_expanded, average_maintained = compute_averages(method_results)

        print(f"Method: {method}")
        print(f"Average Explored: {average_explored:.1f}")
        print(f"Average Expanded: {average_expanded:.1f}")
        print(f"Average Maintained: {average_maintained:.1f}")
        print(f"Optimal Solutions: {optimal_count}")
        print()

def main(args):
    map = Map.from_file(args.map_file)

    if args.start and args.target:
        result = perform_search(args.search, args.start, args.target, map)
        print(result)
    else:
        results = perform_all_searches(map)
        print_stats(results)

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
