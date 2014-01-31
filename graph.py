"""
Graph module for directed graph.

This module follows the same philosophy as the module designed in class, but
it is implemented specifically for map data.

All running time statements are under the assumption that it takes
O(1) time to index a dictionary.
"""

from collections import deque

class Graph:

    def __init__(self, V=set(), E=[]):
        """
        Create a graph with a given set of
        vertices and list of edges.
        For the purpose of this class
        We want E to be a list of tuples of the 2 vertex IDs.
        V is set of tuples, where each tuple is of the format
        (Vertex ID, Latitude, Longitude) of 1 vertex.
        
        If no arguements are passed in,
        the graph is an empty graph with
        no vertices and edges.

        Running time: O(len(V) + len(E))

        >>> g = Graph()
        >>> g._alist == {}
        True
        >>> g = Graph({(1,53.3,-118), (2,55,-120), (3,52,-119)}, {(1,2), (2,3)})
        >>> g._alist.keys() == set({(1,53.3,-118), (2,55,-120), (3,52,-119)})
        True
        >>> g._alist[(1,53.3,-118)]
        [(2, 55, -120)]
        >>> g._alist[3]
        []
        """

        # _alist is a dictionary that maps vertices to a list of vertices
        # i.e. _alist[v] is the list of neighbours of v
        # This also means _alist.keys() is the set of nodes in the graph
        self._alist = {}

        for v in V:
            self.add_vertex(v)

        for e in E:
            self.add_edge(e)
    
    def id_to_coord(self, v_id):
        """
        Returns a tuple of the form (latitude, longitude) of the given v_id (vertex id).
        
        >>> g = Graph({(1,53.3,-118), (2,55,-120), (3,52,-119)}, {(1,2), (2,3)})
        >>> g.id_to_coord(1)
        (53.3, -118)
        >>> g.id_to_coord(3)
        (52, -119)
        >>> g.id_to_coord(6)
        ()
        """
        
        
    def add_vertex(self, v):
        """
        Adds a vertex to our graph.
        If a vertex with same ID is given, the geo coordinates will be updated.
        
        Running time: O(1)
        
        >>> g = Graph()
        >>> g.add_vertex((1,52,-118))
        >>> (1,52,-118) in g._alist.keys()
        True
        >>> g.add_vertex((1,55,-120))
        >>> len(g._alist) == 1
        True
        >>> (1,52,-118) in g._alist.keys()
        False
        >>> (1,55,-120) in g._alist.keys()
        True
        """
        if v[0] not in self._alist.keys():
            self._alist[v] = []

    def add_edge(self, e):
        """
        Adds an edge to our graph.
        Do not add edge if the vertices
        for it do not exist. 
        Can add more than one copy of an edge.

        Running time: O(1)

        >>> g = Graph({1,2})
        >>> 2 in g._alist[1]
        False
        >>> g.add_edge((1,2))
        >>> 2 in g._alist[1]
        True
        >>> g.add_edge((1,2))
        >>> len(g._alist[1]) == 2
        True
        """
        if e[0] in self._alist.keys() and e[1] in self._alist.keys():
            self._alist[e[0]].append(e[1])

    def neighbours(self,v):
        """
        Given a vertex v, return a copy of the list
        of neighbours of v in the graph.
        
        >>> g = Graph()
        >>> g.neighbours(1)
        []
        >>> g = Graph({1,2,3}, [(1,2), (1,3)])
        >>> g.neighbours(1)
        [2, 3]

        Running time: O(len(self._alist[v]))
        (linear in the number of neighbours of v)
        """

        if v not in self._alist.keys():
            return []
        else:
            return list(self._alist[v]) 

    def vertices(self):
        """
        Returns a copy of the set of vertices in the graph.

        Running time: O(# vertices)

        >>> g = Graph({1,2,3}, [(1,2), (2,3)])
        >>> g.vertices() == {1,2,3}
        True
        """

        return set(self._alist.keys())

    def edges(self):
        """
        Create and return a list of the edges in the graph.

        Running time: O(# nodes + # edges)

        >>> g = Graph({1,2,3}, [(1,2), (2,3)])
        >>> g.edges()
        [(1, 2), (2, 3)]
        """
        
        edges = []
        for v,adj in self._alist.items():
            for u in adj:
                edges.append((v,u))
    
        return edges

    def is_vertex(self, v):
        """
        Returns true if and only if v is a vertex in the graph.
        This is more efficient then checking v in g.vertices().

        Running time: O(1)

        >>> g = Graph({1,2})
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(3)
        False
        """

        return v in self._alist.keys()

    def is_edge(self, e):
        """
        Returns true if and only if e is an edge in the graph.
        
        Running time: O(len(self._alist[e[0]]))
        linear in the number neighbours of e[0]

        >>> g = Graph({1,2}, [(1,2)])
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        False
        >>> g.is_edge((3,1))
        False
        """

        if not self.is_vertex(e[0]):
            return False
        return e[1] in self._alist[e[0]]

