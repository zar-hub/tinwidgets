"""
This module demonstrates user interactions with multiple artists (rectangles and lines) on a Matplotlib canvas.
It allows picking, moving, and releasing artists with specific event handlers.
Functions:
    update_bg(): Updates the background of the canvas.
    on_pick(event): Handles the pick event when an artist is selected.
    on_move(event): Handles the motion notify event when the mouse moves.
    on_release(event): Handles the button release event when the mouse button is released.
    on_draw(event): Handles the draw event when the figure is redrawn.
    on_value_change(change): Updates the frame skip value based on widget input.
    on_check(change): Updates the frame skipping mode based on widget input.
Widgets:
    int_range: A slider widget to control the frame skip value.
    check: A toggle button widget to control the frame skipping mode.
    out: An output widget to display messages and information.
"""
__version__ = '0.1.0'

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
import numpy as np
import update_handlers as upd_hand
import logging.handlers
import logging
from components.loggerwidget import OutputWidgetHandler
import ipywidgets as widgets
from matplotlib.transforms import Affine2D

# ___ MODULE STATE ___
bg, fig, ax = None, None, None

def subplots(*args, **kwargs):
    # Turn off interactive mode to avoid 
    # conflicts with the %matplotlib widget
    # backend.
    with plt.ioff():
        fig, ax = plt.subplots(*args, **kwargs)
        
    # Connect the event handlers to the figure
    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('motion_notify_event', on_move)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('draw_event', on_draw)
    logger.info('Figure %s has been created', id(fig))
    return fig, ax

# ___ EVENT HANDLERS ___
def update_bg():
    global bg, fig, ax 
    try:
        fig.canvas.draw()
        bg = fig.canvas.copy_from_bbox(ax.bbox)
    except Exception as e:
        logger.error(e)
        raise RuntimeError

def on_pick(event):
    art : Artist = event.artist
    # If an artist is already picked 
    # just drop out
    if not on_pick.current is None:
        return
    
    # Set the current artist to the picked one
    # and set the figure and axis to the artist's
    global bg, fig, ax
    on_pick.current = art
    fig = art.get_figure()
    ax = art.axes
    logger.debug('Picked artist %s id: %s', type(art), id(art))
    logger.debug('fig: %s, ax: %s', id(fig), id(ax))
    
    # The animated artist are excluded from the 
    # normal drawing pipeline and must be drawn manually.
    # This is used in conjunction with the blit method
    # to have responsive drawing.
    art.set_animated(True)
    
    try:
        # This saves the state of the artist properties in the 
        # on_release.style dict.
        # At first all the properties are getted because there is not
        # a method to get a single prop like there is for setting 
        # a single prop as in art.set(alpha = someval).
        # Then only the ones changed during pick are actually saved in
        # on_release.style
        props = art.properties()
        on_release.style = {
            key : props[key] for key in on_pick.styles[type(art)].keys()
        }
        # on_pick.styles[type(art)] is a dict with
        # all the styles changes needed when the artist
        # is picked.
        # The ** operator unpacks the dict.
        # To be safe that the dict keys are correct
        # we access the dict using the [] operator
        # and not the .get() method. This throws a 
        # KeyError if the key is not found.
        art.set(**on_pick.styles[type(art)])
    except KeyError as e:
       logger.error('Style for %s is not supported', e)
   
    update_bg()
    ax.draw_artist(art)
    fig.canvas.blit(ax.bbox)

