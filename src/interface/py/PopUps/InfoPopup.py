"""" Popup to information."""

from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import webbrowser


class InfoPopup(Popup):
    """Information popup class."""
    msg1 = StringProperty('')
    msg2 = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize popup."""
        super(InfoPopup, self).__init__(**kwargs)
        self.msg1 = 'A desktop application for researchers to measure ' \
                    'and analyze solar cells.'
        self.msg2 = 'Created by: Franciss and Laura.'

    @staticmethod
    def open_repository():
        """Open the repository website."""
        web = 'https://github.com/Franlorlaz/solar_cell_analyzer'
        webbrowser.open(web)
