import sys

import general

INVALID_NODE = sys.maxsize

# Graph Data Structure

# def scan_node(f):

# def scan_raw_weight(f):

# def scan_weight(f):

class edge_tgt_t:
    def __init__(self, w, v):
        self.w = w
        self.v = v

    def _tgt_is_invalid(self):
        return self.v == INVALID_NODE
            
class succs_t:
    def __init__(self):
        self.n = 0
        self.capacity = 0
        self.a = []
        
    def succs_add(self, tgt):
        if (self.n >= self.capacity):
            self.capacity = (self.capacity + 1)*2
            aa = [None]*self.capacity
            for i in range(0, self.n):
                aa[i] = self.a[i]
            self.a = aa
        assert(self.n < self.capacity)
        self.a[self.n] = tgt
        self.n = self.n + 1
        
class graph_t:
    def __init__(self, num_nodes):
        assert(num_nodes < sys.maxsize)
        self.num_nodes = num_nodes
        if (not num_nodes == None):
            self.adjs = [None]*num_nodes
        else:
            self.adjs = None
        for i in range(0, num_nodes):
            self.adjs[i] = succs_t()
            
    def graph_check_node(self, u):
        if (not u < self.num_nodes):
            general.error("Node out of range: %d", u)
            
    def graph_get_num_nodes(self):
        return self.num_nodes
        
    def graph_add_edge(self, u, w, v):
        assert (not (u == v)), "self loop edge %d -> %d" % (u, v)
        assert(w.weight_is_finite())
        
        self.graph_check_node(u)
        self.graph_check_node(v)
        
        self.adjs[u].succs_add(edge_tgt_t(w, v))
        
    def graph_num_succs(self, u):
        return self.adjs[u].n
        
    def get_graph_succs(self, i):
        return self.adjs[i].a[0:self.adjs[i].n]
        
    # graph_read
    
    def graph_write(self, f):
        N = self.graph_get_num_nodes()
        num_edges = 0
        
        for u in range(0, N):
            num_edges += self.graph_num_succs(u)
            
        f.write("%d\n%d\n" % (N, num_edges))
        
        for u in range(0, N):
            for tgt in self.get_graph_succs(u):
                if (not tgt == None):
                    f.write("%d %d %d\n" % (u, tgt.v, tgt.w.weight_to_int()))
                else:
                    f.write("NONE\n")
                
class path_t:
    def set_up(self, len):
        self.len = len
        self.nodes = [None]*len
        for i in range(0, len):
            self.nodes[i] = INVALID_NODE
        
    def __init__(self, pred, v):
        # Determine length
        len = 0
        u = v
        
        while (True):
            len = len + 1
            if (u == pred[u]):
                break
            u = pred[u]
            
        self.set_up(len)
        u = v
        
        while (True):
            len = len - 1
            self.path_set(len, u)
            if (u == pred[u]):
                break
            u = pred[u]

    def path_set(self, i, u):
        assert (i < self.len)
        self.nodes[i] = u
    
    def path_get(self, i):
        assert(i < self.len)
        return self.nodes[i]
        
    def path_len(self):
        return self.len
        
        
        
