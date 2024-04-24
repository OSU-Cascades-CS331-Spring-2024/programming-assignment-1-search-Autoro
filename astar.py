import math
from city import City
from search import Search
from search_result import SearchResult

class Astar(Search):
    """
    Represents an A* search.
    """

    name = "astar"

    # Source: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def __calculate_distance__(self, current : City, target : City, in_miles : bool = False) -> float:
        """
        Calculates the haversine distance between two cities.

        Args:
            current (City): The current city to calculate distance from.
            target (City): The target city to calculate distance to.
            in_mies (bool): Wether or not to calculate the distance in miles. False calculates the distance in kilometers.

        Returns:
            float: The distance in kilometers or miles between two cities.
        """

        lat1 = math.radians(current.latitude.value)
        long1 = math.radians(current.longitude.value)
        lat2 = math.radians(target.latitude.value)
        long2 = math.radians(target.longitude.value)

        deltaLat = lat1 - lat2
        deltaLong = long1 - long2

        # Radius of earth in miles and kilometers.
        r = 3959 if in_miles else 6371
        a = math.sin(deltaLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(deltaLong / 2)**2
        c = 2 * math.asin(math.sqrt(a))

        return r * c
            
    def perform(self, start : str, target : str) -> SearchResult:
        """
        Performs an A* search from the given start city until the given target city is found.

        Args:
            start (str): The name of the city to start at.
            target (str): The name of the target city to be found.

        Returns:
            SearchResult: The result of the A* search.
        """

        start_city = self.map.get_city(start)
        target_city = self.map.get_city(target)

        frontier = [ start_city ]
        parents = { start_city: None }
        costs = { start_city: 0 }
        estimated_costs = { start_city: self.__calculate_distance__(start_city, target_city) }

        result = SearchResult("dls", start, target, explored=1)

        while frontier:
            current = self.__pop_next_lowest_cost__(frontier, estimated_costs)
            result.expanded += 1

            if current == target_city:
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
                    estimated_costs[neighbor] = cost + self.__calculate_distance__(neighbor, target_city)

                    if neighbor not in frontier:
                        frontier.append(neighbor)
                        result.explored += 1
                        
        return result
