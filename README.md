# Solar Cell analyzer

### Dependencies table

| arduino        | esp32       | keithley      | interface   |
|----------------|-------------|---------------|-------------|
| `pyserial 3.5` | `paquete 1` | `numpy 1.21`  | `kivy 2.0`  |
|                | `paquete 2` | `PyVISA 1.11` |             |


# Arduino module

## Usage by Command Line Interface

You can use the arduino Command Line Interface (CLI) by running the `CLI.py` 
python file in `arduino` directory: `python3 arduino/CLI.py <command>`.
There are two possible commands:
- The `ports` command shows a list of all available devices to connect.
- The `connect` command connects to the specified device and open an 
  interactive session. By default, it connects to a virtual device that
  simulate an arduino. To specify a real device, write it after `--port` 
  option. To write the `connect`command without the `--port` option is 
  equivalent to `--port None`.
  
```shell
$ python3 arduino/CLI.py ports
Arduino Relay Controller.

--- Ports ---
/dev/ttyACM0
/dev/ttyS0

```

```shell
$ python3 arduino/CLI.py connect --port /dev/ttyACM0
Arduino Relay Controller.

Arduino connected to:  /dev/ttyACM0

--- Arduino Shell ---
Type `help` or `?` to list commands and `disconnect` to exit.

>> 
```

After connection to a device, an interactive session starts. To disconnect the
device and exit the interactive session, run `disconnect`. Once in the "arduino
shell", you can open a relay by `open <cell><electrode>` where `<cell>` is a
digit (allowed digits: 1, 2, 3, 4) and `<electrode>` is a letter (allowed 
letters: A, B, C, D). The *open* action switch off all relays and then switch 
on the specified one. To switch off all relays without switching on any one, 
run `close all`.

```shell
>> open 1A
```

```shell
>> close all
```

```shell
>> disconnect
Arduino disconnected
```

## Importing Arduino

```python
from arduino import Arduino

ports_list = Arduino.search_ports()
device_port = ports_list[0]

my_arduino = Arduino(port=device_port)

switch_info_1 = my_arduino.switch_relay(cell=1, electrode_id=1)  # open 1A
switch_info_2 = my_arduino.switch_relay(switch_off=True)  # close all

serial_simulation = my_arduino.disconnect()
serial_1 = my_arduino.connect(device_port, disconnect_before=False)
serial_2 = my_arduino.connect(device_port)  # disconnect_before=True
```

From arduino module you can import the `Arduino` class, which has the static 
method `search_ports()`. This method return a list of strings naming all 
available devices. You can instantiate the `Arduino` class specifying the
device to connect. If no device is given, arduino connects to port `None`, 
returning an Arduino object that simulate a successful connection. Port `None`
can be useful for developing and debugging purposes.

An arduino object has two attributes: `my_arduino.port` and `my_arduino.ser`.
The first contains the name of the port connected to. The second contains an
object of the `pyserial` module with information and methods for controlling
the device.

The `switch_relay()` method can be used to switch off all relays 
(`switch_off=True`) or to switch on one (`cell=1, electrode_id=1`) specifying
the cell (an integer: 1, 2, 3, 4)  and an electrode (an integer: 1, 2, 3, 4).
When switching on one, first all relays are switched off and then the one is
switched on.

You can disconnect the device by calling `disconnect()` method. After 
disconnection, the object automatically connect to the virtual device changing
the `port` to `None`. The object returned is the attribute `ser` which now
contains an arduino simulator. You can reconnect to a real device calling
the method `connect()` specifying as first argument the device to connect.
The object returned by this method is the same in attribute `ser`. You can
also set the argument `disconnect_before` to disconnect the current device 
before connecting to the new one. This argument is optional and by default
is `False`.

-------------------------------------------------------------------------------