def on_move(event): 
    global bg, fig, ax
    # ___ FRAME SKIPPING LOGIC ____
    if on_move.skip_frames < 0:
        on_move.skip_frames = 0
    try:
        if on_move.frame_skip == 'normal':
            if on_move.skip_frames:
                on_move.skip_frames -= 1
                return
            on_move.skip_frames = SKIP_FRAMES
            
        elif on_move.frame_skip == 'inverted':
            if not on_move.skip_frames:
                on_move.skip_frames = SKIP_FRAMES
                return
            on_move.skip_frames -= 1
        else:
            logger.error('The selected frame skip mode not supported')
            raise RuntimeError
    except:
        raise RuntimeError
    
    # ___ LOGIC ___
    
    # Fetch relevant data and update state,
    # THIS MUST BE DONE EVEN IF NO ARTIST IS SELECTED
    # TO KEEP THE MOUSE POSITION UPDATED!
    # When there is a click on the canvas the previous 
    # position of the mouse must be known to move the object
    # the first time. 
    # A possible optimization is to update on_move.last 
    # the first time when the object is picked, but this 
    # adds unwanted complexity to the logic.
    # Functions should have minimum scope and responsability.
    # Its not good that on_pick should care about movement...
    # on_move should!
    x, y = event.xdata, event.ydata
    px, py = on_move.last
    on_move.last = (x, y)
    modifiers = event.modifiers
    
    # If no artist is picked why bother updating
    if on_pick.current is None:
        return
    # The class is explicitly stated
    # to get autocomplete.
    art : Artist = on_pick.current
    
    # Paranoia: if the artist is not animated
    # something when orribly wrong.
    # Spoiler: it has happened before.
    if not art.get_animated():
        raise RuntimeError("The artist is not animated")
    
    # Exit any of the variables is None,
    # this can occur if mouse is out of 
    # the axis.
    if not (x and y and px and py):
        return

    dx = x - px
    dy = y - py
    
    # This is a little bit Hacky: depending on the type
    # of the artists get the appropriate update_artist
    # function and pass to it the data that it needs
    # to move the artist depending on dx dy and modifiers.
    on_move.behaviours.get(type(art))(art, dx, dy, modifiers)
    
    # Just to be safe check if the background is present
    if bg is None:
        bg = fig.canvas.copy_from_bbox(ax.bbox) 
        logger.error('Background is None but it should not be')  
    fig.canvas.restore_region(bg)
    ax.draw_artist(art)
    fig.canvas.blit(ax.bbox)

def on_release(event):
    global bg, fig, ax 
    if on_pick.current is None:
        return
    
    # Reset picked artist state
    art : Artist = on_pick.current
    art.set_animated(False)
    # Get the styles that on_pick.styles changed 
    # and restore each of them using the old
    # values in on_release.style
    try:
        art.set(**on_release.style)
    except RuntimeError as e:
        logger.error(e)
    
    ax.draw_artist(art)
    update_bg()
    # fig.canvas.draw_idle()  # Trigger a full redraw to finalize changes
    
    # RESETTING MUST BE DONE LAST
    # Setting art = on_pick.current was done
    # for convenience but now its a reference
    # to on_pick.current.
    # Setting current to None also sets art to None 
    # and this is the last thing that should be done.
    on_pick.current = None
    on_release.style = {}
    
    # Update the widget linked to the artist
    # if there is one.
    if id(art) in widget_handlers:
        logger.debug('Updating widgets linked to artist %s', id(art))
        for widget_handler in widget_handlers[id(art)]:
            widget_handler()
    
    
    logger.debug('Released artist %s id:%s', type(art), id(art))
    
def on_draw(event):
    # When there is a redraw clear the previuos bg.
    # A redraw is a full redraw of the figure, not just a 
    # blit of the canvas. It is triggered by fig.canvas.draw_idle()
    # and fig.canvas.draw() and must be called explicitly
    # when NOT in interactive mode.
    global bg 
    bg = None
    
# __ HELPER FUNCTIONS __
def attach_handler(artist : Artist, widget_handler : callable):
    ''' 
    Adds a widget handler to the artist using id as key.
    To keep things simple a function is created with all the
    necessary info to update the widget, so only a list 
    of functions (handlers) is needed to update all the widgets 
    linked to an artist id.
    Handlers are called when artist is released
    '''
    # Create a list of handlers if it does not exist
    if widget_handlers.get(id(artist)) is None:
        widget_handlers[id(artist)] = []  

    widget_handlers[id(artist)].append(widget_handler)

def link_property(widget : widgets.Widget, artist : Artist, prop : str):
    ''' 
    Attaches a widget to a property of an artist.
    The widget is updated when the property is changed.
    '''
    try :
        artist.properties()[prop]
    except KeyError as e:
        msg = 'Property {} is not supported for {}'.format(e, type(artist))
        logger.error(msg)
        raise KeyError(msg)
    
    # Widget change --> artist change
    def update_art(change):
        new_val = change['new']
        artist.set(**{prop : new_val})
        
    widget.observe(lambda change : update_art(change), names = 'value')

    # artist change --> widget change
    def update_widget():
        logger.debug('Updating prop widget %s', id(widget))
        widget.value = artist.properties()[prop]

    attach_handler(artist, update_widget)
    update_widget()

