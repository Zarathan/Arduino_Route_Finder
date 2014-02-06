def cost_distance(e):
    """
    cost_distance will return the cost of an input edge, e, by finding the
    Euclidian distance between the two nodes of e (using Pythagorean's Theorem).

    e must be a tuple containing two nodes, and each node must also be a tuple.
    The format of a node is (latitude, longitude, id). The id qualifier is not 
    necessary to use this function.

    Examples:

    >>> edge = ((0, 0, "node1"), (0, 0, "node2"))
    >>> cost_distance(edge) == 0
    True
    
    >>> edge = ((3, 4, "node1"), (0, 0, "node2"))
    >>> cost_distance(edge) == 5
    True

    >>> edge = ((0, 0, "node1"), (3, 4, "node2"))
    >>> cost_distance(edge) == 5
    True
    
    >>> edge = ((2, 3, "node1"), (3, 4, "node2"))
    >>> cost_distance(edge) == 2**(1/2)
    True

    >>> edge = ((2, 3), (3, 4))
    >>> cost_distance(edge) == 2**(1/2)
    True
    """
    
    return ((e[1][0] - e[0][0])**2 + (e[1][1] - e[0][1])**2)**(1/2)
