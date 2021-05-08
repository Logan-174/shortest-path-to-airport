from graph import graph_t, path_t, INVALID_NODE
from pq import DPQ_t
# import sp_algorithms

class sssp_result_t:
    def __init__(self, N, src, dst, ncyc, p, d, c):
        self.N = N
        self.src = src
        self.dst = dst
        self.pred = p
        self.has_negative_cycle = ncyc
        self.dist = d
        self.relax_count=c
        
    def sssp_to_sp_result(self, dst):
        p = None
        
        assert(self.dst == INVALID_NODE or self.dst == dst)
        
        if (not self.pred[dst] == INVALID_NODE):
            p = path_t(self.pred,dst)
            
        r = sp_result_t(self.src, dst, p, self.dist[dst], self.relax_count)
        
        return r
        
    def print_sssp_result(self, f):
        N = self.N
        if (N<10):
            NN = N
        else:
            NN = 10
       
        f.write("Distmap:")
        for i in range(0, NN):
            f.write(" ")
            self.dist[i].print_weight(f)
        
        if (N < NN):
            f.write("...\n")
        else:
            f.write("\n")
        
        
        
class sp_result_t:
    def __init__(self, src, dst, p, d, c):
        self.src = src
        self.dst = dst
        self.path = p
        self.dist = d
        self.relax_count = c
        
    def print_sp_result(self, f):
        f.write("Distance: ")
        self.dist.print_weight(f)
        f.write("\n")
        
        f.write("Path: ")
        print_path(f, self.path)
        f.write("\n")
        
        f.write("# Relaxed nodes: %d\n" % (self.relax_count))
        
def print_path(f, p):
    if (p == None):
        f.write("NULL")
    elif (p.path_len() == 0):
        f.write("EMP")
    else:
        f.write("%d" % (p.path_get(0)))
        for i in range(1, p.path_len()):
            f.write("%d" % (p.path_get(i)))
            

        

