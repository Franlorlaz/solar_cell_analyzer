""""Popup to calibration."""
# FIXME: random provisional
import random
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from keithley import Keithley
from esp32 import calibrate


class CalibrationPopup(Popup):
    """Calibration popup class"""

    id_calibration_popup = ObjectProperty(None)
    calibration_msg = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize calibration popup."""
        super(CalibrationPopup, self).__init__(**kwargs)
        self.calibration_msg = ' . . . '
        self.ids.button_calibration_accept.disabled = True
        self.section3 = None

    def pass_arduino_2(self, section3):
        self.section3 = section3

    def reset_popup(self):
        """Reset calibration popup attributes every time it is opened."""
        self.calibration_msg = ' . . . '
        self.ids.button_calibration_accept.disabled = True

    def call_able_button(self):
        """Wait 3 seconds before able 'Accept' button."""
        # self.event = Clock.schedule_interval(self.update_fit, 2)
        Clock.schedule_once(self.able_button, 1)

    def update_fit(self, dt):
        msg = 'Cell: ' + str(random.randint(1, 17)) \
              + '.\n Slope: ' + str(random.random()) \
              + '.\n Y-intercept: ' + str(random.random()) \
              + '.\n r2: ' + str(random.random())
        self.ids.calibration_fit.text = msg

    def able_button(self, dt):
        """Able 'Accept' button when the calibration has ended."""
        calib_path = self.section3.paths['calibration_path']
        arduino = self.section3.arduino
        esp32 = self.section3.esp32
        keithley = Keithley(port=self.section3.keithley)
        calibrate(esp32, arduino, keithley, calib_path)
        keithley.close_resource()
        self.calibration_msg = 'Calibration has ended.'
        self.ids.button_calibration_accept.disabled = False
        # self.event.cancel()
