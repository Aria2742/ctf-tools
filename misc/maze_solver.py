"""
	Program to solve mazes using a depth-first brute force algorithm
	Many reversing problems have included mazes as a way to obfuscate
		the input needed to get the flag
	Modify the global variables as needed for each maze then run to solve
"""

# used to prevent arrays from getting messed up from pass-by-reference
from copy import deepcopy

# constants to indicate what each value in the maze corresponds to
wall = 0
path = 1
start = 2
end = 3

# the maze in the form of an array
# keep this as a 1-dimensional array regardless of the maze's actual dimensions
maze = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,0,1,1,1,1,1,0,0,1,0,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1,1,0,1,1,1,1,1,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,1,1,1,1,1,0,1,0,1,0,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,1,0,1,1,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# list of moves and how they modify your position in the maze
# each element is a tuple of two values
#     1) a character/string to represent what move was made
#     2) an offset from the current position/index that is applied when the move is made
# for example, ('l', -1) may be used to signify a move left, which decrements your position/index in the maze by 1
moves = [('b',-121), ('d',11), ('f',121), ('l',-1), ('r',1), ('u',-11)]
# list of forbidden combinations of moves
# use this to prevent moves such as 'forward backwards' or 'left right'
forbidden = ['fb', 'bf', 'lr', 'rl', 'du', 'ud']
# the maximum number of moves to make when solving the maze
max_moves = 30

# the start and end indices for the maze
# the solver will start the maze from start_idx and work to find a path to end_idx
# if the maze contains a start and end marker, these can be set using maze.index()
start_idx = maze.index(start)
end_idx = maze.index(end)

"""
	Code below should NOT need to be modified
	Simply run this program after making necessary changes to the global variables above
"""

# use recursion to easily implement a depth-first search
# solutions are printed as they are found
# idx is the current position in the maze
# soln is the string representation of all moves made so far
# move_cnt is the number of moves made
# returns nothing
def do_step(idx, soln, move_cnt):
	# kill solutions that are too long
	if move_cnt > max_moves:
		return
	# kill solutions that make forbidden moves
	for f in forbidden:
		if f in soln:
			return
	# check for valid moves forward
	for m in moves:
		repr = m[0]
		delta = m[1]
		# use try-except as quick and dirty way to make sure index is in bounds
		try:
			# if we reached the end, print the solution
			# however, don't return from recursion since maze might have multiple solutions
			if idx+delta == end_idx:
				print(f'Solution: {soln+repr}')
			# if valid path ahead, make the move
			if maze[idx+delta] == path:
				do_step(idx+delta, deepcopy(soln)+repr, move_cnt+1)
		except IndexError:
			pass

do_step(start_idx, '', 0)
print('Finished')