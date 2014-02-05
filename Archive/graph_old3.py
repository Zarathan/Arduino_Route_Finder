"""
Graph module for directed graph.

The data is stored as a dict where the keys are tuples of the vertex coordinates
of the form (latitude, longitude). Tuples are immutable so can be used for hashing.
Also, the client requests come in the form of (lat, long), so runtime should be better
than the class graph_old.py which hashes on vertex IDs.
The value of each key is a list consisting of 1 list and 1 int (optional):
    => The list contains the coordinates (tuples) of all the neighbours of that vertex.
       List is being used as neighbours could need updating as the map progresses.
    => The int is the ID of that vertex as mentioned in the database. This is added
       only if it was provided. Since a general mapping is done between coordinates,
       this is not a mandatory piece of information. Even if it is provided,
       all the data processing is done in terms of coordinates (after processing 
       the ID). The ID is just stored for future references.
    
A compromise between runtime during the program and during data load has to be made.
If the dict is hashed using IDs, converting CSV to graph is faster as the edges
are stored as pairs of IDs. But, running client requests will be slower as the client
provides and demands data in form of coordinates. As seen in graph_old.py, pulling
IDs from coordinates and then processing it is slower because the dict keys are IDs.
Instead here, the dict keys are coordinates, so looking up neighbours will be O(1). 

This comes at a cost of data loading runtime, as the program will have to convert
the links stated as a pair of IDs to a link in coordinate tuples. 

Since, loading is just done once, this tradeoff is preferred.  

SO in nutshell, all the processing and data management is done in terms of coordinates.
Nevertheless, IDs can be used as handles for these coordinates if they were mentioned.
"""

from collections import deque

