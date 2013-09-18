import draw_func2 as df2
from PIL import Image, ImageOps
from os.path import realpath, join
import helpers
import fileio as io
import imp
import matplotlib.pyplot as plt
import numpy as np
import os
import params
import pyflann
import sklearn.decomposition
import sklearn.preprocessing as sklpreproc
import sys
import sklearn
import scipy as sp
import signal
import scipy.sparse as spsparse
#print('LOAD_MODULE: algos.py')
#imp.reload(sys.modules['hotspotter.helpers'])
#imp.reload(sys.modules['params'])

# reloads this module when I mess with it
def reload_module():
    import imp
    import sys
    imp.reload(sys.modules[__name__])
def rrr():
    reload_module()

def xywh_to_tlbr(roi, img_wh):
    (img_w, img_h) = img_wh
    # Ensure ROI is within bounds
    (x, y, w, h) = roi
    x1 = max(x,0)
    y1 = max(y,0)
    x2 = min(x+w, img_w-1)
    y2 = min(y+h, img_h-1)
    return (x1, y1, x2, y2)


def localmax(signal1d):
    maxpos = []
    nsamp = len(signal1d)
    for ix in xrange(nsamp):
        _prev = signal1d[max(0, ix-1)]
        _item = signal1d[ix]
        _next = signal1d[min(nsamp-1, ix+1)]
        if (_item >= _prev and _item >= _next) and\
           (_item != _prev and _item != _next):
            maxpos.append(ix)
    return maxpos

def viz_localmax(signal1d):
    #signal1d = np.array(hist)
    signal1d = np.array(signal1d)
    maxpos = np.array(localmax(signal1d))
    x_data = range(len(signal1d))
    y_data = signal1d
    fig = df2.figure('localmax vizualization')
    df2.plot(x_data, y_data)
    df2.plot(maxpos, signal1d[maxpos], 'ro')
    df2.update()


def sparse_normalize_rows(csr_mat):
    return sklpreproc.normalize(csr_mat, norm='l2', axis=1, copy=False)

def sparse_multiply_rows(csr_mat, vec):
    'Row-wise multiplication of a sparse matrix by a sparse vector'
    csr_vec = spsparse.csr_matrix(vec, copy=False)
    #csr_vec.shape = (1, csr_vec.size)
    sparse_stack = [row.multiply(csr_vec) for row in csr_mat]
    return spsparse.vstack(sparse_stack, format='csr')

def tune_flann(data, **kwargs):
    flann = pyflann.FLANN()
    num_data = len(data)
    flann_atkwargs = dict(algorithm='autotuned',
                                 target_precision=.01,
                                 build_weight=0.01,
                                 memory_weight=0.0,
                                 sample_fraction=0.001)
    flann_atkwargs.update(kwargs)

    suffix = repr(flann_atkwargs)
    badchar_list = ',{}\': '
    for badchar in badchar_list:
        suffix = suffix.replace(badchar, '')

    print flann_atkwargs

    tuned_params = flann.build_index(data, **flann_atkwargs)

    helpers.myprint(tuned_params)

    out_file = 'flann_tuned'+suffix
    helpers.write_to(out_file, repr(tunned_params))
    flann.delete_index()
    return tuned_params

def __tune():
    tune_flann(sample_fraction=.03, target_precision=.9, build_weight=.01)
    tune_flann(sample_fraction=.03, target_precision=.8, build_weight=.5)
    tune_flann(sample_fraction=.03, target_precision=.8, build_weight=.9)
    tune_flann(sample_fraction=.03, target_precision=.98, build_weight=.5)
    tune_flann(sample_fraction=.03, target_precision=.95, build_weight=.01)
    tune_flann(sample_fraction=.03, target_precision=.98, build_weight=.9)

    tune_flann(sample_fraction=.3, target_precision=.9, build_weight=.01)
    tune_flann(sample_fraction=.3, target_precision=.8, build_weight=.5)
    tune_flann(sample_fraction=.3, target_precision=.8, build_weight=.9)
    tune_flann(sample_fraction=.3, target_precision=.98, build_weight=.5)
    tune_flann(sample_fraction=.3, target_precision=.95, build_weight=.01)
    tune_flann(sample_fraction=.3, target_precision=.98, build_weight=.9)

    tune_flann(sample_fraction=1, target_precision=.9, build_weight=.01)
    tune_flann(sample_fraction=1, target_precision=.8, build_weight=.5)
    tune_flann(sample_fraction=1, target_precision=.8, build_weight=.9)
    tune_flann(sample_fraction=1, target_precision=.98, build_weight=.5)
    tune_flann(sample_fraction=1, target_precision=.95, build_weight=.01)
    tune_flann(sample_fraction=1, target_precision=.98, build_weight=.9)

