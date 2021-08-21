"""" Popup to print measures."""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class MeasurePopup(Popup):
    """Measure popup class."""
    # TODO: Pantalla imprimir resultados -> Actualizar boton Stop->Volver
    #  y titulo del popup al acabar medidas
    id_measure_popup = ObjectProperty(None)

    def display_measure(self, measures):
        """Update the measures shown in the measure windows
        with the last six measures done.

        :param measures: A list that contains six dictionaries. Each
        dictionary contains some parameters calculated after the measure
        and their values.
        """
        lst_param = ['name', 'PCE', 'FF', 'Pmax', 'Jsc', 'Voc']
        for i in range(1, len(measures)+1):
            for j in range(1, 7):
                the_reference = self.ids['line_' + str(i) + str(j)]
                the_reference.text = str(measures[i-1][lst_param[j-2]])
