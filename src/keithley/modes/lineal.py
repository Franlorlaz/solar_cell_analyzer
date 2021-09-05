"""Lineal mode."""

from datetime import datetime
from pathlib import Path

from .devices import Keithley
from .utils import make_file, set_up_directories
from .utils import calculate_pv_param, save_pv_param


def lineal(cell_name, electrode, directory, config, keithley=None):
    """Run lineal mode.

    Measure from voltage V1 to V2 along N points.
    This mode set the Keithley to sweep mode.
    The measured and calculated data is automatically saved.

    :param cell_name: Sample's name.
    :param electrode: Electrode name. Should be one of: ['A', 'B', 'C', 'D'].
    :param directory: Root directory where save generated data.
    :param config: Keithley configuration. Must be a dictionary with the
    next keys: {'v_1', 'v_2', 'points', 'speed', 'delay', 'cmpl',
    'area', 'light_power'}.
    :param keithley: A Keithley object or the port to connect (str).
    :return: A dict with keys: {PCE, FF, iPmax, Pmax, Jsc, Voc, P_sol, A}.
    """
    electrode = str(electrode)
    directory = Path(directory).resolve()

    if ('v_1' not in config or
            'v_2' not in config or
            'points' not in config or
            'speed' not in config or
            'delay' not in config or
            'cmpl' not in config or
            'area' not in config or
            'light_power' not in config):
        raise ValueError(f'Missing config parameters in dict: {config}')

    area = config['area']
    light_power = config['light_power']

    if not cell_name:
        cell_name = 'no_name'
    else:
        cell_name = cell_name.replace(' ', '_')

    disconnect_keithley = False
    if not keithley or type(keithley) == str:
        keithley = Keithley(port=keithley)
        disconnect_keithley = True

    today_now = datetime.now().strftime('%y%m%d%H%M%S')

    base_dir = Path(set_up_directories(cell_name, directory)).resolve()
    base_dir = base_dir.joinpath(electrode).joinpath('lineal')

    file_data = base_dir.joinpath(today_now+'.txt')
    file_pv_param = base_dir.joinpath(cell_name+'-lineal-'+electrode+'.csv')

    file_data = make_file(str(file_data), new=True, extension=None)
    file_pv_param = make_file(str(file_pv_param), header=True, extension=None)

    file_data = Path(file_data).resolve()
    file_pv_param = Path(file_pv_param).resolve()

    keithley.set_config(config)
    keithley.set_sensors()
    keithley.set_source()
    keithley.source_sweep_mode()
    keithley.set_trigger()
    keithley.set_display()

    data = keithley.run(mode='lineal')
    pv_param = calculate_pv_param(data, area=area, light_power=light_power)

    keithley.save(file_data)
    save_pv_param(file_pv_param, today_now, param=pv_param)

    if disconnect_keithley:
        keithley.close_resource()

    return pv_param
