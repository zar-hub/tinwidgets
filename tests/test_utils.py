import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.lines import Line2D
import ipywidgets as widgets
import numpy as np
from IPython import get_ipython
import sys

def prepare_env(reload_all=True):
    '''
    Resets the test cell,
        - prepares the backend
        - autoreload modules for testing 
        - closes all figures
        - adds the path to all the folders
    '''

    # Only run this once per kernel session
    if prepare_env.active:
        return
    
    ipython = get_ipython()
    ipython.magic('matplotlib widget')
    if reload_all:
        ipython.magic('load_ext autoreload')
        ipython.magic('autoreload 2')
    plt.close('all')
    sys.path.append('..')
    sys.path.append('..\\components')
    prepare_env.active = True

def reset_cell():
    '''
    Resets the test cell,
        - closes all figures
        - clears the output
    '''
    plt.close('all')
    ipython = get_ipython()
    ipython.magic('clear')

# set the state
prepare_env.active = False