"""" Popup to print measures"""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class MeasurePopup(Popup):
    # TODO: Pantalla imprimir resultados -> Actualizar (iniciadas a cero) labels con datos del fichero de medida y actualizar boton Stop->Volver y titulo del popup al acabar medidas
    id_measurepopup = ObjectProperty(None)

    def display_measure(self):
        with open('interface/prueba_medidas.dat', 'r') as f:
            lines = f.readlines()
            print('Contents: ', lines)
        self.ids.prueba_1.text = lines[0]