def is_walk(g, walk):
    """
    g is a graph and w is a list of nodes.
    Returns true if and only if w is a walk in g.

    Running time - O(d * m) where:
      - k = len(walk)
      - d = maximum size of a neighbourhood of a node
    In particular, if the graph has no repeated edges, then d <= # nodes.
    
    >>> g = Graph({1,2,3,4}, [(1,2), (2,3), (2,4), (4,3), (3,1)])
    >>> is_walk(g, [1,2,3,1,2,4])
    True
    >>> is_walk(g, [1,2,3,2])
    False
    >>> is_walk(g, [])
    False
    >>> is_walk(g, [1])
    True
    >>> is_walk(g, [5])
    False
    """
    
    for v in walk: # O(k)
        if not g.is_vertex(v): # O(1)
            return False

    if len(walk) == 0:
        return False

    # Note, can reduce the running time of the entire function
    # to O(k) if we implement the method is_edge to run in O(1) time.
    # This is a good exercise to think about.
    for node in range(0,len(walk)-1): # O(k)
        if not g.is_edge((walk[node], walk[node+1])): # O(d)
            return False
        
    return True

def is_path(g, path):
    """
    Returns true if and only if path is a path in g

    Running time: O(k*d)
    Specifically, is O(k) + running time of is_walk.

    >>> g = Graph({1,2,3,4}, [(1,2), (2,3), (2,4), (4,3), (3,1)])
    >>> is_path(g, [1,2,3,1,2,4])
    False
    >>> is_path(g, [1,2,3])
    True
    """

    return is_walk(g, path) and len(path) == len(set(path))
    
def breadth_first_search(g,start):
    """
    Find all nodes that can be reached from start in the graph g.
    
    Returns a dictionary 'reached' such that reached.keys() are all nodes that can be reached 
    from 'start' and reached[u] is the predecessor of u in the search.
    
    Running time : O(#nodes + #edges)
    More specifically, O(# edges (u,w) with u reachable from start)
    
    This will give a longer path than depth_first_search
    
    >>> g = Graph({1,2,3,3,4,5,6}, [(1,2), (1,3), (2,5), (3,2), (4,3), (4,5), (4,6), (5,2), (5,6)])
    >>> reached = breadth_first_search(g, 1)
    >>> reached.keys() == {1,2,3,5,6}
    True
    >>> g.is_edge((reached[6], 6))
    True
    >>> g = Graph({1,2,3}, [(1,2), (3,2)])
    >>> reached = breadth_first_search(g, 2)
    >>> reached.keys() == {2}
    True
    """
    
    reached = {}

    stack = deque([(start,start)])

    # running time: each edge (x,u) will be added to stack at most once
    while stack:
        
        # O(1)
        node, prev  = stack.pop() # ) 
        
        # the following statement will be processed at most once per node
        if node not in reached.keys():
            reached[node] = prev
    
            # (len(g.neighbours(node)))
            # each edge (x,u) will be considered at most once here            
            # total work over all executions of the loop is O(# edges)
            for nbr in g.neighbours(node):
                stack.append((nbr,node))
    return reached    
    
def depth_first_search(g,start):
    """
    Find all nodes that can be reached from start in the graph g.
    
    Returns a dictionary 'reached' such that reached.keys() are all nodes that can be reached 
    from 'start' and reached[u] is the predecessor of u in the search.
    
    Running time : O(#nodes + #edges)
    More specifically, O(# edges (u,w) with u reachable from start)

    This will give shortest path    
    >>> g = Graph({1,2,3,3,4,5,6}, [(1,2), (1,3), (2,5), (3,2), (4,3), (4,5), (4,6), (5,2), (5,6)])
    >>> reached = depth_first_search(g, 1)
    >>> reached.keys() == {1,2,3,5,6}
    True
    >>> g.is_edge((reached[6], 6))
    True
    >>> g = Graph({1,2,3}, [(1,2), (3,2)])
    >>> reached = depth_first_search(g, 2)
    >>> reached.keys() == {2}
    True
    """
    
    # This gives a shortest path because if a node is found at a depth,
    # it was not there in the 1 lower level of depth. 
    reached = {}
    queue = deque([(start,start)])

    # running time: each edge (x,u) will be added to queue at most once
    while queue:
        
        # O(1), not O(len(queue))) because deque is used
        node, prev  = queue.popleft() 
        # This will ensure that shortest paths are returned
        
        # the following statement will be processed at most once per node
        if node not in reached.keys():
            reached[node] = prev
    
            # (len(g.neighbours(node)))
            # each edge (x,u) will be considered at most once here            
            # total work over all executions of the loop is O(# edges)
            for nbr in g.neighbours(node):
                queue.append((nbr,node))
    return reached    

