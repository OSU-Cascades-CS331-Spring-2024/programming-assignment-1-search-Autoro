from typing import Self

class Coordinate:
    """
    Represents either a latitude or longitude coordinate.
    """

    def __init__(self, value : float) -> None:
        self.value = value
        
    @classmethod
    def from_dms(cls, degrees : int, minutes : int, seconds : int, hemisphere : str) -> Self:
        """
        Create an instance of Coordinate from provided degrees, minutes, seconds, and a heading.

        Args:
            degrees (int): The degrees.
            minutes (int): The minutes.
            seconds (int): The seconds.
            hemisphere (str): The hemisphere.
        
        Returns:
            Coordinate: An initialized instance of Coordinate.
        """

        value = int(degrees)
        value += int(minutes) / 60
        value += int(seconds) / 3600

        if hemisphere.lower() == "w" or hemisphere.lower() == "s":
            value *= -1
            
        return cls(value)
    
    def __str__(self) -> str:
        return self.value.__str__
