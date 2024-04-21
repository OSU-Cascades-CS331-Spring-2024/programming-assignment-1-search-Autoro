import argparse
import re
from pathlib import Path
from action import Action
from city import City
from coordinate import Coordinate
from typing import List

city_pattern = r"(?P<name>\w+)"
lat_pattern = r"(?P<lat_degrees>\d+) (?P<lat_minutes>\d+) (?P<lat_seconds>\d+) (?P<lat_heading>N|S)"
long_pattern = r"(?P<long_degrees>\d+) (?P<long_minutes>\d+) (?P<long_seconds>\d+) (?P<long_heading>E|W)"
action_pattern = r"(?P<actions>va-(?P<destination>\w+) (?P<cost>\d+))+"
pattern = re.compile(f"^{city_pattern} {lat_pattern} {long_pattern} -->")

def parse_actions(action_line : str) -> List[Action]:
    """
    Parses the actions portion of a map file line into a collection of actions.

    Args:
        action_line (str): The string containing the actions that can be taken from a city.

    Returns:
        List[Action]: The collection of initialized action objects.
    """

    parts = action_line.split()
    
    # Pair up every destination with its cost, then create an Action object from
    # those pairs and add it to the list.
    actions = []
    for action in zip(parts[::2], parts[1::2]):
        actions.append(Action(action[0], action[1]))

    return actions

def parse_city(city_line : str) -> City:
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

def parse_map_line(line : str) -> City:
    """
    Parses a specific map file line into a city and its actions.

    Args:
        line (str): A single line from the map file.

    Returns:
        City: A complete city object with its associated actions.
    """

    city_part, action_part = line.strip().split(" --> ")

    city = parse_city(city_part)
    actions = parse_actions(action_part)

    city.add_actions(actions)
    
    return city
        
def parse_map(map_file):
    """
    Loads the given map file and parses it into an array of cities.
    
    Args:
        map_file (str): The name of the file to load the map from.

    Returns:
        list: A list of cities that represents the map.
    """

    map = []

    map_file_path = Path(map_file)
    if not map_file_path.is_file:
        raise(f"Error: The map file '{map_file}' does not exist.")

    with open(map_file_path, "r") as file:
        for line in file.readlines():
            city = parse_map_line(line)
            map.append(city)

    return map

def main(args):
    map = parse_map(args.map_file)
    print(map)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map_file", help="The name of the file containing the map to run searches on.")
    parser.add_argument("-m", "--method", default="bfs", choices=["bfs",  "dls", "ucs", "astar"], help="The search method to perform on the map.")
    parser.add_argument("-A", help="The starting point of the search.")
    parser.add_argument("-B", help="The goal of the search.")

    args = parser.parse_args()

    if args.A and not args.B or args.B and not args.A:
        parser.error("Both a start and goal must be specified together.")

    main(args)
