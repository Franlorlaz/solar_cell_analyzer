"""Section 0: Superior bar"""

from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionButton
from kivy.properties import ObjectProperty
from keithley import Keithley


class ActionBarS0(ActionBar):
    """Section 0 (actionbar) class."""
    id_actionbar_S0 = ObjectProperty(None)

    def create_port_lst(self):
        """Generate the port list for Arduino, ESP32 and
        Keithley when some of the spinner are clicked."""
        arduino_ports_lst = self.parent.ids.section3.arduino.search_ports()
        esp32_ports_lst = self.parent.ids.section3.esp32.search_ports()
        keithley_ports_lst = Keithley.search_ports()
        # arduino_ports_lst = ['ardu one', 'ardu two', 'ardu three']
        # esp32_ports_lst = ['esp32 alpha', 'esp32 beta']
        # keithley_ports_lst = ['keithley w', 'keithley x', 'keithley y', 'keithley z']

        self.ids.arduino_port_1.text = '- - -'
        self.ids.arduino_port_2.text = arduino_ports_lst[0]
        self.ids.esp32_port_1.text = '- - -'
        self.ids.esp32_port_2.text = esp32_ports_lst[0]
        self.ids.keithley_port_1.text = '- - -'
        self.ids.keithley_port_2.text = keithley_ports_lst[0]

        for port in arduino_ports_lst[1:]:
            action_group = self.ids.arduino_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: \
                self.connect_arduino_to_port(port.text))
            action_group.add_widget(action_button)

        for port in esp32_ports_lst[1:]:
            action_group = self.ids.esp32_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: \
                self.connect_esp32_to_port(port.text))
            action_group.add_widget(action_button)

        for port in keithley_ports_lst[1:]:
            action_group = self.ids.keithley_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: \
                self.connect_keithley_to_port(port.text))
            action_group.add_widget(action_button)

    def connect_arduino_to_port(self, port):
        """Connect Arduino to an specific port.

        :param port: A str that contains the name of the port.
        """
        if port == '- - -':
            port = None
        self.parent.ids.section3.arduino.connect(port)

    def connect_esp32_to_port(self, port):
        """Connect ESP32 to an specific port.

        :param port: A str that contains the name of the port.
        """
        if port == '- - -':
            port = None
        self.parent.ids.section3.esp32.connect(port)

    def connect_keithley_to_port(self, port):
        """Connect Keithley to an specific port.

        :param port: A str that contains the name of the port.
        """
        if port == '- - -':
            port = None
        self.parent.ids.section3.keithley = port
