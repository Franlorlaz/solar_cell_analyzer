"""" Popup to polarization configuration."""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


# TODO: Polarize: popup inicial al darle a "Start" cuando esté maracado,
#  con botón "Continuar" para pasar las medidas
class PolarizePopup(Popup):
    """Polarization popup class."""
    id_polarize_popup = ObjectProperty(None)

    def stop_polarize(self):
        """Stop the popup."""
        self.dismiss()

    def polarize_next_cell(self):
        """Go to next polarization measurement."""
        cell_lst = ['A', 'B', 'C', 'D']
        actual_value = self.ids.polarization_text.text
        ref = cell_lst.index(actual_value)

        if ref == len(cell_lst)-1:
            self.ids.polarization_text.text = 'Polarization is over'
            self.ids.continue_polarize.text = 'End'
        else:
            self.ids.polarization_text.text = cell_lst[ref + 1]

    def end_polarize(self):
        """Close the popup after ending polarization measurement."""
        self.dismiss()
