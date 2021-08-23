"""Section 0: Superior bar"""

from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionGroup
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionPrevious
from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from keithley import Keithley


class ActionBarS0(ActionBar):
    id_actionbar_S0 = ObjectProperty(None)
    fake_keithley = Keithley(port=None)

    def __init__(self, **kwargs):
        super(ActionBarS0, self).__init__(**kwargs)
        self.keithley_ports_lst = self.fake_keithley.search_ports()

    def create_port_lst(self):
        arduino_ports_lst = self.parent.ids.section3.arduino.search_ports()
        esp32_ports_lst = self.parent.ids.section3.esp32.search_ports()
        keithley_ports_lst = Keithley.search_ports()
        # arduino_ports_lst = ['ardu one', 'ardu two', 'ardu three']
        # esp32_ports_lst = ['esp32 alpha', 'esp32 beta']
        # keithley_ports_lst = ['keithley w', 'keithley x', 'keithley y', 'keithley z']

        self.ids.arduino_port_1.text = 'Simulation port'
        self.ids.arduino_port_2.text = arduino_ports_lst[0]
        self.ids.esp32_port_1.text = 'Simulation port'
        self.ids.esp32_port_2.text = esp32_ports_lst[0]
        self.ids.keithley_port_1.text = 'Simulation port'
        self.ids.keithley_port_2.text = keithley_ports_lst[0]

        for port in arduino_ports_lst[1:]:
            action_group = self.ids.arduino_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: self.connect_arduino_to_port(port.text))
            action_group.add_widget(action_button)

        for port in esp32_ports_lst[1:]:
            action_group = self.ids.esp32_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: self.connect_esp32_to_port(port.text))
            action_group.add_widget(action_button)

        for port in keithley_ports_lst[1:]:
            action_group = self.ids.keithley_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: self.connect_keithley_to_port(port.text))
            action_group.add_widget(action_button)


    def connect_arduino_to_port(self, port):
        if port == 'Simulation port':
            port = None
        self.parent.ids.section3.arduino.connect(port)

    def connect_esp32_to_port(self, port):
        if port == 'Simulation port':
            port = None
        self.parent.ids.section3.esp32.connect(port)

    def connect_keithley_to_port(self, port):
        if port == 'Simulation port':
            port = 'None'
        self.parent.ids.section3.keithley = port
