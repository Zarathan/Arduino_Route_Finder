from graph import *
from cost import *


edmonton_graph = load_data("edmonton-roads-2.0.1.txt")

start_lat = input("Please enter the latitude of the starting point.\n")
start_lon = input("Please enter the longitude of the starting point.\n")
end_lat = input("Please enter the latitude of the end point.\n")
end_lon = input("Please enter the longitude of the end point.\n")

start = (start_lat, start_lon)
end = (end_lat, end_lon)


def least_cost_path(G, start, dest, cost):

    component = depth_first_search(G, start)    # The component of "start".
    
    costs = {node:float("inf") for node in component.keys()}    # creates a dictionary containing
                                                                # each node of the component and a
                                                                # cost of infinity assigned to it.
    costs[start] = 0 # set the cost of the starting node to be 0.
    cheapest = start # "cheapest" is the variable that will run through Dijkstra's
    
    # Dijkstra's Algorithm.
    # At the end of this process, the dictionary "costs" SHOULD (untested) contain every node 
    # of the component and the shortest distance to get there.
    while component:
        adjacents = G.neighbours(cheapest)  # a list of neighbours of "cheapest"
        
        # update the cost of each neighbour:
        for node in adjacents:
            if costs[node] > cost(cheapest, node) + costs[cheapest]:
                costs[node] = cost(cheapest, node) + costs[cheapest]
                
        component.pop(cheapest) # delete the node from component
        cheapest = min(costs, key=costs.get) # find the NEW cheapest node.....this will search
                                             # through all of the nodes in "costs" and find the
                                             # one with least cost
