import math
from search import Search
from search_result import SearchResult

class UniformCostSearch(Search):
    """
    Represents a uniform-cost search.
    """

    def search(self, start : str, target : str) -> SearchResult:
        """
        Performs a uniform-cost search from the given start city until the given target city is found.

        Args:
            start (str): The name of the city to start at.
            target (str): The name of the target city to be found.

        Returns:
            SearchResult: The result of the A* search.
        """

        start_city = self.map.get_city(start)

        frontier = [ start_city]
        parents = { start_city: None }
        costs = { start_city: 0 }

        result = SearchResult(explored=1)
        
        while frontier:
            current = self.__pop_next_lowest_cost__(frontier, costs)
            result.expanded += 1

            if current.name == target:
                result.success = True
                result.path = self.__build_path__(current, parents)
                result.cost = costs[current]
                result.maintained = len(frontier)
                
                break

            for action in current.actions:
                neighbor = self.map.get_city(action.destination)
                cost = costs[current] + action.cost

                if cost < costs.get(neighbor, math.inf):
                    parents[neighbor] = current
                    costs[neighbor] = cost

                    if neighbor not in frontier:
                        frontier.append(neighbor)
                        result.explored += 1
                
        return result
