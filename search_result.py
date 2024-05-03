from city import City
from dataclasses import dataclass, field

@dataclass
class SearchResult:
    method : str
    start : str
    target : str
    success : bool = field(default=False)
    path : list[City] = field(default=None)
    cost : int = field(default=0)
    explored : int = field(default=0)
    expanded : int = field(default=0)
    maintained : int = field(default=0)

    def __str__(self) -> str:
        return f"{self.start} -> {self.target}\n" \
        + f"Method: {self.method}\n" \
        + f"Result: { 'Success' if self.success else 'Failure'}\n" \
        + f"Path: {', '.join([c.name for c in self.path])}\n" \
        + f"Cost: {self.cost}\n" \
        + f"Explored: {self.explored}\n" \
        + f"Expanded: {self.expanded}\n" \
        + f"Maintained: {self.maintained}"
