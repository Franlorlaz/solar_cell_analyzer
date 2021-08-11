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
from py.PopUps.PolarizationPopup import PolarizationPopup
from py.PopUps.ExaminePopup import ExaminePopup
from py.PopUps.MeasurePopup import MeasurePopup
from py.SectionsMainLayout import Section1
from py.SectionsMainLayout import Section2
from py.SectionsMainLayout import Section3
# from py.SectionsMainLayout import MainScreen
#TODO: Hay que importar los Section_i aunque no se usen explicitamente. MainScreen declarado explicitamente o no funciona.

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
        self.PolarizationPopup = PolarizationPopup()
        self.ExaminePopup = ExaminePopup()
        self.MeasurePopup = MeasurePopup()

    def act_label_dir(self):
        self.ids.section3.ids.directory_label.text = str(self.ExaminePopup.ids.filechooser.selection)
        self.ExaminePopup.dismiss()

    def stop(self):
        self.MeasurePopup.ids.stop_button.text = 'Stop'
        trigger = {'stop_button': True}
        trigger_path = Path(__file__ + '/../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'w') as f:
            json.dump(trigger, f)
        self.MeasurePopup.ids.stop_button.text = 'Volver'

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

#TODO: Action bar para Arduino/Keithley/ESP32 -> Pruebas en Spyder
#TODO: Ventanas de error si no se rellenan los campos de config
#TODO: Ventanas de error o valores por defectos (notificacion) si no se rellenan los campos principales
#TODO: Comprobar nombres de archivos de la seccion 2