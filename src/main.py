"""Main file."""

import json
from pathlib import Path
from keithley import lineal, hysteresis


def test_lineal_mode():
    """Test lineal mode."""
    cell_name = 'perovskita de prueba'
    electrode = 'B'
    directory = Path(__file__ + '/../measures').resolve()
    config_file = Path(__file__ + '/../config/default/mode.json').resolve()

    with open(config_file, 'r') as f:
        config_json = json.load(f)
    config = config_json['config']

    pv_param = lineal(cell_name, electrode, str(directory), config)

    for key, value in pv_param.items():
        print(key, value, sep=': ')


def test_hysteresis_mode():
    """Test hysteresis mode."""
    cell_name = 'perovskita de prueba'
    electrode = 'B'
    directory = Path(__file__ + '/../measures').resolve()
    config_file = Path(__file__ + '/../config/default/mode.json').resolve()

    with open(config_file, 'r') as f:
        config_json = json.load(f)
    config = config_json['config']

    pv_param = hysteresis(cell_name, electrode, str(directory), config)

    for key, value in pv_param.items():
        print(key, value, sep=': ')


if __name__ == '__main__':
    test_lineal_mode()
    test_hysteresis_mode()
