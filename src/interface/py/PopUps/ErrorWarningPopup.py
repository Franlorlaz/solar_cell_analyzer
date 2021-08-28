"""" Popup to print error/warning messages."""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class ErrorWarningPopup(Popup):
    """Error and warning popup class."""
    id_error_warning_popup = ObjectProperty(None)


    def print_error_msg(self, msg):
        """Print error in popup.

        :param msg: A string with the error/warning to print.
        """
        self.ids.error_msg.text = msg
