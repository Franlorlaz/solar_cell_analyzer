"""Section 0: Superior bar"""

from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionGroup
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionPrevious
from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from arduino import Arduino
from keithley import Keithley
from interface.py.PopUps.ErrorWarningPopup import ErrorWarningPopup

class ActionBarS0(ActionBar):
    id_actionbar_S0 = ObjectProperty(None)
    fake_arduino = Arduino(port=None)
    fake_esp_32 = Arduino(port=None)
    fake_keithley = Keithley(port=None)

    # @mainthread
    def __init__(self, **kwargs):
        super(ActionBarS0, self).__init__(**kwargs)
        self.arduino_ports_lst = self.fake_arduino.search_ports()
        self.keithley_ports_lst = self.fake_keithley.search_ports()
        # FIXME: No se puede inicializar con los widgets de la seccion 3 porque aun no estan creados

    # METODO PARA CREAR LOS PUERTOS USADO EN ARDUINO (INCLUYE CHAPUZA DEL RESIZE)
    def create_arduino_port_lst2(self):
        self.arduino_ports_lst = self.parent.ids.section3.arduino.search_ports()
        # print(self.arduino_ports_lst)
        # print(self.ids.arduino_spinner.list_action_item)

        # FIXME: No actualiza los nuevos hasta que se reajusta el tamaño de la ventana
        #  --> He hecho una super chapuza para que cambie un pixel el tamaño de la ventana
        if self.ids.arduino_port_1.text == ' Init ':
            self.ids.arduino_port_1.text = ' --- '
            for port in self.arduino_ports_lst:
                action_group = self.ids.arduino_spinner
                action_button = ActionButton(text=port)
                action_button.bind(on_press = lambda port: self.connect_arduino_to_port(port.text))
                action_group.add_widget(action_button)

        # print(self.ids.arduino_spinner.list_action_item)


    # METODO PARA CREAR LOS PUERTOS USADO EN ESP32
    def create_ports(self):
        self.esp32_ports_lst = ['uno', 'dos', 'tres'] # self.parent.ids.section3.arduino.search_ports()
        self.ids.esp32_port_1.text = self.esp32_ports_lst[0]
        for port in self.esp32_ports_lst[1:]:
            action_group = self.ids.esp32_spinner
            action_button = ActionButton(text=port)
            action_button.bind(on_press = lambda port: self.connect_arduino_to_port(port.text))
            action_group.add_widget(action_button)

    # METODO PARA CREAR LOS PUERTOS USADO EN KEITHLEY
    def update_ports(self):
        for i in range(min(len(self.keithley_ports_lst), 6)):
            the_reference = self.ids['keithley_port_' + str(i + 1)]
            the_reference.text = self.keithley_ports_lst[i]
            # FIXME: Si los puertos se actualizan al pulsar el grupo, pueden leerse los puertos
            #  del arduino/keithley real de la section3, en vez de generar el fake en el init.

    def connect_arduino_to_port(self, port):
        if port == ' --- ':
            port = None
        self.parent.ids.section3.arduino.connect(port)

    def connect_keithley_to_port(self, port):
        if port == ' - - - ':
            error_warning_popup = ErrorWarningPopup()
            error_warning_popup.open()
            msg = "The selected port doesn't exist."
            error_warning_popup.print_error_msg(msg)
        else:
            self.parent.ids.section3.keithley = port
