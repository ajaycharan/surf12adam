from . import DiffeoPlanningAlgo, PlanningResult, contract
from .. import UncertainImage
from ..graph import Node, TreeConnector
from diffeoplan.configuration import get_current_config
from diffeoplan.library.graph.graph import Graph
from . import logger
 
class GraphSearch(DiffeoPlanningAlgo):
    """ 
        This is an algorithm that returns the best plan
        after trying all possible plans of exact length <nsteps> 

    """
    
    @contract(nsteps='int,>=1')
    def __init__(self, nsteps, thresh, metric, directions=1, max_ittr=1000):
        DiffeoPlanningAlgo.__init__(self)
        self.thresh = thresh
        self.nsteps = nsteps
        self.directions = directions
        self.max_ittr = max_ittr
        self.comp_ind = 0 # Dont look for nodes of lower inde than this
        config = get_current_config()
        self.metric = config.distances.instance(metric)
        
    @contract(y0=UncertainImage, y1=UncertainImage, returns=PlanningResult)
    def plan(self, y0, y1): #@UnusedVariable
        # print('Engering graphsearch plan()')
        dds = self.get_dds()
        
        ncmd = len(dds.actions)
        
        start_node = Node(y=y0, path=[])
        start_node.command_stack = range(ncmd)
        start_tree = Graph(start_node, self.metric, self.thresh)
        
        goal_node = Node(y=y1, path=[])
        goal_node.command_stack = range(ncmd)
        goal_tree = Graph(goal_node, self.metric, self.thresh)
        
        connector = TreeConnector(start_tree, goal_tree, self.thresh)

        def make_extra():
            """ Extra information to return about the search """
            extra = self.make_extra()
            extra['start_tree'] = start_tree
            extra['goal_tree'] = goal_tree
            extra['connector'] = connector
            return extra

                
        self.info('GraphSearch starting')
        while True:
            new_start_node = self.get_new_node(start_tree)
            self.info('Chosen new_start_node = %s' % new_start_node)
            if len(new_start_node.path) <= self.nsteps:
                start_tree.add_node(new_start_node)
            else:
                self.info('Breaking and failing.')
                break
            
            if self.directions == 2:
                new_goal_node = self.get_new_node(goal_tree)
                self.info('Goal node is %s.' % new_goal_node)
                if len(new_goal_node.path) <= self.nsteps:
                    goal_tree.add_node(new_goal_node)
                    
            nplans = connector.connect_update()
            if nplans > 0:
                plan = connector.get_connection()
                self.info('Returning plan: ' + str(plan))
                return PlanningResult(True, plan, 'Graph Search Plan',
                                      extra=make_extra())
        
        self.info('Planning failed.')
        return PlanningResult(False, None, 'GraphSearch failed',
                              extra=make_extra())
        
     
    @staticmethod
    def is_unique(path, tree):
        for p in tree.blocked:
#            pdb.set_trace()
            if list(p) == list(path):
                return False
        return True
    
    def get_new_node(self): # XXX: with tree or without?
        raise ValueError('not implemented')
        

    
    
        
