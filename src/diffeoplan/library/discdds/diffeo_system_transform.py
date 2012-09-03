from . import np, logger
from boot_agents.diffeo import Diffeomorphism2D, diffeo_stats
from diffeoplan.configuration import get_current_config
from diffeoplan.library.discdds import DiffeoAction, DiffeoSystem

def HardChoiceIso(id_dds, info_percentile):
    """ Instantiates the given DDS and changes it. """
    config = get_current_config()
    dds = config.discdds.instance(id_dds)
    ddst = make_hard_choices(dds, info_threshold=None,
                             use_isomorphism_heuristics=True,
                             info_percentile=info_percentile)
    return ddst


def make_hard_choices(dds, info_threshold=0.5, use_isomorphism_heuristics=True,
                      info_percentile=50):
    """ Applies a threshold to the uncertainty of the diffeomorphisms """ 
    
    def make_hard(dd):
        assert isinstance(dd, Diffeomorphism2D)
        if use_isomorphism_heuristics:
            stats = diffeo_stats(dd.d)
            limit = np.percentile(stats.norm, info_percentile) / 3.0
            #print('norm mean/mean: %g %g' % (np.mean(stats.norm), np.median(stats.norm)))            
            #for i in range(0, 100, 5):
            #    print(' %3d%% = %g' % (i, np.percentile(stats.norm, i)))
            #limit = np.percentile(stats.norm, info_percentile)
            #if limit <= 1:
            #    print('limit was %g' % limit)
            #    limit = 4
            variance = (stats.norm > limit).astype('float')
            logger.info('limit: %g pixels' % limit)
            logger.info('visibility: %g' % np.mean(dd.variance))
        else:
            variance = (dd.variance > info_threshold).astype('float')
        return Diffeomorphism2D(dd.d, variance)
    
    def make_hard_action(a):
        label = a.label + '_inv'
        diffeo = make_hard(a.get_diffeo2d_backward())
        diffeo_inv = make_hard(a.get_diffeo2d_forward())
        original_cmd = a.original_cmd
        return DiffeoAction(label, diffeo, diffeo_inv, original_cmd)
    
    actions = map(make_hard_action, dds.actions)
    label = dds.label + '_inv'    
    return DiffeoSystem(label, actions)
