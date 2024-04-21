class Action:
    """
    Represents an action that can be taken from a city to move to another city.
    """
    
    def __init__(self, destination : str, cost : int) -> None:
        self.destination = destination
        self.cost = cost
