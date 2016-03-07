'''
A*-Search framework for solving the Genius Hockey Puck using the fewest number of flips.
Note: The framework assumes that n is even in several places.
'''

import random
import Queue


# Create a random signed permutation starting with +1 with even sign-parity and return it.
# The "sign-parity" refers to the number of negative symbols in a signed permutation.
# For example, the sign-parity of [1,-3,2,-5,4] is even since there are two negatives.
def start(n):
    # Create a random permutation of {1,2,..n} that starts with 1.
    symbols = range(2,n+1)
    random.shuffle(symbols)
    perm = [1] + symbols

    # Assign +1 or -1 to each symbol randomly.
    for i in range(1,n):
        if random.getrandbits(1) == 1:
            perm[i] = -perm[i]

    # Compute the sign parity.
    # If it is odd, then change the sign of one symbol at random. 
    negatives = [x for x in perm if x < 0]
    signParity = len(negatives) % 2
    if signParity == 1:
        index = random.randint(1,n-1)
        perm[index] = -perm[index] 

    return perm


# Flip over n/2 consecutive symbols starting at index k and return the result.
# Each flip reverses the order and sign of the symbols involved in the flip.
# We need to keep the symbol +1 at index 0, so k must be in {1,2,...,n/2},
# where k is a 0-based index.
def flip(perm, k):
    # Make sure that k is in the proper range.
    m = len(perm) / 2
    assert(k >= 1 and k <= m)

    # Flip the m symbols and return the result.
    flipped = perm[0:k] + list(reversed([-x for x in perm[k:k+m]])) + perm[k+m:]
    return(flipped)


# Return the list of neighbors of a given signed permutation.
# See the documentation of flip() for a description of the neighbors.
# In this version of the problem all neighbors are reached using the same cost of 1.
def neighbors(perm):
    N = []
    m = len(perm) / 2
    for k in range(1,m+1):
        neighbor = flip(perm, k)
        N.append(neighbor)
    return N


# Test if the signed permutation is in a goal state and return the result.
# The only goal state is the signed permutation [1,2,...,n].        
def goal(perm):
    n = len(perm)
    return perm == range(1,n+1)


'''
Provide your heuristic(s) below.
Remember to provide heuristics that only give lower-bounds on the number of flips required.
Otherwise, A* search is not guaranteed to find an optimal solution (ie fewest number of flips).
One sample heuristic is provided.
'''

# This sample heuristic always returns 0.
# Note that this is always a lower-bound on the number flips required.
def zero(perm):
    return 0


# Run AStar search starting from the signed permutation using the given heuristic.
# An optimal path is returned.  In this case 'optimal' means fewest flips.
# The nodes in the path are signed permutations starting with +1 so no rotation information is given.
def AStar(perm, heuristic):
    # Make sure that there are an even number of symbols in the signed permutation.
    n = len(perm)
    assert(n % 2 == 0)

    # The frontier is a priority queue of 2-tuples of the form (cost, path).
    # (The priority queue will be prioritized by the first entry in the 2-tuple, ie cost.)
    # We initialize the queue with the starting signed permutation as a path along with its heuristic cost.
    frontier = Queue.PriorityQueue()
    past_cost = 0
    future_cost = heuristic(perm)
    total_cost = past_cost + future_cost 
    path = [perm]
    two_tuple = (total_cost, path)
    frontier.put(two_tuple)

    # Continue processing paths from the frontier until it is empty or we find a solution.

    # debugging, help!
    loops = 0

    while frontier.qsize() > 0 and loops < 1000:
        # Get the next path from the queue.
        # We also get the path's actual cost thus far and the last node (ie signed permutation) in the path.
        current_tuple = frontier.get()
        current_cost = current_tuple[0] 
        current_path = current_tuple[1]
        current_last_node = current_path[-1]

        # Check if the last node is a goal state, and if so return it.
        if goal(current_last_node):
            return current_path

        # Otherwise, consider all of the neighbors of the last node.
        N = neighbors(current_last_node)
        
        # debugging, help!
        random.shuffle(N)
        loops += 1
        print(frontier.qsize())
        print("last node")
        print(current_last_node)

        for neighbor in N:
            print("neighbor")
            print(neighbor)
            # Compute the estimated total cost from this neighbor to a goal state.
            # Then append the neighbor to the current path.
            # Add the resulting 2-tuple to the frontier.
            future_cost = heuristic(neighbor)
            total_cost = current_cost + future_cost 
            new_path = current_path + [neighbor]
            new_tuple = (total_cost, new_path)
            frontier.put(new_tuple)

    # If we did not find a solution then return None.
    return None

if __name__ == "__main__":
    n = 6 # n must be even

    # Create a random permutation and print it.
    perm = start(n)
    perm = [1,2,3,-6,-5,-4]
    perm = [1,6,-3,-2,-5,-4]
    #perm = [1,6,5,2,3,-4]
    perm = [1,-4,-3,-2,5,6]
    print(perm)
    print(neighbors(perm))
    #raise SystemExit, 0

    # Select a heuristic, then run A* search.
    heuristic = zero  # use your heuristic here for testing.
    solution_path = AStar(perm, heuristic)

    # Print out the solution if one was found.
    if solution_path == None:
        print("No solution found.")
    else:
        print("Solution found.")
        print(solution_path)

