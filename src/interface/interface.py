#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jun 2021
@author: Laura Garrido Regife
@e-mail: lgarridoregife@gmail.com

DESCRIPTION:

"""
# ***************************************************
# ***************************************************
#                   KIVY VERSION
# ***************************************************
# ***************************************************
import kivy
kivy.require('2.0.0')


# ***************************************************
# ***************************************************
#                IMPORT FROM KIVY
# ***************************************************
# ***************************************************
# Base class for creating Kivy Apps
from kivy.app import App

# Window's size setting
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 550)
Config.set('graphics', 'height', 600)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # Remove red circle when right-click

# Modulos
from kivy.uix import widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooser
from kivy.uix.dropdown import DropDown

# TODO: (Utilidades usadas en .kv's) Por ahora esto no hace nada, porque igualmente hay que ponerlas en main_kv.kv para que funcione.
# import kivy.utils
# from kivy.factory import Factory

# Builder is a global Kivy instance used in widgets that you can use
# to load other kv files in addition to the default ones.
from kivy.lang import Builder
import os
from os import listdir
from os.path import isfile, join

# Loads all kv file in kv/ dir
kv_path = os.getcwd() + '/kv/'
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
from kivy.clock import Clock
class MainScreen(BoxLayout):
    def imprimir_label(self):
        print('Guardado de lineal')
        #print(self.ids)

class MyPopup(Popup):
    def selected(self):
        # Variables for widget
        name = self.ids.filechooser.selection
        print(name)

        # Update label #NO FUNCIONA
        self.ids.directory_label.text = name

# ***************************************************
# ***************************************************
#                     APP
# ***************************************************
# ***************************************************
class Main_kv(App):
    title = 'Solar Cell Analyzer'
    def build(self):
        return MainScreen()

    def current_mode_state(self,mode):
        print(mode + ' selected.')
        # conf_mode = mode

# ***************************************************
# ***************************************************
#                     RUNNING
# ***************************************************
# ***************************************************
if __name__ == '__main__':
    Main_kv().run()