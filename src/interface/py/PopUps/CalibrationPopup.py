""""Popup to calibration."""

from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class CalibrationPopup(Popup):
    """Calibration popup class"""

    id_calibration_popup = ObjectProperty(None)
    calibration_msg = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize calibration popup."""
        super(CalibrationPopup, self).__init__(**kwargs)
        self.calibration_msg = ' . . . '
        self.ids.button_calibration_accept.disabled = True

    def launch_calibration(self):
        self.reset_popup()
        self.open()
        self.call_able_button()

    def reset_popup(self):
        """Reset calibration popup attributes every time it is opened."""
        self.calibration_msg = ' . . . '
        self.ids.button_calibration_accept.disabled = True

    # FIXME: Esta función está de prueba, la llamada a able_button
    #  iría en Section3 cuando acabe la calibración
    def call_able_button(self):
        """Wait 3 seconds before able 'Accept' button."""
        # print(my_arduino)
        Clock.schedule_once(self.able_button, 3)

    def able_button(self, dt):
        """Able 'Accept' button when the calibration has ended."""
        self.calibration_msg = 'Calibration has ended.'
        self.ids.button_calibration_accept.disabled = False
