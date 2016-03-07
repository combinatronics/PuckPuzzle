'''
Determine the solvable instances of the Genius Hockey Puck puzzle.
States are modeled by signed permutations of (even) n that begin with +1.
So we are determining the connected componenent of the underlying graph that contains +1+2...+n.
'''

from SignedPermutations import SignedPermutations
from GeniusPuckUtilities import flip, neighbors, node_string, total_nodes
import numpy as np
import sys

def main(argv):
	# Read in the value of n and make sure it is even.
	if len(argv) < 2: usage()
	n = int(argv[1])
	if n % 2 != 0 or n < 2: usage()

	# The start node is +1+2....+n.
	start = list(range(1,n+1))

	#
	num_reached = BFS(start)
	print(num_reached)
	print(total_nodes(n))
	print(total_nodes(n) / float(num_reached))

#
def BFS(start):
	n = len(start)
	S = SignedPermutations()
	t = S.total(n) # note: our first symbol is +1 so this is wasteful
	reached = np.zeros([t], np.bool)  # could use np.int8 for distances
	reached[S.rank(start)] = True
	num_reached = 1
	Q = [start]
	while len(Q) > 0:
		node = Q.pop(0)
		for neighbor in neighbors(node):
			if reached[S.rank(neighbor)] == False:
				reached[S.rank(neighbor)] = True
				Q.append(neighbor)
				num_reached += 1
	return num_reached



def usage():
	print("usage: 'PuckConnected n' where n is a positive even integer.")
	exit(0)


if __name__ == "__main__":
	main(sys.argv)