class Graph:

    def __init__(self, V=set(), E=[]):
        """
        Create a graph with a given set of vertices and list of edges.
        E is a list of tuples of the 2 vertex coordinates of the form ((start lat, start lon), (end lat, end lon)).
        V is set of tuples, where each tuple is of the format
        (Latitude, Longitude, Vertex ID(optional)) of 1 vertex.
        
        If no arguements are passed in, the graph is an empty graph with
        no vertices and edges.

        If IDs of vertices are provided, edges can be stated in the form of tuples of 
        vertex IDs. Runtime will be slower as reverse lookup in a dict will be used.
        IDs will also be stored as a ._map_data[(coordinates)][1]
        If no IDs are stated in vertices, but edges are mentioned as IDs, those edges will be ignored.
        
        The two data entry methods are demonstrated as below.
        
        >>> g = Graph()
        >>> g._map_data == {}
        True
        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3)])
        >>> g._map_data.keys() == set({(53.3,-118), (55,-120), (52,-119)})
        True
        >>> g._map_data[(53.3,-118)]
        [[(55, -120)], 1]
        >>> g._map_data[(52,-119)]
        [[], 3]
        >>> g._map_data[(55,-120)]
        [[(52, -119)], 2]
        >>> g = Graph({(53.3,-118), (55,-120), (52,-119)}, [((53.3,-118), (55,-120)), ((55,-120), (52,-119))])
        >>> g._map_data.keys() == set({(53.3,-118), (55,-120), (52,-119)})
        True
        >>> g._map_data[(53.3,-118)]
        [[(55, -120)]]
        >>> g._map_data[(52,-119)]
        [[]]
        >>> g._map_data[(55,-120)]
        [[(52, -119)]]
        >>> g.add_edge((1,3))
        >>> g.is_edge(((53.3,-118), (52,-119)))
        False
        >>> g.is_edge((1,3))
        False
        """

        self._map_data = {}
        self._id_index = {}
                
        for v in V:
            self.add_vertex(v)

        for e in E:
            self.add_edge(e)
    
    def id_to_coord(self, v_id):
        """
        Returns a tuple of the form (latitude, longitude) of the given v_id (vertex id).
        Useful only if the optional data vertex ID was given during graph generation.
        
        Returns () if no such ID is found. 
        
        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-115)}, [(1,2), (2,3)])
        >>> g.id_to_coord(1)
        (53.3, -118)
        >>> g.id_to_coord(3)
        (52, -119)
        >>> g.id_to_coord(6)
        ()
        """
        if v_id in self._id_index.keys(): return self._id_index[v_id]
        else: return ()
        
    def coord_to_id(self, coord):
        """
        Returns the ID of the passed coordinates of a vertex as a tuple: (latitude, longitude)
        
        Returns None if no such coordinates are found, or if the coordinates do 
        not have any ID associated with them.
        
        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-115)}, [(1,2), (2,3)])
        >>> g.coord_to_id((53.3, -118))
        1
        >>> g.coord_to_id((52, -119))
        3
        >>> g.coord_to_id((89, 82))
        >>> g.coord_to_id((59,-115))
        """
        if coord not in self._map_data.keys(): return None
        elif len(self._map_data[coord]) == 1: return None
        else: return self._map_data[coord][1] # Can directly return without any risk becuase int is immutable
        
    def add_vertex(self, v):
        """
        Adds a vertex to our graph.
        If a vertex with the same coordinates is given, but this time an ID is 
        specified, the ID will added to the graph. But if there was an ID 
        earlier, but this time an ID is not mentioned, the ID will NOT be removed.
        
        Warning: If different vertex coordinates with an already used ID is added, 
        this ID is assigned to the new vertex. 
        
        Running time: O(1)
        
        >>> g = Graph()
        >>> g.add_vertex((52,-118,1))
        >>> (52,-118) in g._map_data.keys()
        True
        >>> g._map_data[(52,-118)]
        [[], 1]
        >>> g.add_vertex((55,-120,1))
        >>> g._map_data[(55,-120)]
        [[], 1]
        >>> g._map_data[(52,-118)]
        [[]]
        >>> g.add_vertex((55,-120,2))
        >>> g._map_data[(55,-120)]
        [[], 2]
        >>> g.id_to_coord(1)
        ()
        """
        if (v[0], v[1]) not in self._map_data.keys():
            self._map_data[(v[0], v[1])] = [[]]

        if len(v) == 3: # If ID is passed. Either ID needs to be added or update
            if len(self._map_data[(v[0], v[1])]) == 1: # The vertex did not already have any ID assigned
                self._map_data[(v[0], v[1])].append(v[2])

                if v[2] in self._id_index.keys(): # But v[2] is already used by some other coordinates!
                    temp = self._id_index[v[2]] # The other coordinates
                    self._map_data[temp] = [self._map_data[temp][0]] # Delete this ID from the other coordinates                    
                
                self._id_index[v[2]] = (v[0], v[1]) # Adding the new coordinates to ID index
                
            else: # The vertex has an old ID assigned. Needs updating
                temp = self._map_data[(v[0], v[1])][1] # Old ID
                self._map_data[(v[0], v[1])][1] = v[2] # Add new ID to coordinate data
                self._id_index.pop(temp) # Remove old ID from ID index
                self._id_index[v[2]] = (v[0], v[1]) # Add new ID to ID index
                                    
    def add_id(self, v, v_id):
        """
        Adds an ID (v_id) to an already existent vertex (v). If the vertex does not  
        exist, it will not do anything. If the vertex already has an ID, updates the ID.
        
        It calls the .add_vertex method itself. But it ensures that the vertex exists first.
        Can be useful if you want to add an ID, only if the vertex exists, but are 
        unsure if the vertex exists.
        
        >>> g = Graph()
        >>> g.add_vertex((52,-118,1))
        >>> g.add_id((52,-118), 2)
        >>> g.coord_to_id((52,-118))
        2
        >>> g.add_id((55,-115), 1)
        >>> g.id_to_coord(1)
        ()
        >>> g._map_data[(52,-118)]
        [[], 2]
        """
        
        if v in self._map_data.keys(): self.add_vertex((v[0], v[1], v_id))
        
    def add_edge(self, e):
        """
        Adds an edge to our graph. The edge should be of the form: 
        ((start_lat, start_lon), (end_lat, end_lon)). 
        If IDs were mentioned for the corresponding start and/or end vertices,
        this format can be used to (though slower):
        (v_id_start, (end_lat, end_lon)).
        
        where v_id1 and v_id2 should be the IDs of 2 vertices already in graph.
        Can add more than one copy of an edge.

        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)})
        >>> g.id_to_coord(2) in g._map_data[g.id_to_coord(1)][0]
        False
        >>> g.add_edge((1,2))
        >>> g.id_to_coord(2) in g._map_data[g.id_to_coord(1)][0]
        True
        >>> g.add_edge((1,2))
        >>> len(g._map_data[g.id_to_coord(1)][0]) == 2
        True
        """
        start = e[0]
        end = e[1]
        
        if type(e[0]) is int:
            start = self.id_to_coord(e[0])
        if type(e[1]) is int:
            end = self.id_to_coord(e[1])      
        
        if start in self._map_data.keys() and end in self._map_data.keys():
            self._map_data[start][0].append(end)
    

    def neighbours(self,v):
        """
        Given a vertex v, return a copy of the list
        of neighbours of v in the graph.
        v should be of the form (lat, lon). If the graph contains an ID for that 
        vertex, v can also be the ID for that vertex (slower).
        
        Returns None if the vertex is not found (both in coordinate or ID form).
        (to differentiate from the case where the vertex is actually found 
        but has no neighbours....[] is returned in that case)
        
        Running time: O(len(self._map_data[v]))
        (linear in the number of neighbours of v)        

        >>> g = Graph()
        >>> g.neighbours(1)
        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3), (1,3)])
        >>> g.neighbours(1)
        [(55, -120), (52, -119)]
        >>> [g.coord_to_id(i) for i in g.neighbours(1)]
        [2, 3]
        """
        if type(v) is int: 
            v = self.id_to_coord(v)
            
        if v not in self._map_data.keys():
            return None 
        else:
            return list(self._map_data[v][0]) 

    def vertices(self):
        """
        Returns a copy of the set of vertices in the graph.

        Running time: O(# vertices)

        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3)])
        >>> g.vertices() == {(53.3,-118), (55,-120), (52,-119)}
        True
        """

        return set(self._map_data.keys())

    def edges(self):
        """
        Create and return a list of the edges in the graph.

        Running time: O(# nodes + # edges)

        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3)])
        >>> set(g.edges()) == {((53.3, -118), (55, -120)), ((55, -120), (52, -119))}
        True
        """
        
        rv = []
        for coord,data in self._map_data.items():
            for u in data[0]:
                rv.append((coord,u))
    
        return rv

    def ids(self):
        """
        Returns a copy of set of all IDs and their in the graph. The
        returned value only contains those vertices whose IDs existed in graph.
        
        
        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3)])
        >>> g.ids() == {(1, (53.3, -118)), (2, (55, -120)), (3, (52, -119))}
        True
        >>> g.add_vertex((45, -130))
        >>> g.ids() == {(1, (53.3, -118)), (2, (55, -120)), (3, (52, -119))}
        True
        >>> g.vertices() == {(53.3,-118), (55,-120), (52,-119)}
        False
        """
        return set(self._id_index.items())

    def is_vertex(self, v):
        """
        Returns true if and only if v is a vertex in the graph. v should be a 
        tuple: (lat, long), or its ID if there is one (slower).

        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3)])
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(4)
        False
        >>> g.add_vertex((55, -150))
        >>> g.is_vertex((55, -150))
        True
        >>> g.is_vertex((150, -200))
        False
        """
        if type(v) is int: v = self.id_to_coord(v)

        return v in self._map_data.keys()

    def is_edge(self, e):
        """
        Returns true if and only if e is an edge in the graph. e should be a 
        tuple: ((start_lat, start_lon), (end_lat, end_lon)), or (v_id1, v_id2)
        if IDs exist for those vertices (or a combination of IDs and coordinates)
        
        >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3)}, [(1,2), (2,3)])
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        False
        >>> g.is_edge((3,1))
        False
        >>> g.is_edge((1,(55,-120)))
        True
        >>> g.is_edge(((53.3,-118), (52,-119)))
        False
        """
        start = e[0]
        end = e[1]
        
        if type(e[0]) is int: start = self.id_to_coord(e[0])
        if type(e[1]) is int: end = self.id_to_coord(e[1])
        
        if not self.is_vertex(start):
            return False
        return end in self._map_data[start][0]

