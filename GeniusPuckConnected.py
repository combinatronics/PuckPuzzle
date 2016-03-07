'''
Determine the solvable instances of the Genius Hockey Puck puzzle.
States are modeled by signed permutations of (even) n that begin with +1.
So we are determining the connected componenent of the underlying graph that contains +1+2...+n.
'''

from GeniusPuckUtilities import flip, neighbors, node_string, total_nodes
import sys

def main(argv):
	# Read in the value of n and make sure it is even.
	if len(argv) < 2: usage()
	n = int(argv[1])
	if n % 2 != 0 or n < 2: usage()
	
	# The start node is +1+2....+n.
	start = list(range(1,n+1))



	# Run one of two different versions.
	if False:

		# Run the verbose breadth-first search to find the distances with the reachable nodes.
		distances = BFS(start)

		# print out the results
		for (distance, node) in distances:
			sys.stdout.write(str(distance) + ":")
			print(node_string(node))
		print("total: " + str(len(distances)) + " out of " + str(total_nodes(n)))
		print(total_nodes(n) / float(len(distances)))

	else:

		# Run the simplified BFS.
		num = BFS_num(start)

		# print out the results
		print("total: " + str(num) + " out of " + str(total_nodes(n)))
		print(total_nodes(n) / float(num))


# Same as BFS but only returns the number of reached nodes.
def BFS_num(start):
	R = [start] # the reached nodes 
	current_pos = 0
	last_pos = 0 
	while current_pos <= last_pos:
		node = R[current_pos]
		for neighbor in neighbors(node):
			if neighbor not in R:
				R.append(neighbor)
				last_pos += 1
		current_pos += 1
	return last_pos+1


# Breadth-first search on the underlying graph.
def BFS(start):
	R = [start] # the reached nodes
	D = [(0, start)] # the reached nodes and distances
	Q = [(0, start)] # the queue of distances and nodes
	while len(Q) > 0:
		(distance, node) = Q.pop(0)
		for neighbor in neighbors(node):
			if neighbor not in R:
				R.append(neighbor)
				D.append((distance+1,neighbor))
				Q.append((distance+1,neighbor))
	return D



def usage():
	print("usage: 'GeniusPuckConnected n' where n is a positive even integer.")
	exit(0)


if __name__ == "__main__":
	main(sys.argv)

