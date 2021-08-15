"""" Popup to print measures"""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class ErrorWarningPopup(Popup):
    id_error_warning_popup = ObjectProperty(None)

    def print_error_msg(self,msg):
        self.ids.error_msg.text = msg

