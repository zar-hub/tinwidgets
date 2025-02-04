import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib import transforms

def update_Rectangle(rect : Rectangle, *args):
    ''' 
    Updates the position of a dragged Rectangle artist.
    THIS IS A HARD CHANGE: the rectangle is intended to be used as a
    "selector", so its actually moved during an update and not only
    "shown" displaced at drawtime.
    '''
    dx, dy, modifiers = args
    
    # modifiers can change the bahaviour from
    # a translation to a scale
    if 'ctrl' in modifiers:
        width, height = rect.get_width(), rect.get_height()
        width += dx
        height += dy
        rect.set_width(width)
        rect.set_height(height)
    else:
        xy = np.array(rect.get_xy())
        xy = xy + [dx, dy]
        rect.set_xy(xy)

def update_Line2D(line : Line2D, *args):
    ''' 
    Updates the position of a dragged Line2D artist.
    THIS IS A SOFT CHANGE: THE ACTUAL POINTS ARE NOT 
    TOUCHED, THE ARTIST IS TRANSLATED ONLY AT DRAW TIME!
    This is important because one might not want to actually
    change the experimental wavedata (Igor like behaviuour) when dragging
    things around...
    '''
    dx, dy, modifiers = args
    
    if 'ctrl' in modifiers:
        line.set_transform(transforms.Affine2D().scale(1 + dx, 1 + dy) + line.get_transform())
    else:
        # WARNING: Transform.__add__ is NOT commutative!
        # this means that .translate + .get_transform is not the 
        # same as .get_transform + .translate
        # Compute the current scale factors from the transformation
        # Extract the current transformation matrix
        line.set_transform(transforms.Affine2D().translate(dx, dy) + line.get_transform())
