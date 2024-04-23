from action import Action
from coordinate import Coordinate
from typing import List

class City:
    """
    Represents a city with a name, latitude and longitude, and actions that can be taken to move to other cities.
    """

    def __init__(self, name : str, latitude : Coordinate, longitude : Coordinate) -> None:
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.actions = []

    def add_action(self, action : Action):
        """
        Adds a single action to the list of actions that can be taken from the city.

        Args:
            action (Action): The action that can be taken.
        """
        self.actions.append(action)

    def add_actions(self, actions : List[Action]):
        """
        Adds multiple actions to the list of actions that can be taken from a city.

        Args:
            actions (List[Action]): The actions that can be taken.
        """
        self.actions.extend(actions)

    def __repr__(self) -> str:
        return f"City(name={self.name}, latitude={self.latitude}, longitude={self.longitude})"
    
    def __str__(self) -> str:
        return self.name
