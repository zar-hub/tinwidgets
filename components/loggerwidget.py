import ipywidgets as widgets
import logging
from IPython.display import display

class OutputWidgetHandler(logging.Handler):
    """ Custom logging handler sending logs to an output widget """

    def __init__(self, *args, **kwargs):
        super(OutputWidgetHandler, self).__init__(*args, **kwargs)
        layout = {
            'width': '100%', 
            'height': '160px', 
            'border': '1px solid black'
        }
        self.out = widgets.Output(layout=layout)

    def emit(self, record):
        """ Overload of logging.Handler method """
        formatted_record = self.format(record)
        new_output = {
            'name': 'stdout', 
            'output_type': 'stream', 
            'text': formatted_record+'\n'
        }
        self.out.outputs = (new_output, ) + self.out.outputs
        
    def show_logs(self):
        """ Show the logs """
        display(self.out)
    
    def clear_logs(self):
        """ Clear the current logs """
        self.out.clear_output()