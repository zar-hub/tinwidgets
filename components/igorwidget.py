import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Layout, Button, Box, FloatSlider, Label, Dropdown, HTML
from matplotlib.lines import Line2D
import tinwidgets as tw

# __ Layouts __
container_layout = Layout(
    display='flex',
    flex_flow='column',
    align_items='center',
    align_content='flex-start',
    border='solid',
    padding='0px',
    margin='0px',
    width='100%'
)

items_layout = Layout(
    width='100%',
    margin='0px',
) 


class FitPanelWidget():
    def __init__(self, options : list = [''], title : str = 'Rect id:'):
        self.dropdown = Dropdown(
            options=options,
            description='Choose:',
            layout=Layout(width='90%')
        )

        self.wave = None
        self.fit_button = Button(description='Fit', layout=Layout(width='90%'))
        self.title = HTML(value=f'<h3 style="margin:0;padding:0;">{title}</h3>', layout=Layout(width='90%'))
        self.words = ['left', 'top', 'width', 'height']
        self.items = [FloatSlider(description=word, layout=items_layout) for word in self.words]
        self.items = [self.title, self.dropdown] + self.items
        self.items.append(self.fit_button)
        self.container = Box(children=self.items, layout=container_layout)
        
    def show(self):
        display(self.container)

class WavePanel():
    def __init__(self, title : str = 'Wave id'):
        self.reset_button = Button(description='Reset', layout=Layout(width='90%'))
        self.title = HTML(value=f'<h3 style="margin:0;padding:0;">{title}</h3>', layout=Layout(width='90%'))
        self.words = ['x-offset', 'y-offset', 'x-scale', 'y-scale']
        self.items = [FloatSlider(description=word, layout=items_layout, min = 0, max = 10) for word in self.words]
        self.items = [self.title] + self.items
        self.items.append(self.reset_button)
        self.container = Box(children=self.items, layout=container_layout)
    
    def link(self, wave : Line2D):
        self.wave = wave
        tw.link_property(self.items[1], wave.getTra, 'xdata')
        tw.link_property(self.items[2], wave, 'ydata')
        
    def show(self):
        display(self.container)
