""""Popup to confirm calibration."""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from interface.py.PopUps.CalibrationPopup import CalibrationPopup


class ConfirmCalibrationPopup(Popup):
    """Confirm Calibration popup class"""
    id_confirm_calibration_popup = ObjectProperty(None)
    trigger_confirm_calibration = BooleanProperty(bool = False)

    def __init__(self, **kwargs):
        """Initialize confirm calibration popup."""
        super(ConfirmCalibrationPopup, self).__init__(**kwargs)
        self.trigger_confirm_calibration = False

    def pass_arduino_1(self, arduino_widget):
        self.arduino = arduino_widget
        print(self.arduino)

    def set_no(self):
        """Close popup."""
        self.dismiss()

    def set_yes(self):
        """Close popup and open calibration menu."""
        self.dismiss()
        calibration_popup = CalibrationPopup()
        calibration_popup.reset_popup()
        calibration_popup.pass_arduino_2(self.arduino)
        calibration_popup.open()
        calibration_popup.call_able_button()
