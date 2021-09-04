""""Popup to calibration."""
# FIXME: random provisional
import random
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

    def pass_arduino_2(self, arduino_widget):
        self.arduino = arduino_widget
        print(self.arduino)
        self.arduino.connect(self.arduino.search_ports()[0])
        print(self.arduino.port)

    def reset_popup(self):
        """Reset calibration popup attributes every time it is opened."""
        self.calibration_msg = ' . . . '
        self.ids.button_calibration_accept.disabled = True

    # FIXME: Esta función está de prueba, la llamada a able_button
    #  se sustituiria por la función que realiza la calibración
    def call_able_button(self):
        """Wait 3 seconds before able 'Accept' button."""
        # print(my_arduino)
        self.event = Clock.schedule_interval(self.update_fit, 2)
        Clock.schedule_once(self.able_button, 7)

    def update_fit(self, dt):
        msg = 'Cell: ' + str(random.randint(1,17)) \
              + '.\n Slope: ' + str(random.random()) \
              + '.\n Y-intercept: ' + str(random.random()) \
              + '.\n r2: ' + str(random.random())
        self.ids.calibration_fit.text = msg

    def able_button(self, dt):
        """Able 'Accept' button when the calibration has ended."""
        self.calibration_msg = 'Calibration has ended.'
        self.ids.button_calibration_accept.disabled = False
        self.event.cancel()
