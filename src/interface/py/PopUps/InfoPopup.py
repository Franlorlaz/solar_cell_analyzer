"""" Popup to info"""

from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import webbrowser


class InfoPopup(Popup):
    msg1 = StringProperty('')
    msg2 = StringProperty('')

    def __init__(self, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.msg1 = 'A desktop application for researchers to measure and analyze solar cells.'
        self.msg2 = 'Created by: Franciss and Laura.'

    def open_repository(self):
        web = 'https://github.com/Franlorlaz/solar_cell_analyzer'
        webbrowser.open(web)