# Look at /flann/algorithms/dist.h for distance clases

#distance_translation = {"euclidean"        : 1, 
                        #"manhattan"        : 2, 
                        #"minkowski"        : 3,
                        #"max_dist"         : 4,
                        #"hik"              : 5,
                        #"hellinger"        : 6,
                        #"chi_square"       : 7,
                        #"cs"               : 7,
                        #"kullback_leibler" : 8,
                        #"kl"               : 8,
                        #"hamming"          : 9,
                        #"hamming_lut"      : 10,
                        #"hamming_popcnt"   : 11,
                        #"l2_simple"        : 12,}

# MAKE SURE YOU EDIT index.py in pyflann

#flann_algos = {
    #'linear'        : 0,
    #'kdtree'        : 1,
    #'kmeans'        : 2,
    #'composite'     : 3,
    #'kdtree_single' : 4,
    #'hierarchical'  : 5,
    #'lsh'           : 6, # locality sensitive hashing
    #'kdtree_cuda'   : 7, 
    #'saved'         : 254, # dont use
    #'autotuned'     : 255,
#}

#multikey_dists = {
    ## Huristic distances
    #('euclidian', 'l2')        :  1,
    #('manhattan', 'l1')        :  2,
    #('minkowski', 'lp')        :  3, # I guess p is the order?
    #('max_dist' , 'linf')      :  4,
    #('l2_simple')              : 12, # For low dimensional points
    #('hellinger')              :  6,
    ## Nonparametric test statistics
    #('hik','histintersect')    :  5,
    #('chi_square', 'cs')       :  7,
    ## Information-thoery divergences
    #('kullback_leibler', 'kl') :  8,
    #('hamming')                :  9, # xor and bitwise sum
    #('hamming_lut')            : 10, # xor (sums with lookup table ; if no sse2)
    #('hamming_popcnt')         : 11, # population count (number of 1 bits)
#}


 #Hamming distance functor - counts the bit differences between two strings - useful for the Brief descriptor
 #bit count of A exclusive XOR'ed with B

#flann_distances = {"euclidean"        : 1, 
                   #"manhattan"        : 2, 
                   #"minkowski"        : 3,
                   #"max_dist"         : 4,
                   #"hik"              : 5,
                   #"hellinger"        : 6,
                   #"chi_square"       : 7,
                   #"cs"               : 7,
                   #"kullback_leibler" : 8,
                   #"kl"               : 8 }

#pyflann.set_distance_type('hellinger', order=0)

def ann_flann_once(dpts, qpts, num_neighbors, flann_params):
    flann = pyflann.FLANN()
    flann.build_index(dpts, **flann_params) 
    checks = flann_params['checks']
    (qx2_dx, qx2_dist) = flann.nn_index(qpts, num_neighbors, checks=checks)
    return (qx2_dx, qx2_dist)