def link_transform(widget : widgets.Widget, artist : Artist, transform : str):
    ''' 
    Attaches a widget to a transformation of an artist.
    The widget is updated when the transformation is changed.
    Transform is a 3x3 mask of the transformation.

    Properties:
        sx : x scaling
        sy : y scaling
        tx : x translation
        ty : y translation
    '''

    # Transformations mask
    masks = {
        'sx' : (0,0),
        'sy' : (1,1),
        'tx' : (0,2),
        'ty' : (1,2),
    }

    if not transform in masks:
        raise KeyError('Transform {} is not supported'.format(transform))

    # Widget change --> artist change
    def update_art(change):
        new_val = change['new']
        trans = artist.axes.transData
        inv = trans.inverted()
        matrix = inv.get_matrix() @ artist.get_transform().get_matrix()
        matrix[masks[transform]] = new_val
        matrix = trans.get_matrix() @ matrix
        artist.set_transform(Affine2D(matrix))

    widget.observe(lambda change : update_art(change), names = 'value')
    # artist change --> widget change
    def update_widget():
        logger.debug('Updating transform widget %s', id(widget))
        inv = artist.axes.transData.inverted()
        matrix = inv.get_matrix() @ artist.get_transform().get_matrix()
        widget.value = matrix[masks[transform]]

    attach_handler(artist, update_widget)
    update_widget()
    
def attach_output(artist : Artist, widget : widgets.Output):
    ''' 
    Displays the Artist properties in a widget.
    The diplay properties are listed 
    in the display_output.styles dict.
    '''
    try:
        display_props = attach_output.styles[type(artist)]
    except KeyError as e:
        msg = 'Display properties for {} are not supported'.format(e)
        logger.error(msg)
        raise KeyError(msg)
    
    def handle_output():
        logger.debug('Updating out widget %s', id(widget))
        for prop, propname in display_props.items():
            widget.append_stdout('{} : {}\n'.format(propname, artist.properties()[prop]))   
    
    attach_handler(artist, handle_output) 
    
    
    
# __ PREPARE ENVIRONMENT __
# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# The widget handler can be displayed
# in the notebook using tinwidgets.widget_handler.show_logs()
widget_handler = OutputWidgetHandler()
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
widget_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(widget_handler)
logger.addHandler(file_handler)

# initialize the static variables
logger.info('Initializing Module') 
# Frameskpping
SKIP_FRAMES = 0
on_move.frame_skip = 'normal'
# Mouse position
on_move.last = (None, None)
on_move.skip_frames = SKIP_FRAMES
# Dragging behaviours
on_move.behaviours = {
    Rectangle : upd_hand.update_Rectangle,
    Line2D : upd_hand.update_Line2D
}
on_pick.styles = {
    Rectangle : {
        'alpha' : 0.6,
        'linewidth' : 1
    },
    Line2D : {
        'linewidth' : 2
        },
}
attach_output.styles = {
    # name propname
    Rectangle : {
        'x' : 'x',
        'y' : 'y',
        'width' : 'width',
        'height' : 'height', 
    }
}
# This is used internally to save the style
# the artist prior to picking
on_pick.current = None
# This should not be setted by the dev, it loads
# the style of the artist when it is picked so 
# it can be restored when it is released.
on_release.style = {}

# Widget state synchandlers
# Each object handled by the library has
# an unique id, and we can use that id
# to display the state of the obj in a widget
widget_handlers = {}


if __name__ == '__main__':
    logger.info('Starting main')
    with plt.ioff():
        fig, ax = plt.subplots()  
        
    x = np.linspace(0,5,30)
    y = np.sin(x)
    rect = Rectangle([0.5, 0.5], 5, 10, alpha=.3,
                    color = 'yellow', lw = 0)
    rect1 = Rectangle([1, 1], 5, 10, alpha=.3,
                    color = 'yellow', lw = 0)
    line = Line2D([0,1], [0,1])
    rect.set_picker(5)
    rect1.set_picker(5)
    line.set_picker(5)

    # adds the line to the axs objects
    # when calling ax.draw() the line 
    # is drawn
    # NOTE: if line.animated is true then 
    # ax.draw() will not draw the line,
    # the updates are handled manually
    ax.add_artist(rect)
    ax.add_artist(rect1)
    ax.add_line(line)
    ax.relim()
    ax.autoscale_view()
    fig.tight_layout()
    fig.set_size_inches(5,3.5)
    fig.canvas.draw()

    bg = fig.canvas.copy_from_bbox(ax.bbox)
    fig.canvas.blit(ax.bbox)