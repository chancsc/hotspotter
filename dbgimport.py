from __future__ import division, print_function
# Python
from collections import OrderedDict
from os.path import dirname, realpath, join, exists, normpath
import imp
import itertools
import itertools  # NOQA
import multiprocessing
import os
import re
import sys
import sys
import textwrap
import textwrap  # NOQA
# Scientific
import numpy as np  # NOQA
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
# Qt
import PyQt4
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import (QAbstractItemModel, QModelIndex, QVariant, QWidget,
                      Qt, QObject, pyqtSlot, QKeyEvent)
# HotSpotter
import DataStructures as ds
import HotSpotter
import Parallelize as parallel
import algos
import chip_compute2 as cc2
import dev
import draw_func2 as df2
import extract_patch
import feature_compute2 as fc2
import fileio as io
import helpers as helpers
import load_data2 as ld2
import match_chips3 as mc3
import matching_functions as mf
import segmentation
import vizualizations as viz
import voting_rules2 as vr2

if __name__ == 'main':
    multiprocessing.freeze_support()
    #exec(open('dbgimport.py').read())
    if '--img' in sys.argv:
        img_fpath_ = helpers.dbg_get_imgfpath()
        np_img_ = io.imread(img_fpath_)
        img_ = Image.open(img_fpath_)
