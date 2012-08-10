import numpy as np

from diffeoplan.library.images.distance.distance_L2 import Distance_L2

class Tree():
    def __init__(self, root_node, metric=Distance_L2()):
        self.nodes = [root_node]
        self.distances = np.zeros((1, 1))
        self.size = 1
        self.metric = metric
        
    def add_node(self, node):
        self.nodes.append(node)
        self.distances = extend_distances(self.distances)
        self.size = len(self.nodes)
        self.calculate_distances(self.size - 1)
    
    def calculate_distances(self, node_index):
        for i in range(self.size):
#            pdb.set_trace()
            dist_i = self.metric.distance(self.nodes[node_index].y, self.nodes[i].y)
            self.distances[node_index, i] = dist_i
            self.distances[i, node_index] = dist_i
    
#def distance(y0, y1):
##    pdb.set_trace()
#    return UncertainImage.dist_values_L2(y0, y1)
        
def extend_distances(distances):
    """
        Takes a distances array as input and returns 
        the array with one more row and one more 
        column filled with zeros.
    """
#    s0, s1 = distances.shape
#    new_dist = np.zeros((s0,s1))
#    new_dist[:s0,:s1] = distances
    return extend_array(distances, np.array(distances.shape) + (1, 1))

def extend_array(array, size):
    """
        Takes a array as input and returns 
        the array with shape array.shape + extend.
    """
#    pdb.set_trace()
    s0, s1 = array.shape
    new_dist = -np.ones(size)
    new_dist[:s0, :s1] = array
    return new_dist