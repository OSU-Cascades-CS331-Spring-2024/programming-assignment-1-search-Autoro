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
