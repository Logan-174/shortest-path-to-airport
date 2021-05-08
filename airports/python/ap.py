import sys

import general
from hashmap import hashmap_t
import airports
import sp_algorithms
import weight
from weight import weight_t as w
import graph
from shortest_path import sssp_result_t

def msg0(s):
    general.msg(0, s)
def msg1(s):
    general.msg(1, s)

def dfs(g, src, dst):
    stat_edges_explored = 0
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    dist = [weight.weight_inf()]*N
    pred[src] = src
    dist[src] = weight.weight_t(0)
    node_queue = [src]
    visited = set([src])
    while node_queue:
        cur_node = node_queue.pop()
        if cur_node == dst:
            break
        for tgt in g.get_graph_succs(cur_node):
            if tgt.v not in visited:
                stat_edges_explored += 1
                pred[tgt.v] = cur_node
                dist[tgt.v] = weight.weight_add(dist[cur_node], tgt.w)
                node_queue.append(tgt.v)
                visited.add(tgt.v)
    return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)
def count_reachable(code):
    #
    # Print out the  number of airports reachable from airport code
    # Also count the start airport itself!
    #
    count = -1

    s = airports.ap_get_id(code)
    g = airports.ap_get_graph()
    r = dfs(g, s, -1)

    count = len([w for w in r.dist if w.weight_is_finite()])

    print("%d airports reachable from %s" % (count, code))

def compute_route(algo, scode, dcode):
    s = airports.ap_get_id(scode)
    d = airports.ap_get_id(dcode)
    g = airports.ap_get_graph()
    
    # Computer a shortest route between s and d, using the specified algorithm!
    # "bfs" should compute a route with minimal hops, all other algorithms compute a route with minimal milage
    #initialize variable
    path_result = None

    if (algo == "bellman-ford"):
        #get the result of using bfs algorithm
        path = sp_algorithms.bellman_ford(g, s)
        #transfer result into structure describing the result of a shortest path search between two nodes
        path_result = path.sssp_to_sp_result(d)

    elif (algo == "dijkstra"):
        path = sp_algorithms.dijkstra(g, s, d)
        path_result = path.sssp_to_sp_result(d)
    elif (algo == "astar"):
        N = airports.ap_get_num_ids()
        h = [None]*N
        for i in range(airports.ap_get_num_ids()):
            #if i is a valid node, calculate its distance away from node
            if airports.ap_is_valid_id(i):
                h[i] = airports.ap_get_dist(i, d)
            else:
                h[i] = weight.weight_inf()
        path_result = sp_algorithms.astar_search(g, s, d, h)

    elif (algo == "bfs"):
        path = sp_algorithms.bfs(g, s, d)
        path_result = path.sssp_to_sp_result(d)
    else:
        general.error("Invalid algorithm name: %s" % algo)
    
    if path_result.path == None:
        print("No route from %s to %s" % (scode, dcode))
    else:
        distance = 0
        N = path_result.path.nodes

        for i in range(len(N) - 1):
            distance = airports.ap_get_dist(N[i], N[i+1]).w + distance
            print("%s to %s (%dkm)" % (airports.ap_get_code(N[i]), airports.ap_get_code(N[i+1]), airports.ap_get_dist(N[i], N[i + 1]).weight_to_int()))
        print("Total = %dkm" % distance)
    msg0("relaxed %d edges\n" % path_result.relax_count)

airports.ap_std_init()
 
 
if (len(sys.argv) == 5 and sys.argv[1] == "route"):
    compute_route(sys.argv[2], sys.argv[3], sys.argv[4])
elif (len(sys.argv) == 3 and sys.argv[1] == "count"):
    count_reachable(sys.argv[2])
else:
    general.error("Invalid command line")
    
    
