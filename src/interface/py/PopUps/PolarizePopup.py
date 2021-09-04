"""" Popup to polarization configuration."""

from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class PolarizePopup(Popup):
    """Polarization popup class."""
    id_polarize_popup = ObjectProperty(None)
    title_msg = StringProperty('')
    description_msg = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize polarize popup."""
        super(PolarizePopup, self).__init__(**kwargs)

    def pass_arg(self, sequence):
        self.sequence = sequence
        print(sequence)
        self.title_msg = 'All electrodes covered except ' \
                         + str(self.sequence[0])
        self.description_msg = "Press 'Continue' to start the measure."

    # TODO: Que detenga el proceso, no solo cerrar el popup
    def stop_polarize(self):
        """Stop the popup."""
        self.dismiss()

    def polarize_next_cell(self):
        """Go to next polarization measurement."""
        description = self.ids.polarization_description
        actual_value = self.ids.polarization_title.text[-2:]
        ref = self.sequence.index(actual_value)

        if description.text[0:5] == "Press":
            description.text = 'Measuring...'
            self.ids.continue_polarize.disabled = True
            Clock.schedule_once(self.prueba, 3)

        elif ref < len(self.sequence) - 1:
            self.ids.polarization_title.text = \
                'All electrodes covered except ' \
                + str(self.sequence[ref + 1])
            description.text = "Press 'Continue' to start the measure."

        if ref == len(self.sequence) - 1 and \
                description.text[0:7] == 'Measure':
            self.ids.polarization_title.text = 'ZZZZZ is over'
            description.text = "Initial voltages at maximun power " \
                               "calculated. Press 'Start' to BLABLABLA "
            self.ids.continue_polarize.text = 'Start'

    def prueba(self, dt):
        """Able 'Accept' button when the calibration has ended."""
        description = self.ids.polarization_description
        description.text = 'Measure done. \n'\
                           + 'Voltage at maximun power: ' + str(2.3) + '. \n'\
                           + 'Go to next cell.'
        self.ids.continue_polarize.disabled = False

    def start_measure(self):
        """Close the popup and start the measure applying voltage at
        maximun power."""
        self.dismiss()
