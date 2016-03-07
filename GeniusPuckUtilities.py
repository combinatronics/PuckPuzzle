'''
Utility functions for working with the Genius Hockey Puck puzzle.
States of the puzzle are signed permutations of (even) n that begin with +1.
'''
from math import factorial

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


# Converts a signed permutation into a string and returns it.
def node_string(perm):
    n = len(perm)
    string = ""
    for i in perm:
        if n >= 10 and i > -10 and i < 10:
            string += " "
        if i > 0:
            string += " "
        string += str(i)
    return string

# Returns the total number of nodes in the underlying graph for any given n.
def total_nodes(n):
    return factorial(n-1) * 2**(n-1)