#@profile
def __akmeans_iterate(data,
                      clusters,
                      datax2_clusterx_old,
                      max_iters,
                      flann_params,
                      ave_unchanged_thresh,
                      ave_unchanged_iterwin):
    num_data = data.shape[0]
    num_clusters = clusters.shape[0]
    # Keep track of how many points have changed in each iteration
    xx2_unchanged = np.zeros(ave_unchanged_iterwin, dtype=np.int32) + len(data)
    print('[algos] Starting iterations:')
    print('[algos] Printing akmeans info in format: time (iterx, ave(#changed), #unchanged)')
    for xx in xrange(0, max_iters): 
        # 1) Find each datapoints nearest cluster center
        tt = helpers.tic()
        helpers.print_('...tic')
        helpers.flush()
        (datax2_clusterx, _dist) = ann_flann_once(clusters, data, 1, flann_params)
        ellapsed = helpers.toc(tt)
        helpers.print_('...toc(%.2fs)' % ellapsed)
        helpers.flush()
        # 2) Find new cluster datapoints
        datax_sort    = datax2_clusterx.argsort()
        clusterx_sort = datax2_clusterx[datax_sort]
        _L = 0   
        clusterx2_dataLRx = [None for _ in xrange(num_clusters)]
        for _R in xrange(len(datax_sort)+1): # Slide R
            if _R == num_data or clusterx_sort[_L] != clusterx_sort[_R]:
                clusterx2_dataLRx[clusterx_sort[_L]] = (_L, _R)
                _L = _R
        # 3) Compute new cluster centers
        helpers.print_('+')
        helpers.flush()
        for clusterx, dataLRx in enumerate(clusterx2_dataLRx):
            if dataLRx is None: continue # ON EMPTY CLUSTER
            (_L, _R) = dataLRx
            clusters[clusterx] = np.mean(data[datax_sort[_L:_R]], axis=0)
            #if params.__BOW_DTYPE__ == np.uint8:
            #clusters[clusterx] = np.array(np.round(clusters[clusterx]), dtype=params.__BOW_DTYPE__)
            clusters[clusterx] = np.array(np.round(clusters[clusterx]), dtype=np.uint8)
        # 4) Check for convergence (no change of cluster id)
        helpers.print_('+')
        helpers.flush()
        num_changed = (datax2_clusterx_old != datax2_clusterx).sum()
        xx2_unchanged[xx % ave_unchanged_iterwin] = num_changed
        ave_unchanged = xx2_unchanged.mean()
        #(iterx, ave(#changed), #unchanged)
        helpers.print_('  (%d, %.2f, %d)\n' % (xx, ave_unchanged, num_changed))
        helpers.flush()
        if ave_unchanged < ave_unchanged_thresh:
            break
        else: # Iterate
            datax2_clusterx_old = datax2_clusterx
            if xx % 5 == 0: 
                sys.stdout.flush()
    print('[algos]  * AKMEANS: converged in %d/%d iters' % (xx+1, max_iters))
    sys.stdout.flush()
    return (datax2_clusterx, clusters)

#@profile
def akmeans(data, num_clusters, max_iters=5, flann_params=None,
            ave_unchanged_thresh=0,
            ave_unchanged_iterwin=10):
    '''Approximiate K-Means (using FLANN)
    Input: data - np.array with rows of data.
    Description: Quickly partitions data into K=num_clusters clusters.
    Cluter centers are randomly assigned to datapoints. 
    Each datapoint is assigned to its approximate nearest cluster center. 
    The cluster centers are recomputed. 
    Repeat until convergence.'''
    print('[algos] Running akmeans: data.shape=%r ; num_clusters=%r' % (data.shape, num_clusters))
    print('[algos] * max_iters = %r ' % max_iters)
    #print('  * dtype = %r ' % params.__BOW_DTYPE__)
    print('[algos] * ave_unchanged_iterwin=%r ; ave_unchanged_thresh=%r' % \
          (ave_unchanged_thresh, ave_unchanged_iterwin))
    # Setup iterations
    #data   = np.array(data, params.__BOW_DTYPE__) 
    num_data = data.shape[0]
    # Initialize to random cluster clusters
    datax_rand = np.arange(0,num_data);
    np.random.shuffle(datax_rand)
    clusterx2_datax     = datax_rand[0:num_clusters] 
    clusters            = np.copy(data[clusterx2_datax])
    datax2_clusterx_old = -np.ones(len(data), dtype=np.int32)
    # This function does the work
    (datax2_clusterx, clusters) = __akmeans_iterate(data,
                                                    clusters,
                                                    datax2_clusterx_old,
                                                    max_iters,
                                                    flann_params,
                                                    ave_unchanged_thresh,
                                                    ave_unchanged_iterwin)
    return (datax2_clusterx, clusters)

