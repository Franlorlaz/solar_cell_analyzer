"""" Popup to calibration"""

from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class CalibrationPopup(Popup):
    id_calibration_popup = ObjectProperty(None)
    calibration_msg = StringProperty('')

    def __init__(self, **kwargs):
        super(CalibrationPopup, self).__init__(**kwargs)
        self.calibration_msg = ' . . . '
        self.ids.button_calibration_accept.disabled = True

    def able_button(self):
        Clock.schedule_once(self.my_callback, 3)

    def my_callback(self, dt):
        self.calibration_msg = 'Calibration has ended.'
        self.ids.button_calibration_accept.disabled = False


