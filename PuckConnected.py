'''
Determine the solvable instances of the Genius Hockey Puck puzzle.
States are modeled by signed permutations of (even) n that begin with +1.
So we are determining the connected componenent of the underlying graph that contains +1+2...+n.
'''

from SignedPermutations import SignedPermutations
from GeniusPuckUtilities import flip, neighbors, node_string, total_nodes
import sys

def main(argv):
	# Read in the value of n and make sure it is even.
	if len(argv) < 2: usage()
	n = int(argv[1])
	if n % 2 != 0 or n < 2: usage()

	# The start node is +1+2....+n.
	start = list(range(1,n+1))

	#
	distances = BFS(start)

	reached = [i for i, d in enumerate(distances) if d > -1]
	num_reached = len(reached)
	print(num_reached)
	print(total_nodes(n))
	print(total_nodes(n) / float(num_reached))

#
def BFS(start):
	n = len(start)
	S = SignedPermutations()
	distances = [-1] * S.total(n)
	distances[S.rank(start)] = 0
	Q = [start]
	while len(Q) > 0:
		node = Q.pop(0)
		distance = distances[S.rank(node)]
		for neighbor in neighbors(node):
			if distances[S.rank(neighbor)] == -1:
				distances[S.rank(neighbor)] = distance + 1
				Q.append(neighbor)
	return distances



def usage():
	print("usage: 'PuckConnected n' where n is a positive even integer.")
	exit(0)


if __name__ == "__main__":
	main(sys.argv)
