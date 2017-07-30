# Description

This is a slightly higher version of [ultimate tictactoe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) where 4x4 grids are used. If the opponent plays (X or O) on a particular square, then you are supposed to play the block corresponding to that square. Each player has to play within 15 seconds.

# Instructions

1. cd `ultimate-tictactoe-bot`
2. python simulator.py [option]

There are five options:

1. Bot vs. Human
2. Human vs. Bot
3. Random player vs. Bot
4. Bot vs. Random player
5. Random player vs. Random player


# Algorithm

Iterative deepening minimax algorithm with alpha-beta pruning.

# Heuristics

1.	Basic winning and losing positions : inf and -inf ; number of grids won - number of grids.
2.	Usual tictactoe diagonal, coloumn and row winning conditions incorporated.
3.	Different weights for small blocks and the bigger block.

# Development

The code is pretty straight and easy to hack. There are several issues as of now and hence any sort of ideas/PRs would be really helpful!