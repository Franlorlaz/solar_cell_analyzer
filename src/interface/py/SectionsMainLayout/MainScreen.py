"""MainScreen"""

import json
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from py.PopUps.LinealPopup import LinealPopup
from py.PopUps.HysteresisPopup import HysteresisPopup
from py.PopUps.ExaminePopup import ExaminePopup
from py.PopUps.MeasurePopup import MeasurePopup


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.LinealPopup = LinealPopup()
        self.HysteresisPopup = HysteresisPopup()
        self.ExaminePopup = ExaminePopup()
        self.MeasurePopup = MeasurePopup()

    def act_label_dir(self):
        self.ids.section3.ids.directory_label.text = str(self.ExaminePopup.ids.filechooser.selection)
        self.ExaminePopup.dismiss()

    def stop(self):
        print(self.MeasurePopup.ids.stop_button.text == 'Volver')
        if self.MeasurePopup.ids.stop_button.text == 'Stop':
            trigger = {'stop_button': True}
            trigger_path = Path(__file__ + '/../../config/tmp/trigger.json')
            trigger_path = trigger_path.resolve()
            with open(trigger_path, 'w') as f:
                json.dump(trigger, f)
            self.MeasurePopup.ids.stop_button.text = 'Volver'

        elif self.MeasurePopup.ids.stop_button.text == 'Volver':
            #self.MeasurePopup.dismiss()
            pass
