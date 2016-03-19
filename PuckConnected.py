'''
Determine the solvable instances of the Genius Hockey Puck puzzle.
States are modeled by signed permutations of (even) n that begin with +1.
So we are determining the connected componenent of the underlying graph that contains +1+2...+n.
'''

from SignedPermutations import SignedPermutations
from GeniusPuckUtilities import flip, neighbors, node_string, total_nodes
from math import log
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
	(num_reached, max_distance) = BFS_numpyQ(start, updates=True) #BFS(start, updates=True)
	print("max distance: " + str(max_distance))
	print("num reached:  " + str(num_reached))
	print("total nodes:  " + str(total_nodes(n)))
	print(total_nodes(n) / float(num_reached))



#
def BFS(start, updates=False):
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
				if num_reached % 10000 == 0:
					print("reached: " + str(num_reached))
					print("queue length: " + str(len(Q)))
	return (num_reached, -1) # we didn't keep track of the max distance


# The BFS routine is getting killed because the queue is growing too large.
# So this routine will statically allocate it and use integer ranks inside it.
# Also, we will keep track of the distances.
def BFS_numpyQ(start, updates=False):
	n = len(start)
	S = SignedPermutations()
	t = S.total(n) # note: our first symbol is +1 so this is wasteful

	reached = np.zeros([t], np.int8)  # could use np.int8 for distances
	reached[S.rank(start)] = 1 # the distance counts starting from 1
	num_reached = 1

	assert(log(t,2) < 63)
	Q = np.zeros([t], np.int64)
	Q[0] = S.rank(start) # leave Q[0] empty to make indexing easier
	Qindex = 0
	while Qindex < num_reached:
		node_rank = Q[Qindex]
		node_signed = S.unrank(node_rank, n)
		Qindex += 1
		for neighbor_signed in neighbors(node_signed):
			neighbor_rank = S.rank(neighbor_signed) 
			if reached[neighbor_rank] == 0:
				reached[neighbor_rank] = reached[node_rank]+1
				Q[num_reached] = neighbor_rank
				num_reached += 1
				if num_reached % 1000000 == 0:
					print("reached: " + str(num_reached) + " (" + str(Qindex) + ")")

	max_distance = max(reached)-1  # we start counting at 1
	return (num_reached, max_distance)


def usage():
	print("usage: 'PuckConnected n' where n is a positive even integer.")
	exit(0)


if __name__ == "__main__":
	main(sys.argv)
