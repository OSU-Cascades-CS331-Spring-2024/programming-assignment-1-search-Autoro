from search import Search
from search_result import SearchResult

class BreadthFirstSearch(Search):
    """
    Represent a breadth-first search.
    """
    
    def search(self, start : str, target : str) -> SearchResult:
        """
        Performs a breadth-first search from the given start city until the given target city is found.

        Args:
            start (str): The name of the city to start at.
            target (str): The name of the target city to be found.

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

            if current.name == target:
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