# Exercise 2 function
def count_components(g):
    """
    Returns the number of connected components in the graph g.
    
    g should be an undirected graph, i.e., for every edge {u,v}, there should be
    an edge {v,u} in g as well. Failure to do this will produce unpredicatable
    results.
    
    A connected component of an undirected graph is a subset of vertices C such 
    that there is a path between any two nodes in C and there is no path between
    a node in C and a node lying outside of C.
    
    Runtime: O(# of nodes + # of edges)
    
    >>> g = Graph({1,2,3,4,5,6}, [(1,2), (2,1), (3,4), (4,3), (3,5), (5,3), (4,5), (5,4)])
    >>> count_components(g)
    3
    >>> g.add_edge((1,4))
    >>> g.add_edge((4,1))
    >>> count_components(g)
    2
    """

    rv = 0
    queue = deque(g.vertices()) # O (# of nodes)
    
    # The following while loop will be run once per connected component. It will start 
    # from the "parent" node of the component (first one in queue)
    # and WILL NOT be run AGAIN for other members of the component.
    while queue: # O (# of connected components)

        start = queue.popleft()

        connected_vertices = list(depth_first_search(g,start).keys()) 
        # For above, O (# of nodes reachable from start + (# of edges (u,w) with u reachable from start))
        # => O (# nodes in component + # edges in component)
        
        for vertex in connected_vertices: # O (# nodes in the component)
            if vertex in queue: queue.remove(vertex)
        
        rv += 1
    return rv
    
    # net complexity = O (# of nodes + # of connected components*(2* # of nodes in component + # of edges in component ))
    #                = O (# nodes + # edges) [ignoring any constants terms and factors]
    
def load_data(filename):
    """
    Reads in 'filename', which a CSV file. The first value should be a 'V' or
    'E' for each row, for a vertex or edge respectively. 
    
    Make sure that 'filename' exists. Program will break if it is not found.
    
    Data syntax for V:
    V, <Vertex ID>, <Latitude>, <Longitude>
    
    Data syntax for E:
    E, <Vertex ID start>, <Vertex ID end> <Edge name>
    
    >>>
    >>>
    """
    print("Loading data...\n")
    line_number = 0
    errored_lines = []
    g = Graph()
    
    f = open(filename, 'r')
    print("Map data CSV file successfully opened! Converting to graph...\n")
    
    for i,l in enumerate(f): pass # Source: http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    file_len = i + 1
    f.seek(0)
    
    print("Progress: |" + 100*" " + "| 0 %", end = "") # Progress bar
    last_per = 0
    
    for line in f:
        line_number += 1
        data = line.strip()
                
        if data[0] = 'V': # Vertex
            g.add_vertex(data[1], data[2], data[3])
        elif data[0] = 'E': # Edge
            g.add_edge((data[1], data[2]))
        else: # Incorrect data type
            errored_lines.append(line_number)
        
        # Following is the progress bar printer
        if int((line_number/file_len)*100 - last_per) >= 1: 
           new_per = (line_number*100//file_len)
           print((105-last_per)*"\u0008" + (new_per-last_per)*"*" + (100-new_per)*" " + "| " + str(new_per) + "%", end="")
           last_per = new_per
    
    print("\n")
    f.close() 
    
    print("Data loaded. Number of errors = " + len(errored_lines))

    if len(errored_lines) != 0: 
        print("Errored lines: " + errored_lines)
        print("All the recognised lines have been loaded.
        
        while(1):
            decision = input("Do you want to edit the file " + filename + " and try loading data again? (Y/N)")
            if decision == 'Y' or decision == 'y':
                cont = input("Press any key when done editing the file.")
                g = load_data(filename)
                break
                
            elif decision == 'N' or decision == 'n': break
        
            else:
                print("Unrecognised input. Try again.")       
                
    return g    
