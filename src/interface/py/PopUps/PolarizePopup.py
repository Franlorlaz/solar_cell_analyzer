"""" Popup to polarization configuration"""

import json
from pathlib import Path
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


# TODO: Polarize: popup inicial al darle a "Start" cuando esté maracado, con botón "Continuar" para pasar las medidas
class PolarizePopup(Popup):
    id_polarize_popup = ObjectProperty(None)

    def stop_polarize(self):
        self.dismiss()

    def polarize_next_cell(self):
        cell_lst = ['A', 'B', 'C', 'D']
        actual_value = self.ids.polarization_text.text
        ref = cell_lst.index(actual_value)

        if ref == len(cell_lst)-1:
            self.ids.polarization_text.text = 'Polarization is over'
            self.ids.continue_polarize.text = 'End'
        else:
            self.ids.polarization_text.text = cell_lst[ref + 1]


    def end_polarize(self):
        self.dismiss()