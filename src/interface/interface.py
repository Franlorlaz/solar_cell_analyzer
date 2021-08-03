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

class ExaminePopup(Popup):
    id_examinepopup = ObjectProperty(None)

    def selected(self):
        # Variables for widget
        name = self.ids.filechooser.selection
        print(name)

#TODO: Pantalla imprimir resultados -> Crear labels con datos del fichero de medida y actualizar boton Stop->Volver y titulo del popup al acabar mediads
class MeasurePopup(Popup):
    id_measurepopup = ObjectProperty(None)

class Section1(BoxLayout):
    id_section1 = ObjectProperty(None)
    pass

class Section2(BoxLayout):
    id_section2 = ObjectProperty(None)
    pass

class Section3(BoxLayout):
    id_section3 = ObjectProperty(None)

    def Start_button(self):
        mode_dict = dict()
        #params_mode_dict_lst = ['name','config']
        mode_dict['name'] = self.parent.ids.section1.ids.mode_spinner.text
        mode_dict['config'] = 'path/to/file/mode.json'

        repeat_dict = dict()
        #params_repeat_dict_lst = ['type', 'times', 'wait']
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
            'saving_directory': self.parent.ids.section3.ids.directory_label.text,
            'mode': mode_dict,
            'repeat': repeat_dict,
            'cells': cells_dict
        }
        print(interface_dict)

        # Crea el popup de medida y lo abre
        midiendo = MeasurePopup()
        midiendo.open()


class MainScreen(BoxLayout):
    def act_label_dir(self):
        # TODO: Actualizar label del directorio -> ¿Como acceder a widget del popup cuando esta cerrado?
        self.ids.section3.ids.directory_label.text = self.ids.id_examinepopup.ids.filechooser.text
            #self.ids.section1.ids.mode_spinner.text
            #self.ids.id_examinepopup.ids.filechooser.text
            # FUNCIONA ACTUALIZANDO AL MODO DEL SPINNER PERO NO AL DIRECTORIO DEL POPUP

        print('Etiqueta de directorio actualizada')

# ***************************************************
# ***************************************************
#                     APP
# ***************************************************
# ***************************************************
#TODO: (Secundario??) Mantener los valores de la ventana de configuracion despues de salvar los datos y cerrarla
#TODO: Action bar para Arduino/Keithley/ESP32
class Main_kv(App):
    title = 'Solar Cell Analyzer'
    def build(self):
        # Config.set('kivy','window_icon','path/to/icon.ico') #TODO: Icono de Fran
        #self.icon = 'myicon.png' #Icono en el mismo directorio que el archivo principal
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