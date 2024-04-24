import re
from action import Action
from city import City
from coordinate import Coordinate
from pathlib import Path
from typing import Self

class Map:
    """
    Represents a map of cities.
    """

    def __init__(self, cities : list[City]) -> None:
        self.cities = cities
    
    @staticmethod
    def __parse_actions__(action_line : str) -> list[Action]:
        """
        Parses the actions portion of a map file line into a collection of actions.

        Args:
            action_line (str): The string containing the actions that can be taken from a city.

        Returns:
            list[Action]: The collection of initialized action objects.
        """

        parts = action_line.split()
        
        # Pair up every destination with its cost, then create an Action object from
        # those pairs and add it to the list.
        actions = []
        for action in zip(parts[::2], parts[1::2]):
            destination = re.sub("va-", "", action[0])
            cost = int(action[1])

            actions.append(Action(destination, cost))

        return actions

    @staticmethod
    def __parse_city__(city_line : str) -> City:
        """
        Parses the city portion of a map file line into a city object.

        Args:
            city_line (str): The string containing the city name, latitude, and longitude.

        Returns:
            City: An initialized city object containing its information.
        """

        # Create variables from the different parts of the string using list unpacking.
        city_name, lat_degrees, lat_minutes, lat_seconds, lat_heading, long_degrees, long_minutes, long_seconds, long_heading = city_line.split()

        latitude = Coordinate.from_dms(lat_degrees, lat_minutes, lat_seconds, lat_heading)
        longitude = Coordinate.from_dms(long_degrees, long_minutes, long_seconds, long_heading)

        return City(city_name, latitude, longitude)

    @staticmethod
    def __parse_map_line__(line : str) -> City:
        """
        Parses a specific map file line into a city and its actions.

        Args:
            line (str): A single line from the map file.

        Returns:
            City: A complete city object with its associated actions.
        """

        city_part, action_part = line.strip().split(" --> ")

        city = Map.__parse_city__(city_part)
        actions = Map.__parse_actions__(action_part)

        city.add_actions(actions)
        
        return city

    @classmethod
    def from_file(cls, file_name : str) -> Self:
        """
        Loads the given map file and parses it into an array of cities.
        
        Args:
            map_file (str): The name of the file to load the map from.

        Returns:
            list: A list of cities that represents the map.
        """

        cities = []

        map_file_path = Path(file_name)
        if not map_file_path.is_file:
            raise(f"Error: The map file '{file_name}' does not exist.")

        with open(map_file_path, "r") as file:
            for line in file.readlines():
                city = Map.__parse_map_line__(line)
                cities.append(city)

        return cls(cities)
    
    def get_city(self, name : str) -> City:
        """
        Finds the given city in the map.

        Args:
            name (str): The name of the city to search for.
            
        Returns:
            City: The city if it is found, otherwise None.
        """
        for city in self.cities:
            if city.name == name:
                return city
        
        return None
