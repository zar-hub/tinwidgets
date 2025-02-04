import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.lines import Line2D
import ipywidgets as widgets
import numpy as np
from IPython import get_ipython

def prepare_env():
    '''
    Resets the test cell,
        - prepares the backend
        - autoreload modules for testing 
        - closes all figures
    '''
    ipython = get_ipython()
    ipython.magic('matplotlib widget')
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 2')
    plt.close('all')