import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
import ipywidgets as widgets
from ipywidgets import Widget
'''
Each handler should have the following signature:
handler_name(artist : Artist, widget : Widget) -> None
'''

def handle_output(artist : Artist, widget : Widget):
    '''
    This handler is intended to be used with the Output widget.
    It will display the artist in the output widget.
    '''
    widget.clear_output(wait=True)
    with widget:
        if type(artist) is Rectangle:
            print(f"Position {artist.get_xy()}, width {artist.get_width()}, height {artist.get_height()}")