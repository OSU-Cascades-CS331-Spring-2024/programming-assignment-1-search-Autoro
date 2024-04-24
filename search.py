from city import City
from map import Map
from typing import Dict, List

class Search:
    """
    Represents a search that can be performed on a map of cities.
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
    
    def __pop_next_lowest_cost__(self, frontier : List[City], costs : Dict[City, int]) -> City:
        """
        Pops the next lowest path cost city from the frontier.

        Args:
            frontier (List[City]): The current frontier to pop a city from.
            costs (Dict[City, int]): A dictionary containing the total path cost to a given city.

        Returns:
            City: The next lowest path cost cost city.
        """

        min_index = 0

        for i in range(1, len(frontier)):
            city = frontier[i]
            
            if costs[city] < costs[frontier[min_index]]:
                min_index = i

        return frontier.pop(min_index)
