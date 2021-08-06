
import datetime
from ..devices.Keithley import Keithley
from ..utils.path_maker import make_folder, make_file
from ..utils.pv_param import pv_param, save_pv_param


def lineal(cell_name, electrode, directory, config, keithley=None):
    """Function to make folders and files required, measure and calculate.

    :param electrode: Number of electrode measured: 0, 1, 2, 3.
    :param cell_name: Sample's name.
    :param directory: Base directory where place or search for directories
    where save data generated.
    :param config: Keithley configuration. Must be a dictionary with the
    next keys: {'mode', 'v_1', 'v_2', 'points', 'speed', 'delay', 'cmpl'}.
    :param keithley: A Keithley object or the port to connect (str).
    :return: A result tuple = (PCE, FF, iPmax, Pmax, Jsc, Voc, P_sol, A)
    """

    if not cell_name:
        cell_name = 'no_name'
    else:
        cell_name = cell_name.replace(' ', '_')

    today = datetime.date.today().strftime('%Y-%m-%d')
    now = datetime.datetime.now().strftime('%H-%M-%S')

    folder = make_folder(directory + '\\' + today, new=False)
    folder = make_folder(folder + '\\' + cell_name, new=False)

    file = now + '_lineal_' + electrode
    file_data = folder + '\\' + file
    file_calculations = folder + '\\' + cell_name
    file_data = make_file(file_data, new=True)
    file_calculations = make_file(file_calculations, header=True)

    if not keithley or type(keithley) == str:
        keithley = Keithley(port=keithley)
    data = keithley.measure(config=config)
    keithley.save(data, file_data)

    results = pv_param(data)
    save_pv_param(file_calculations, file, results)

    return results
