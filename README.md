# Algorithm

Iterative deepening minimax algorithm with alpha-beta pruning.

# Heuristics

1.	Basic winning and losing positions : inf and -inf ; number of grids won - number of grids
2.	- Center four blocks/Corner blocks : 10000
	- Other blocks : 7000
3.	If >= 2 blocks are there in row, col or diagonals : *2 [likewise to opposite player, but negative]
4.	Memoization
5.	Limit opponent's choices [2000, -2000]

6. Number of X's and mult factor?