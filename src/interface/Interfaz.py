#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 16:08:13 2021
@author: Laura Garrido Regife
@e-mail: laugarreg@alum.us.es
"""
# ***************************************************
# ***************************************************
#           IMPORTACION Y VERSION DE KIVY
import kivy

kivy.require('2.0.0')
# ***************************************************
# ***************************************************

# ***************************************************
# ***************************************************
#         IMPORTACION DE LIBRERIAS DE KIVY
# ***************************************************
# ***************************************************

# Libreria principal para Apps
from kivy.app import App

# Modulo para el tamaño de inicio de la ventana
from kivy.config import Config

# Configuracion del tamaño inicial de la ventana de la App
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 550)
Config.set('graphics', 'height', 600)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # Quita el punto rojo del boton secundario

# Modulos
from kivy.uix import widget
from kivy.uix.boxlayout import BoxLayout
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
from kivy.uix.popup import Popup


# ***************************************************
# ***************************************************
#                     MAIN CODE
# ***************************************************
# ***************************************************
class MainScreen(BoxLayout):
    None


class Seccion1(BoxLayout):
    None


class Seccion2(BoxLayout):
    None


class Seccion3(BoxLayout):
    None


class MyButton():
    None


class MyPopup(Popup):
    def selected(self):
        # Variables for widget
        name = self.ids.filechooser.selection
        print(name)

        # Update label
        self.ids.directory_label.text = name


# ***************************************************
# ***************************************************
#                     APP
# ***************************************************
# ***************************************************
class Main_layout(App):
    title = 'Keithley'

    # Definicion del constructor
    def build(self):
        return MainScreen()


# ***************************************************
# ***************************************************
#                     RUNNING
# ***************************************************
# ***************************************************
# Convencion para correr la App en ciertas plataformas
if __name__ == '__main__':
    Main_layout().run()
