#Traveling salesman: Greedy solutions in python.

This is two simple python solutions to the NP-complete problem, The Travelling Salesman.

simpleGreedy.py is a solution that starts from city 0 and visits the nearest unvisited city until all cities have been visited.

Example usage:      
`python simpleGreedy.py tsp_example_1.txt`  

 randomStartingPlaces.py does the same thing, but instead of starting from city 0 is runs 40 randomly chosen starting cities and keeps the shortest path.    
               
 Example usage:      
 `python randomStartingPlaces.py tsp_example_1.txt`

Both programs take an input file that looks like tsp_example_1.txt (a list of cities given as [id#, x-coordinate, y-coordinate]), and produce an output file that looks like tsp_example_1.txt.tour (the top number is the total distance of the best path found, followed by the cities listed in the order they are visited on that path).

tsp-verifier.py and TSPAllVisited.py were used during development to ensure that the path produces an accurate distance. Example usage:  
`python tsp-verifier.py tsp_example_1.txt tsp_example_1.txt.tour`