def is_walk(g, walk):
    """
    g is a graph and w is a list of nodes.
    Returns true if and only if w is a walk in g.

    Running time - O(d * m) where:
      - k = len(walk)
      - d = maximum size of a neighbourhood of a node
    In particular, if the graph has no repeated edges, then d <= # nodes.
    
    >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-125,4)}, [(1,2), (2,3), (3,1), (2,4)])
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

    >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-125,4)}, [(1,2), (2,3), (3,1), (2,4)])
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
    
    >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-125,4), (54,-130,5), (51,-115,6)}, [(1,2), (1,3), (2,5), (3,2), (4,3), (4,5), (4,6), (5,2), (5,6)])
    >>> reached = breadth_first_search(g, 1)
    >>> reached.keys() == {(53.3,-118),(55,-120),(52,-119),(54,-130),(51,-115)}
    True
    >>> g.is_edge((reached[(51,-115)], (51,-115)))
    True
    >>> g = Graph({(52.5,-119,1),(53,-120,2),(51,-122,3)}, [(1,2), (3,2)])
    >>> reached = breadth_first_search(g, (53,-120))
    >>> reached.keys() == {g.id_to_coord(2)}
    True
    """
    if type(start) is int: start = g.id_to_coord(start) 
    
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
    >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-125,4), (54,-130,5), (51,-115,6)}, [(1,2), (1,3), (2,5), (3,2), (4,3), (4,5), (4,6), (5,2), (5,6)])
    >>> reached = breadth_first_search(g, 1)
    >>> reached.keys() == {(53.3,-118),(55,-120),(52,-119),(54,-130),(51,-115)}
    True
    >>> g.is_edge((reached[(51,-115)], (51,-115)))
    True
    >>> g = Graph({(52.5,-119,1),(53,-120,2),(51,-122,3)}, [(1,2), (3,2)])
    >>> reached = breadth_first_search(g, (53,-120))
    >>> reached.keys() == {g.id_to_coord(2)}
    True
    """
    if type(start) is int: start = g.id_to_coord(start)
    
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
    
    >>> g = Graph({(53.3,-118,1), (55,-120,2), (52,-119,3), (59,-125,4), (54,-130,5), (51,-115,6)}, [(1,2), (2,1), (3,4), (4,3), (3,5), (5,3), (4,5), (5,4)])
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
    V,<Vertex ID>,<Latitude>,<Longitude>
    
    Data syntax for E:
    E,<Vertex ID start>,<Vertex ID end>,< Optional Edge name>
    
    """
    print("Loading data...\n")
    line_number = 0
    errored_lines = []
    g = Graph()
    
    f = open(filename, 'r')
    print("Map data CSV file successfully opened! Converting to graph...\n")
    
    
    for i,l in enumerate(f): pass # Source: http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    file_len = 2*(i + 1)
    f.seek(0)
    
    print("Progress: |" + 99*" " + "|   0 %%", end = "") # Progress bar
    last_per = 0
    
    attempt = 1
    for line in f:
        line_number += 1
        data = line.split(sep=",")
                
        if data[0] == 'V': # Vertex
            if attempt == 1: g.add_vertex((float(data[2]), float(data[3]), int(data[1])))
        elif data[0] == 'E': # Edge
            if attempt == 2: g.add_edge((int(data[1]), int(data[2])))
        else: # Incorrect data type
            if attempt == 1: errored_lines.append(line_number)
        
        if line_number == file_len/2:
            f.seek(0)
            attempt = 2
         
        # Progress bar printer
        new_per = (line_number*100//file_len)
        if new_per - last_per >= 1:
            print((107-last_per)*"\u0008" + (new_per-last_per)*"*" + (100-new_per)*" " + "| %3.0f %%" %new_per, end="")
        last_per = new_per
    
    print("\n")
    
    f.close() 
    
    print("Data loaded. Total successful lines = %d. Number of errored lines = %d" %(((file_len/2)-len(errored_lines)), len(errored_lines)))

    if len(errored_lines) != 0: 
        print("Errored lines: " + str(errored_lines))
        print("All the recognised lines have been loaded.")
        
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