def whiten(data):
    'wrapper around sklearn'
    pca = sklearn.decomposition.PCA(copy=True, n_components=None, whiten=True)
    pca.fit(data)
    data_out = pca.transform(data)
    return data_out
def norm_zero_one(data):
    return (data - data.min()) / (data.max() - data.min())
def scale_to_byte(data):
    return np.array(np.round(norm_zero_one(data) * 255), dtype=np.uint8)

def plot_clusters(data, datax2_clusterx, clusters):
    # http://www.janeriksolem.net/2012/03/isomap-with-scikit-learn.html
    print('[algos] Doing PCA')
    num_pca_dims = min(3, data.shape[1])
    pca = sklearn.decomposition.PCA(copy=True, n_components=num_pca_dims, whiten=False).fit(data)
    pca_data = pca.transform(data)
    pca_clusters = pca.transform(clusters)
    print('[algos] ...Finished PCA')

    fig = plt.figure(1)
    fig.clf()
    cmap = plt.get_cmap('hsv')
    data_x = pca_data[:,0]
    data_y = pca_data[:,1]
    data_colors = datax2_clusterx
    clus_x = pca_clusters[:,0]
    clus_y = pca_clusters[:,1]
    clus_colors = np.arange(0,len(clusters))
    if num_pca_dims == 2:
        plt.scatter(data_x, data_y, s=20,  c=data_colors, marker='o')
        plt.scatter(clus_x, clus_y, s=500, c=clus_colors, marker='*')
    if num_pca_dims == 3:
        from mpl_toolkits.mplot3d import Axes3D
        ax = fig.add_subplot(111, projection='3d')
        data_z = pca_data[:,1]
        clus_z = pca_clusters[:,1]
        ax.scatter(data_x, data_y, data_z, s=20,  c=data_colors, marker='o')
        ax.scatter(clus_x, clus_y, clus_z, s=500, c=clus_colors, marker='*')
    return fig

import textwrap
def force_quit_akmeans(signal, frame):
    try: 
        print(textwrap.dedent('''
        --- algos ---
        Caught Ctrl+C in:
            function: %r
            stacksize: %r
            line_no: %r
                            ''') % \
            (frame.f_code.co_name, 
            frame.f_code.co_stacksize,
            frame.f_lineno))
        exec(df2.present()) 
        target_frame = frame
        target_frame_coname = '__akmeans_iterate'
        while True:
            if target_frame.f_code.co_name == target_frame_coname:
                break
            if target_frame.f_code.co_name == '<module>':
                print('Traced back to module level. Missed frame: '+target_frame_coname)
                break
            target_frame = target_frame.f_back
            print 'Is target frame?: '+target_frame.f_code.co_name

        fpath = target_frame.f_back.f_back.f_locals['fpath']

        data            = target_frame.f_locals['data']
        clusters        = target_frame.f_locals['clusters']
        datax2_clusterx = target_frame.f_locals['datax2_clusterx']
        helpers.save_npz(fpath+'.earlystop', datax2_clusterx, clusters)
    except Exception as ex: 
        print(repr(ex))
        exec(helpers.IPYTHON_EMBED_STR)

