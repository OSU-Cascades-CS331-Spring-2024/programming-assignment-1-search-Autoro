# CS 333 Programming Assignment 1 - Search
Perform searches for cities in a given map one of several search algorithms. The algorithms that can be chosen from are breadth-first search, iterative deepening depth-limited search, uniform-cost search, or A* search.

If no start or target city is provided, the program will perform a set of default searches using every search algorithm. The results of these searches will be saved to a file named `solutions.txt`, and stats about the overall performance of each algorithm will be printed to the console.

## Usage
`./python3 main.py <map_file> [-S <search_method>] [-A <start>] [-B <target>]`

* `<map_file>` (required) - The name of the file to parse the map from.
* `<search_method>` (optional, default="bfs") - The name of the search method to use. Only takes affect if a start and target are specified.  
    * Options: `bfs` `dls` `ucs` `astar`
* `<start>` (optional) - The name of the city to start a search at. Requires `<target>` to also be specified.
* `<target>` (optional) - The name of the target city to search for. Requires `<start>` to also be specified.

## Results
```
Method: bfs
Average Explored: 16.4
Average Expanded: 14.5
Average Maintained: 1.9
Optimal Solutions: 2
```

Breadth-first search performed about as expected. It it explored and expanded most cities in the map without maintaining many in the frontier when finished. It also managed to find a couple optimal solutions.

```
Method: dls
Average Explored: 111.2
Average Expanded: 82.5
Average Maintained: 59.2
Optimal Solutions: 0
```

Iterative deeepening depth-limited search was by far the worst performer. IDDLS's ability to find a solution was likely hindered by the high number of actions that could be taken at each city. This probably caused it to perform many iterations before it found the target. As a result, its average explored, expanded, and maintained stats were considerably higher than the other searches. It also never found an optimal solution.

```
Method: ucs
Average Explored: 16.6
Average Expanded: 15.5
Average Maintained: 1.1
Optimal Solutions: 8
```
Uniform-cost search's performance was close to that of breadth-first search. Likely due to the fact that the consideration for path cost causes it to explore the closest cities first before moving further. However, it did manage to find the most optimal solutions.

```
Method: astar
Average Explored: 15.0
Average Expanded: 9.8
Average Maintained: 5.2
Optimal Solutions: 7
```
A*'s stats are overall much better than the other searches. While it discovered most cities in the map, it had to expand considerably less to find a solution. This meant that it had more nodes left unexpanded in its frontier. Surprisingly, A* did not find the most optimal solutions. I expected there to be a tie between A* and UCS, but A* seems to have failed to find an optimal search in one case.

## Summary
A* not being the most optimal search algorithm for this assignment was surprising. However, after checking some of the coordinates for cities in the map, I suspect it's due to some, if not all, the coordinates being considerably off (e.g. the coordinates for Brest point to the middle of the ocean). Since A* is an informed search, it relies on those coordinates being accurate to perform optimally.
