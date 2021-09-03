"""Main file for interface."""

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock

from os import listdir
from os.path import isfile, join
from pathlib import Path
import json

from interface.py.PopUps.LinealPopup import LinealPopup
from interface.py.PopUps.HysteresisPopup import HysteresisPopup
from interface.py.PopUps.PolarizePopup import PolarizePopup
from interface.py.PopUps.CalibrationPopup import CalibrationPopup
from interface.py.PopUps.ExaminePopup import ExaminePopup
from interface.py.PopUps.MeasurePopup import MeasurePopup
from interface.py.PopUps.ErrorWarningPopup import ErrorWarningPopup
from interface.py.PopUps.InfoPopup import InfoPopup
from interface.py.SectionsMainLayout import Section1
from interface.py.SectionsMainLayout import Section2
from interface.py.SectionsMainLayout import Section3

# ***************************************************
# ***************************************************
#                  KIVY CONFIG
# ***************************************************
# ***************************************************
# Kivy's version, window's size and app icon setting
kivy.require('2.0.0')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 550)
Config.set('graphics', 'height', 650)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'window_icon', 'interface/icon3.png')

# Loads all kv file in kv/ dir
kv_path = str(Path(__file__ + '/../interface/kv/').resolve()) + '/'
kv_load_dir = [f for f in listdir(kv_path)]
for directory in kv_load_dir:
    kv_load_list = [f for f in listdir(kv_path + directory)
                    if isfile(join(kv_path + directory, f))]
    for file in kv_load_list:
        if file.endswith('.kv'):
            Builder.load_file(kv_path + directory + '/' + file)


# ***************************************************
# ***************************************************
#                   MAIN SCREEN
# ***************************************************
# ***************************************************
class MainScreen(BoxLayout):
    """Main screen class."""

    def __init__(self, **kwargs):
        """Initialize popups."""
        super(MainScreen, self).__init__(**kwargs)
        self.lineal_popup = LinealPopup()
        self.hysteresis_popup = HysteresisPopup()
        self.polarize_popup = PolarizePopup()
        self.calibration_popup = CalibrationPopup()
        self.examine_popup = ExaminePopup()
        self.measure_popup = MeasurePopup()
        self.error_warning_popup = ErrorWarningPopup()
        self.info_popup = InfoPopup()

    def act_label_dir(self):
        """Update directory label in section 3."""
        self.ids.section3.init_dir = \
            str(self.examine_popup.ids.filechooser.selection[0])
        self.ids.section3.init_dir_clipped = \
            '...' + self.ids.section3.init_dir[-33:]
        self.ids.section3.ids.directory_label.text = \
            self.ids.section3.init_dir_clipped
        self.examine_popup.dismiss()

    def stop(self):
        """Change trigger for stop button to True."""
        self.measure_popup.ids.stop_button.text = 'Stop'
        trigger_path = Path(__file__ + '/../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        trigger['stop_button'] = True
        with open(trigger_path, 'w') as f:
            json.dump(trigger, f, indent=2, sort_keys=True)
        self.measure_popup.ids.stop_button.text = 'Go back'


from interface.py.SectionsMainLayout.ActionBarS0 import ActionBarS0
from kivy.core.window import Window


# ***************************************************
# ***************************************************
#                     APP
# ***************************************************
# ***************************************************
class Main_kv(App):
    """App main class"""
    title = 'Solar Cell Analyzer'

    def build(self):
        """Build the app.

        :return: Main screen class.
        """
        self.icon = r'interface/icon3.png'
        # Clock.schedule_interval(self.update, 1)
        return MainScreen()

    @staticmethod
    def update(dt):
        """Update app's interface every microsecond."""
        Clock.usleep(1)

    @staticmethod
    def resize_window():
        """Resize app's windows."""
        Window.size = (549, 650)

    @staticmethod
    def restore_window():
        """Restore app's windows size."""
        Window.size = (550, 650)


# ***************************************************
# ***************************************************
#                     RUNNING
# ***************************************************
# ***************************************************
if __name__ == '__main__':
    Main_kv().run()
