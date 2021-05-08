import graph
import pq
import general
from shortest_path import sssp_result_t, sp_result_t
import weight

def bfs(g, src, dst):
    stat_edges_explored = 0
    
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    dist = [weight.weight_inf()]*N
    pred[src] = src
    dist[src] = weight.weight_zero()
    queue = [src]
    has_found = [src]
    while queue:
        u = queue[0]
        queue.remove(u)
        successors = g.get_graph_succs(u)
        for successor in successors:
            stat_edges_explored += 1
            if successor.v not in has_found:
                queue.append(successor.v)
                has_found.append(successor.v)
                pred[successor.v] = u
                dist[successor.v] = weight.weight_add(successor.w, dist[u])
                if successor.v == dst:
                    return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)
    return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)
    
def bellman_ford(g, src):
	stat_edges_explored = 0
	times = 0
	N = g.graph_get_num_nodes()
	pred = [graph.INVALID_NODE]*N
	dist = [weight.weight_inf()]*N
	has_neg = False
	flag = True
	pred[src] = src
	dist[src] = weight.weight_zero()

	edge = []
	for u in range(N):
		succs = g.get_graph_succs(u)
		succs = [r for r in succs if r.w != weight.weight_inf()]
		edge.extend([(u, succ) for succ in succs])

	while flag and times < N:
		flag = False
		for node in edge:
			stat_edges_explored += 1
			if weight.weight_less(weight.weight_add(dist[node[0]], node[1].w), dist[node[1].v]):
				dist[node[1].v] = weight.weight_add(dist[node[0]], node[1].w)
				pred[node[1].v] = node[0]
				flag = True
		times += 1
	
	for node in edge:
		if weight.weight_less(weight.weight_add(dist[node[0]], node[1].w), dist[node[1].v]):
			dist[node[1].v] = weight.weight_neg_inf()
			has_neg = True		


	return sssp_result_t(N, src, graph.INVALID_NODE, has_neg, pred, dist, stat_edges_explored)
	#general.error("Not implemented")
 	
def dijkstra(g, src, dst):

	stat_edges_explored = 0
	N = g.graph_get_num_nodes()
	pred = [graph.INVALID_NODE]*N
	dist = [weight.weight_inf()]*N

	pred[src] = src
	dist[src] = weight.weight_zero()

	node_queue = pq.DPQ_t(N)
	node_queue.DPQ_insert(src, dist[src])

	has_found = []

	
	while not node_queue.DPQ_is_empty():

		u = node_queue.DPQ_pop_min()
		if u in has_found:
			continue
		if u == dst:
			return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)

		has_found.append(u)
		succs = g.get_graph_succs(u)
		for node in succs:
			stat_edges_explored += 1
			if weight.weight_less(weight.weight_add(dist[u], node.w), dist[node.v]):
				dist[node.v] = weight.weight_add(dist[u], node.w)
				pred[node.v] = u
				if node_queue.DPQ_contains(node.v):
					node_queue.DPQ_decrease_key(node.v, dist[node.v])
				else:
					node_queue.DPQ_insert(node.v, dist[node.v])

	return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored) 

    #general.error("Not implemented")


def astar_search(g, src, dst, h):

	stat_edges_explored = 0

	N = g.graph_get_num_nodes()
	pred = [graph.INVALID_NODE]*N
	dist = [weight.weight_inf()]*N
	pred[src] = src
	dist[src] = weight.weight_zero()

	node_queue = pq.DPQ_t(N)
	node_queue.DPQ_insert(src, dist[src])
	has_found = []

	while not node_queue.DPQ_is_empty():
		u = node_queue.DPQ_pop_min()
		if u in has_found:
			continue
		if u == dst:
			return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored).sssp_to_sp_result(dst)
		has_found.append(u)
		succs = g.get_graph_succs(u)
		for node in succs:
			stat_edges_explored += 1
			if weight.weight_less(weight.weight_add(dist[u], node.w), dist[node.v]):
				dist[node.v] = weight.weight_add(dist[u], node.w)
				pred[node.v] = u
				if node_queue.DPQ_contains(node.v):
					node_queue.DPQ_decrease_key(node.v, weight.weight_add(dist[node.v], h[node.v]))
				else:
					node_queue.DPQ_insert(node.v, weight.weight_add(dist[node.v], h[node.v]))

	return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored).sssp_to_sp_result(dst)
    #general.error("Not implemented")

