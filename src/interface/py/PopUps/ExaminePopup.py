"""" Popup to examine the save path"""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class ExaminePopup(Popup):
    id_examinepopup = ObjectProperty(None)
