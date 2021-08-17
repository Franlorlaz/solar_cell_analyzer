#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRIPTION:

"""
# ***************************************************
# ***************************************************
#                     IMPORTS
# ***************************************************
# ***************************************************
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from os import listdir
from os.path import isfile, join
from pathlib import Path
import json

from py.PopUps.LinealPopup import LinealPopup
from py.PopUps.HysteresisPopup import HysteresisPopup
from py.PopUps.PolarizePopup import PolarizePopup
from py.PopUps.ExaminePopup import ExaminePopup
from py.PopUps.MeasurePopup import MeasurePopup
from py.PopUps.ErrorWarning import ErrorWarningPopup
from py.SectionsMainLayout import Section1
from py.SectionsMainLayout import Section2
from py.SectionsMainLayout import Section3
# from py.SectionsMainLayout import MainScreen

# ***************************************************
# ***************************************************
#                  KIVY CONFIG
# ***************************************************
# ***************************************************
# Kivy's version, window's size and app icon setting
kivy.require('2.0.0')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 550)
Config.set('graphics', 'height', 600)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # Remove red circle when right-click
Config.set('kivy','window_icon','icon3.png')

# Loads all kv file in kv/ dir
kv_path = str(Path(__file__ + '/../kv/').resolve()) + '/'
kv_load_dir = [f for f in listdir(kv_path)]
for dir in kv_load_dir:
    kv_load_list = [f for f in listdir(kv_path + dir) if isfile(join(kv_path + dir, f))]
    for file in kv_load_list:
        if file.endswith('.kv'):
            Builder.load_file(kv_path + dir + '/' + file)



# ***************************************************
# ***************************************************
#                     MAIN LAYOUT
# ***************************************************
# ***************************************************
class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.LinealPopup = LinealPopup()
        self.HysteresisPopup = HysteresisPopup()
        self.PolarizePopup = PolarizePopup()
        self.ExaminePopup = ExaminePopup()
        self.MeasurePopup = MeasurePopup()
        self.ErrorWarningPopup = ErrorWarningPopup()

    def act_label_dir(self):
        self.ids.section3.ids.directory_label.text = str(self.ExaminePopup.ids.filechooser.selection[0])
        self.ExaminePopup.dismiss()

    def stop(self):
        self.MeasurePopup.ids.stop_button.text = 'Stop'
        trigger_path = Path(__file__ + '/../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        trigger['stop_button'] = True
        with open(trigger_path, 'w') as f:
            json.dump(trigger, f, indent=2, sort_keys=True)
        self.MeasurePopup.ids.stop_button.text = 'Volver'


from kivy.uix.actionbar import ActionBar
from kivy.properties import ObjectProperty


class ActionBarS0(ActionBar):
    id_actionbar_S0 = ObjectProperty(None)

    def prueba(self):
        self.parent.ids.section3.arduino = 'puerto 1'

# ***************************************************
# ***************************************************
#                     APP
# ***************************************************
# ***************************************************
class Main_kv(App):
    title = 'Solar Cell Analyzer'
    def build(self):
        self.icon = r'icon3.png' #Icono en el mismo directorio que el archivo principal, sino especificar ruta
        return MainScreen()


# ***************************************************
# ***************************************************
#                     RUNNING
# ***************************************************
# ***************************************************
if __name__ == '__main__':
    Main_kv().run()
