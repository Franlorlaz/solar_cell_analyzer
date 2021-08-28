"""Section 2: cells configuration."""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class Section2(BoxLayout):
    """Section 2 (cells configuration) class."""
    id_section_2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Initialize attributes."""
        super(Section2, self).__init__(**kwargs)
        self.id_i = ['1', '2', '3', '4']
        self.id_j = ['a', 'b', 'c', 'd']

    def select_all_electrodes(self):
        """Select all electrodes to measure."""
        for i in self.id_i:
            for j in self.id_j:
                the_reference = self.ids['cell_' + i + j]
                the_reference.active = True

    def deselect_all_electrodes(self):
        """Deselect all electrodes to measure."""
        for i in self.id_i:
            for j in self.id_j:
                the_reference = self.ids['cell_' + i + j]
                the_reference.active = False

