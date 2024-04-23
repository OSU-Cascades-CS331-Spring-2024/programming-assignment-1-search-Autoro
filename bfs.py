from city import City
from map import Map
from search_result import SearchResult
from typing import Dict, List

class BreadthFirstSearch:
    """
    Represent a breadth-first search.
    """
    
    def __init__(self, map : Map) -> None:
        self.map = map

    def __build_path__(self, current : City, parents : Dict[City, City]) -> List[City]:
        """
        Builds a path from the start of the search to the specified current city.

        Args:
            current (City): The current city to build a path to.
            parents (dict[City, City]): The dictionary containing the parents for every city in the search.

        Returns:
            list: The list of cities in the path from the start to the end of the search.
        """

        path = [ current ]

        # Follow the chain of parents until no other parent is found.
        while current in parents and (current := parents[current]):
            # Insert to the front of the list so the last one inserted is the start of the path.
            path.insert(0, current)

        return path
    
    def search(self, start : str, end : str) -> SearchResult:
        """
        Performs a BFS search from the given start city name to the given end city name.

        Args:
            start (str): The name of the city to start at.
            end (str): The name of the city to end at.

        Returns:
            SearchResult: The result of the BFS search.
        """

        start_city = self.map.get_city(start)
        
        visited = []
        frontier = [ start_city ]
        parents = { start_city: None }
        costs = { start_city: 0 }

        # explored=1 because the start_city starts in the frontier.
        result = SearchResult(explored=1)

        while frontier:
            current = frontier.pop(0)
            result.expanded += 1

            if current.name == end:
                result.success = True
                result.path = self.__build_path__(current, parents)
                result.cost = costs[current]
                result.maintained = len(frontier)

                break
            
            for action in current.actions:
                neighbor = self.map.get_city(action.destination)

                if neighbor not in frontier and neighbor not in visited:
                    parents[neighbor] = current
                    costs[neighbor] = costs[current] + action.cost

                    frontier.append(neighbor)
                    result.explored += 1
            
            visited.append(current)
        
        return result
