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

# Window's size and app icon setting
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 550)
Config.set('graphics', 'height', 600)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # Remove red circle when right-click
Config.set('kivy','window_icon','icon.png')

# Moduls
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

# TODO: (Utilidades usadas en .kv's) Aqui no hace nada (pueden quitarse), porque igualmente hay que ponerlas en main_kv.kv para que funcione.
# import kivy.utils
# from kivy.factory import Factory

# Builder is a global Kivy instance used in widgets that you can use
# to load other kv files in addition to the default ones.
from kivy.lang import Builder
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

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
import json
#TODO: Pasar todas las clases a archivos independientes en /py y cargarlas como los archivos de /kv
from kivy.properties import ObjectProperty

class LinealPopup(Popup):
    id_linealpopup = ObjectProperty(None)

    def dict_lineal(self):
        print('Guardado de lineal en diccionario')
        params_lineal_lst = [
            'param_v_start',
            'param_v_stop',
            'param_points',
            'param_speed',
            'param_delay',
            'param_cmpl',
            'param_light_power',
            'param_area'
        ]

        params_lineal = dict()
        for par in params_lineal_lst:
            the_reference = self.ids[par]
            params_lineal[par] = the_reference.text
            the_reference.text = the_reference.text

        dict_lineal = {'mode': 'Lineal',
                       'config': params_lineal}
        print(dict_lineal)

        # Create mode.json
        with open('interface/mode.json', 'w') as f:
            json.dump(dict_lineal, f, indent=2)

class HysteresisPopup(Popup):
    id_hysteresispopup = ObjectProperty(None)

    def dict_hysteresis(self):
        print('Guardado de hysteresis en diccionario')
        params_hysteresis_lst = [
            'param_v_start',
            'param_v_stop',
            'param_points',
            'param_speed',
            'param_delay',
            'param_cmpl',
            'param_light_power',
            'param_area'
        ]

        params_hysteresis = dict()
        for par in params_hysteresis_lst:
            the_reference = self.ids[par]
            params_hysteresis[par] = the_reference.text

        dict_hysteresis = {'mode': 'Hysteresis',
                       'config': params_hysteresis}
        print(dict_hysteresis)

        # Create mode.json
        with open('interface/mode.json', 'w') as f:
            json.dump(dict_hysteresis, f, indent=2)

class ExaminePopup(Popup):
    id_examinepopup = ObjectProperty(None)

    def selected(self):
        # Variables for widget
        name = self.ids.filechooser.selection
        print(name)

#TODO: Pantalla imprimir resultados -> Actualizar (iniciadas a cero) labels con datos del fichero de medida y actualizar boton Stop->Volver y titulo del popup al acabar medidas
class MeasurePopup(Popup):
    id_measurepopup = ObjectProperty(None)

    def display_measure(self):
        with open('interface/prueba_medidas.dat', 'r') as f:
            lines = f.readlines()
            print('Contents: ', lines)
        self.ids.prueba_1.text = lines[0]




class Section1(BoxLayout):
    id_section1 = ObjectProperty(None)
    pass

class Section2(BoxLayout):
    id_section2 = ObjectProperty(None)
    pass


import time
from kivy.clock import Clock


class Section3(BoxLayout):
    id_section3 = ObjectProperty(None)

    def Start_button(self):
        mode_dict = dict()
        # params_mode_dict_lst = ['name','config']
        mode_dict['name'] = self.parent.ids.section1.ids.mode_spinner.text
        mode_dict['config'] = 'path/to/file/mode.json'

        repeat_dict = dict()
        # params_repeat_dict_lst = ['type', 'times', 'wait']
        print(list(self.parent.ids.section1.ids))
        for par in ['no_repetition', 'electrode_repetition', 'all_repetition']:
            the_reference = self.parent.ids.section1.ids[par]
            if the_reference.active:
                repeat_dict['type'] = par
        repeat_dict['times'] = self.parent.ids.section1.ids.number_repetition.text
        repeat_dict['wait'] = self.parent.ids.section1.ids.time_repetition.text

        cells_dict = dict()
        params_cells_dict_lst = ['cell_1', 'cell_2', 'cell_3', 'cell_4']
        for par in params_cells_dict_lst:
            i_cell = dict()
            the_reference = self.parent.ids.section2.ids['textinput_' + par]
            i_cell['name'] = the_reference.text
            i_cell['electrodes'] = []
            for i in ['A', 'B', 'C', 'D']:
                the_reference = self.parent.ids.section2.ids[par+i.lower()]
                if the_reference.active:
                    i_cell['electrodes'].append(i)
            cells_dict[par] = i_cell

        interface_dict = {
            'saving_directory': str(self.parent.ids.section3.ids.directory_label.text),
            'mode': mode_dict,
            'repeat': repeat_dict,
            'cells': cells_dict
        }
        print(interface_dict)

        # Create interface.json
        with open('interface/interface.json', 'w') as f:
            json.dump(interface_dict, f, indent=2)

        # Crea el popup de medida y lo abre
        midiendo = MeasurePopup()
        midiendo.open()

        self.run()
        Clock.schedule_once(self.run, 1)

        midiendo.display_measure()

    def run(self, *dt):
        trigger_path = Path(__file__ + '/../../config/tmp/trigger.json')
        trigger_path = trigger_path.resolve()
        with open(trigger_path, 'r') as f:
            trigger = json.load(f)
        print('----- running: ', dt)
        if not trigger['stop_button']:
            Clock.schedule_once(self.run, 1)


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
        MeasurePopup.dismiss()
        print(self.MeasurePopup.ids.stop_button.text == 'Volver')
        if self.MeasurePopup.ids.stop_button.text == 'Stop':
            trigger = {'stop_button': True}
            trigger_path = Path(__file__ + '/../../config/tmp/trigger.json')
            trigger_path = trigger_path.resolve()
            with open(trigger_path, 'w') as f:
                json.dump(trigger, f)
            self.MeasurePopup.ids.stop_button.text = 'Volver'

        elif self.MeasurePopup.ids.stop_button.text == 'Volver':
            pass

# ***************************************************
# ***************************************************
#                     APP
# ***************************************************
# ***************************************************
#TODO: Action bar para Arduino/Keithley/ESP32 -> Pruebas en Spyder
class Main_kv(App):
    title = 'Solar Cell Analyzer'
    def build(self):
        # TODO: Icono de Fran
        # Config.set('kivy','window_icon','path/to/icon.ico')
        #self.icon = r'icon.png' #Icono en el mismo directorio que el archivo principal, sino especificar ruta
        return MainScreen()

    # Testeo del modo seleccionado en el spineer de Section 1 -> Ya se puede eliminar
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


# app --> Main_kv(App)
# app.root --> MainScreen(BoxLayout)
# root --> Widget(Widget)