import json
from pathlib import Path


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


def calibrate(esp32, arduino, calib_path):
    pass
