from city import City
from enum import Enum
from search import Search
from search_result import SearchResult
from typing import List

class DlsResult(Enum):
    """
    A enum representing the results of a depth-limited search.
    """
    SUCCESS = 0
    FAILURE = 1
    CUTOFF = 2

class IterativeDeepeningSearch(Search):
    """
    Represents an iterative deepening depth-limited search.
    """

    name = "dls"

    def __dls__(self, current : City, target : str, limit : int, visited : List[City], search_result : SearchResult):
        """
        Recursively performs a depth-limited search from the given city for the given target.

        Args:
            current (City): The current city to perform the search from.
            target (str): The name of the target city to be found.
            limit (int): The current depth limit. The method will return if the limit is 0.
            visited (List[City]): The list of cities visited so far so that cycles can be avoided.
            search_result (SearchResult): The accumulative results of the search through all recursions.
        
        Returns:
            (DlsResult): An enum value indiciating the result of the depth-limited search.
        """

        if limit == 0:
            # If we hit our limit, consider this action maintained and return.
            search_result.maintained += 1
            
            return DlsResult.CUTOFF
        
        # A call into this method is synonymous with a city being popped from a frontier.
        search_result.expanded += 1

        if current.name == target:
            # If we found our target, start building the path and return.
            search_result.success = True
            search_result.path = [ current ]

            return DlsResult.SUCCESS
        


        cutoff_occured = False
        for i, action in enumerate([a for a in current.actions if a.destination not in [v.name for v in visited]]):
            neighbor = self.map.get_city(action.destination)

            visited.append(neighbor)
            search_result.explored += 1
            
            result = self.__dls__(neighbor, target, limit - 1, visited, search_result)
            if result == DlsResult.SUCCESS:
                # If our last action found the target, add the current city to the beginning
                # of the path as well as the cost of the last action. Consider all other remaining
                # actions from the current city as maintained and return.
                search_result.path.insert(0, current)
                search_result.cost += action.cost
                search_result.maintained += len(current.actions) - i
                
                return result
            elif result == DlsResult.CUTOFF:
                # A cutoff occured deeper down in the recursion, so keep track of that.
                cutoff_occured = True
        
        # If a cutoff occured, indicate so. Otherwise this path and been fully explored without finding the target.
        return DlsResult.CUTOFF if cutoff_occured else DlsResult.FAILURE

    def perform(self, start : str, target : str) -> SearchResult:
        """
        Performs an iterative deepening depth-limited search from the given start city until the given target city is found.
        
        Args:
            start (str): The name of the city to start at.
            target (str): The name of the target city to be found.

        Returns:
            SearchResult: The result of the search.
        """
        
        start_city = self.map.get_city(start)

        search_result = SearchResult(IterativeDeepeningSearch.name, start, target)

        max_depth = 0
        while self.__dls__(start_city, target, max_depth, [], search_result) == DlsResult.CUTOFF:
            # Increase depth until either a success or failure occurs.
            max_depth += 1
        
        return search_result
