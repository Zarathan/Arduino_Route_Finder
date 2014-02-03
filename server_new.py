from graph import *
from cost import *


edmonton_graph = load_data("edmonton-roads-2.0.1.txt")

start_lat = input("\n\nPlease enter the latitude of the starting point.\n")
start_lon = input("Please enter the longitude of the starting point.\n")
end_lat = input("Please enter the latitude of the destination point.\n")
end_lon = input("Please enter the longitude of the destination point.\n")

start = (float(start_lat), float(start_lon))
dest = (float(end_lat), float(end_lon))


def least_cost_path(G, start, dest, cost):
    """
    Returns the shortest (cheapest) path from the starting node to destination node, given
    a graph G and a cost function. 
    
    If the destination cannot be reached from the starting node, return None.
    If the starting and destination nodes are equal, return [start].
    
    
    
    Examples:
    
    >>> g = Graph({(1, 2), (2, 3), (3, 4), (4, 5)}, [((1, 2), (2, 3)), ((2, 3), (3, 4)), ((2, 3), (4, 5)), ((1, 2), (3, 4)), ((3, 4), (4, 5))])
    """
    
    
    if start == dest:
        return [start]

        
    # Find the component associated with "start". This component will be used in
    # Dijkstra's algorithm instead of using the entire graph.
    component = depth_first_search(G, start)    
    visited_edges = list()
    visited = set()
    shortest_path = []
    
    
    # If the destination is not connected to the start, exit.
    if dest not in component:
        return None
    
    
    # Assign the cost of each node (in the component) to infinity.
    # Assign the starting cost to be 0.
    costs = {node:float("inf") for node in component.keys()}
    costs[start] = 0
    cheapest = start
    
    
    # Dijkstra's Algorithm:
    while component:
    
        # Find the neighbours of the current node.
        adjacents = G.neighbours(cheapest)
        
        # Update the cost of each neighbour. A neighbour is only updated if the calculated
        # cost is less than the cost previously assigned.
        for node in adjacents:
            if node not in visited:
                if costs[node] > cost((cheapest, node)) + costs[cheapest]:
                    costs[node] = cost((cheapest, node)) + costs[cheapest]
                    
        # Updated the set of visited nodes.
        visited = visited | {(cheapest)}
        
        # Remove the current node from the component and from costs (to avoid
        # repeated computations).
        component.pop(cheapest)
        if len(costs) != 1:
            previous = costs.pop(cheapest)
        
        # Find the (new) minimum-cost node in the graph; it will be the new "current node".
        cheapest = min(costs, key=costs.get)
            
        # Search through the neighbours of the current node to find out where it came from.
        # Add the edge from which it came into visited_edges.
        for neighbour in G.neighbours(cheapest):
            if neighbour in visited:
                if cost((neighbour, cheapest)) == costs[cheapest] - previous:
                    visited_edges.append((neighbour, cheapest))
                    
        # If the current node is the destination node, form the shortest_path list
        # by working backwards from the destination. (Travel backwards edge-to-edge
        # until you reach the starting node).        
        if cheapest == dest:
            shortest_path.append(cheapest)
            while visited_edges:
                for neighbour in G.neighbours(cheapest):
                    if (neighbour, cheapest) in visited_edges:
                        visited_edges.remove((neighbour, cheapest))
                        shortest_path.append(neighbour)
                        cheapest = neighbour
                        if cheapest == start:
                            shortest_path.reverse()
                            return shortest_path
                        break

    return None
    
    
path = least_cost_path(edmonton_graph, start, dest, cost_distance)
    
       
