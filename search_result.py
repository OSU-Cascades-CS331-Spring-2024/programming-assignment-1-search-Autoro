from city import City
from dataclasses import dataclass, field
from typing import List

@dataclass
class SearchResult:
    method : str
    start : str
    target : str
    success : bool = field(default=False)
    path : List[City] = field(default=None)
    cost : int = field(default=0)
    explored : int = field(default=0)
    expanded : int = field(default=0)
    maintained : int = field(default=0)
