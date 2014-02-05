from graph import *

class network:
    """
    A network is a data structure consisting of 3 objects: graphs, node_ids and
    edge_descriptor.
    This 'graphs' is an object of class graph. So for a network, it is going to 
    contain the information of all network nodes and the neighbours to which the
    node is connected to.
    The 'node_ids' is a dictionary, mapping an id to the nodes contained in graphs.
    It can be useful if you want to give a name/handle to your node. This name/handle
    should be of type that can be used for hashing (i.e. it should be immutable).
    The 'edge_descriptor' is similar to 'ids', but can be used for edges instead
    of nodes.  
    This particular implemention is for using using 'network' to create maps,
    Graphs = connection of intersections, 
    ids = names of intersections,
    descriptor= names of streets
    
    The same class can be modified and adapted for other uses, e.g.:     
    Social Networks: Graphs = user names that are connected by some connection,
    ids = unique ids (e.g. emails) assigned to each user,
    descriptor = description of the connection (friend, acquaintance, spouse, etc.)
    """
    def __init__(self, filename):
        self.graphs, self.node_ids, self.edge_descriptor = load_data(filename)
         
    #def find_nearest_id(self, lat, lon)

def load_data(filename):
    """
    Reads in 'filename', which a CSV file, and uses the data to build a network.
    The first value should be a 'V' or 'E' for each row, for a vertex or edge 
    respectively. 
    
    Make sure that 'filename' exists. Program will break if it is not found.
    
    Data syntax for V:
    V,<Vertex ID>,<Latitude>,<Longitude>
    
    Data syntax for E:
    E,<Vertex ID start>,<Vertex ID end>,<Optional Edge descriptor (string)>
    
    """
    print("Loading data...")
    g = Graph()
    id_index = dict()
    descriptor = dict()
    line_number = 0
    errored_lines = []
        
    f = open(filename, 'r')
    print("Map data CSV file successfully opened! Converting to graph...")
        
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
            if attempt == 1: 
                g.add_vertex((float(data[2]), float(data[3])))
                id_index[int(data[1])] = (float(data[2]), float(data[3])) 
        
        elif data[0] == 'E': # Edge
            if attempt == 2:
                if int(data[1]) in id_index.keys() and int(data[2]) in id_index.keys():    
                    g.add_edge((id_index[int(data[1])], id_index[int(data[2])]))

                    if len(data) == 4:
                        if data[3][-1] == "\n": descriptor[(id_index[int(data[1])], id_index[int(data[2])])] = data[3][:-1]
                        else: descriptor[(id_index[int(data[1])], id_index[int(data[2])])] = data[3]

                else: errored_lines.append(line_number)              
                        
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
    
    print("Data loaded.", end = "")
    print("Total successful lines = %d. Number of errored lines = %d" %(((file_len/2)-len(errored_lines)), len(errored_lines)))

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
                
    return g, id_index, descriptor     