def precompute_akmeans(data, num_clusters, max_iters=100,
                       flann_params=None,  cache_dir=None,
                       force_recomp=False, same_data=True, uid=''):
    'precompute aproximate kmeans'
    print('[algos] precompute_akmeans(): enter')
    if same_data:
        data_hash = helpers.hashstr(data,)
        data_shape = str(data.shape).replace(' ','')
        data_uid = 'dID('+data_shape+data_hash+')'
        uid += data_uid
    clusters_fname = 'akmeans_clusters'
    datax2cl_fname = 'akmeans_datax2cl'
    try:
        clusters        = io.smart_load(cache_dir, clusters_fname, uid, '.npy')
        datax2_clusterx = io.smart_load(cache_dir, datax2cl_fname, uid, '.npy')
        print('[algos] precompute_akmeans(): ... loaded akmeans.')
    except Exception as ex:
        print('[algos] precompute_akmeans(): ... could not load akmeans.')
        errstr = helpers.indent(repr(ex), '[algos]    ')
        print('[algos] precompute_akmeans(): ... caught ex:\n %s ' % errstr)
        print('[algos] precompute_akmeans(): printing debug_smart_load')
        io.debug_smart_load(cache_dir, clusters_fname)
        io.debug_smart_load(cache_dir, datax2cl_fname)
        #print('[algos] Press Ctrl+C to stop k-means early (and save)')
        #signal.signal(signal.SIGINT, force_quit_akmeans) # set ctrl+c behavior
        print('[algos] computing:')
        print('[algos] '+'_'.join([clusters_fname, uid])+'.npy')
        print('[algos] '+'_'.join([datax2cl_fname, uid])+'.npy')
        print('[algos] precompute_akmeans(): calling akmeans')
        (datax2_clusterx, clusters) = akmeans(data, num_clusters, max_iters, flann_params)
        print('[algos] precompute_akmeans(): finished running akmeans')
        io.smart_save(clusters,        cache_dir, clusters_fname, uid, '.npy')
        io.smart_save(datax2_clusterx, cache_dir, datax2cl_fname, uid, '.npy')
        #print('[algos] Removing Ctrl+C signal handler')
        #signal.signal(signal.SIGINT, signal.SIG_DFL) # reset ctrl+c behavior
    print('[algos] precompute_akmeans(): return')
    return (datax2_clusterx, clusters)

def precompute_flann(data, cache_dir=None, uid='', flann_params=None):
    ''' Tries to load a cached flann index before doing anything'''
    print('[algos] precompute_flann(%r): ' % uid)
    cache_dir = '.' if cache_dir is None else cache_dir
    # Generate a unique filename for data and flann parameters
    fparams_uid = helpers.remove_chars(str(flann_params.values()), ', \'[]')
    data_hash    = helpers.hashstr(data) # flann is dependent on the data
    data_shape   = helpers.remove_chars(str(data.shape), ' ')
    flann_suffix = '_' + fparams_uid + '_dID(' + data_shape + data_hash + ').flann'
    # Append any user labels
    flann_fname = 'flann_index' + flann_suffix + uid 
    flann_fpath = os.path.normpath(join(cache_dir, flann_fname))
    # Load the index if it exists
    flann = pyflann.FLANN()
    load_success = False
    if helpers.checkpath(flann_fpath):
        try:
            print('[algos] precompute_flann(): trying to load: %r ' % flann_fname)
            flann.load_index(flann_fpath, data)
            print('[algos]...success')
            load_success = True
        except Exception as ex:
            print('[algos] precompute_flann(): ...cannot load index')
            print('[algos] precompute_flann(): ...caught ex=\n%r' % (ex,))
    if not load_success:
        # Rebuild the index otherwise
        with helpers.Timer(msg='build FLANN', newline=False):
            flann.build_index(data, **flann_params)
        print('[algos] precompute_flann(): save_index(%r)' % flann_fname)
        flann.save_index(flann_fpath)
    return flann

if __name__ == '__main__':

    np.random.seed(seed=0) # RANDOM SEED (for reproducibility)
    num_clusters = 10

    __REAL_DATA_MODE__ = True
    if __REAL_DATA_MODE__:
        exec(open('feature_compute2.py').read())
        cx2_desc = hs_feats.cx2_desc
        data = np.vstack(cx2_desc)
        #datax2_clusterx, clusters = xxprecompute_akmeans(data, num_clusters, force_recomp=True)
    else:
        data = np.random.rand(1000, 3)
        #datax2_clusterx, clusters = akmeans(data, num_clusters)


    fig = plot_clusters(data, datax2_clusterx, clusters)
    fig.show()

    try: 
        __IPYTHON__
    except: 
        plt.show()


#IDEA: 
    #intead have each datapoint "pull" on one another. Maybe warp the space
    #in which they sit with a covariance matrix.  basically let gravity do
    #the clustering.  Check to see if any algos like this. 

    #itertools.groupby
    #groups
