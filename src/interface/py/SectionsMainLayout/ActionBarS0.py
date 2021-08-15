"""Section 0: Superior bar"""

from kivy.uix.actionbar import ActionBar
from kivy.properties import ObjectProperty


class ActionBarS0(ActionBar):
    id_actionbar_S0 = ObjectProperty(None)

    def prueba(self):
        self.parent.ids.section3.arduino = 'puerto 1'
