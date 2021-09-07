import json
import time
from pathlib import Path
from .regression import linear_regression


def polarize(esp32, path, calib_path, reset=False):
    path = Path(path).resolve()
    calib_path = Path(calib_path).resolve()
    with open(calib_path, 'r') as f:
        calib = json.load(f)
    with open(path, 'r') as f:
        polarization = json.load(f)

    for key, value in polarization.items():
        electrode = ['A', 'B', 'C', 'D'].index(key[1]) + 1
        esp32.set_channel(cell=key[0], electrode_id=electrode)
        if reset:
            polarization[key] = 0.0
            esp32.polarize(0)
        else:
            esp32.polarize(value, calib[key])

    with open(path, 'w') as f:
        json.dump(polarization, f, indent=2)


def calibrate(esp32, arduino, keithley, calib_path, reset=False):
    cells = ['1', '2', '3', '4']
    elects = ['A', 'B', 'C', 'D']
    y = list(range(0, 256, 5))  # duty_cycle
    x = []  # real voltage
    calib_path = Path(calib_path).resolve()
    with open(calib_path, 'r') as f:
        calibration = json.load(f)
    arduino.switch_relay(switch_off=True, calibration=True)
    for cell in cells:
        for elect in elects:
            iteration = cell + elect
            elect_id = elects.index(elect) + 1
            arduino.switch_relay(cell=cell, electrode_id=elect_id)
            esp32.set_channel(cell=cell, electrode_id=elect_id)
            for duty_cycle in y:
                esp32.polarize(duty_cycle)
                voltage = keithley.voltmeter()
                x.append(voltage)
                time.sleep(0.2)
            esp32.polarize(0)
            if reset:
                a = 1
                b = 0
                r2 = 0
            else:
                a, b, r2 = linear_regression(x, y)
            calibration[iteration] = {'a': a, 'b': b, 'r2': r2}
            x = []
    arduino.switch_relay(switch_off=True, calibration=False)
    with open(calib_path.resolve(), 'w') as f:
        json.dump(calibration, f, indent=2)
