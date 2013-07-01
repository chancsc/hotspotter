'''
This is less of a helper function file and more of a pile of things 
where I wasn't sure of where to put. 
A lot of things could probably be consolidated or removed. There are many
non-independent functions which are part of HotSpotter. They should be removed
and put into their own module. The standalone functions should be compiled 
into a global set of helper functions.

Wow, pylint is nice for cleaning.
'''

import cPickle
import code
import numpy as np
import os, os.path, sys
import sys
import time
import types

def join_mkdir(*args):
    'os.path.join and creates if not exists'
    output_dir = os.path.join(*args)
    if not os.path.exists(output_dir):
        print('Making dir: '+output_dir)
        os.mkdir(output_dir)
    return output_dir

def vd(dname=None):
    'View directory'
    if dname is None: 
        dname = os.getcwd()
    os_type       = sys.platform
    open_prog_map = {'win32':'explorer.exe', 'linux2':'nautilus', 'darwin':'open'}
    open_prog     = open_prog_map[os_type]
    os.system(open_prog+' '+dname)
        
def str2(obj):
    if type(obj) == types.DictType:
        return str(obj).replace(', ','\n')[1:-1]
    if type(obj) == types.TypeType:
        return str(obj).replace('<type \'','').replace('\'>','')
    else:
        return str(obj)
#---------------
'''
def __getstate__(self):
    out_dict = self.__dict__.copy()
    return odict
def __setstate__(self, in_dict):
    self.__dict__.update(in_dict)
'''
#---------------
def sanatize_fname(fname):
    ext = '.pkl'
    if fname.rfind(ext) != max(len(fname) - len(ext), 0):
        fname += ext
    return fname
def save(obj, fname):
    'A simple save function using cPickle'
    with open(sanatize_fname(fname), 'wb') as file:
        cPickle.dump(obj, file)
def load(fname):
    'A simple load function using cPickle'
    with open(sanatize_fname(fname), 'wb') as file:
        return cPickle.load(file)
#---------------
def filecheck(fpath):
    return os.path.exists(fpath)
#----------------
def dircheck(dpath,makedir=True):
    if not os.path.exists(dpath):
        if not makedir:
            #print('Nonexistant directory: %r ' % dpath)
            return False
        print('Making directory: %r' % dpath)
        os.makedirs(dpath)
    return True

def in_IPython():
    try:
        __IPYTHON__
        return True
    except NameError as nex:
        return False

def have_IPython():
    try:
        import IPython
        return True
    except NameError as nex:
        return False

def keyboard(banner=None):
    ''' Function that mimics the matlab keyboard command '''
    # use exception trick to pick up the current frame
    try:
        raise None
    except:
        frame = sys.exc_info()[2].tb_frame.f_back
    print "# Ctrl-D  Use quit() to exit :) Happy debugging!"
    # evaluate commands in current namespace
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)
    try:
        code.interact(banner=banner, local=namespace)
        #import IPython
        #IPython.embed_kernel(module=None,local_ns=namespace)
    except SystemExit:
        return

def alloc_lists(num_alloc):
    'allocates space for a numpy array of lists'
    return [[] for _ in xrange(num_alloc)]

class Timer(object):
    ''' Used to time statments with a with statment
    e.g with Timer() as t: some_function()'''
    def __init__(self, outlist=[]):
        # outlist is a list to append output to
        self.outlist   = outlist
        self.tstart = -1

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, trace):
        tend = time.time()
        ellapsed = (tend - self.tstart)
        self.outlist.append(ellapsed)
        print 'Elapsed: %s seconds' % ellapsed