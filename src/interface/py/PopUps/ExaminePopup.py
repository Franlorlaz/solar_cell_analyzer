"""" Popup to examine the save path"""

from pathlib import Path
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class ExaminePopup(Popup):
    id_examinepopup = ObjectProperty(None)
    save_init_path = StringProperty('')

    def __init__(self, **kwargs):
        super(ExaminePopup, self).__init__(**kwargs)
        self.save_init_path = str(Path(__file__ + '/../../../../measures').resolve())