"""Managing PhotoVolatic parameters."""

import numpy as np
from pathlib import Path
import csv


def save_pv_param(file_name, name, param):
    """Save calculated PhotoVoltaic Parameters.

    :param file_name: Specifies the file's name where to save results
    (path or str object).
    :param name: Name of electrode. Should be equal to the file's name of data
    measured.
    :param param: A dictionary with values to write. Must have this keys:
    {PCE, FF, Pmax, Jsc, Voc, P_sol, A}.
    :return: None.
    """
    PCE = param['PCE']
    FF = param['FF']
    Pmax = param['Pmax']
    Jsc = param['Jsc']
    Voc = param['Voc']
    P_sol = param['P_sol']
    A = param['A']

    file_name = Path(file_name).resolve()
    with open(file_name, 'a') as file:
        file.write('%17s     %8.6E   %8.6E   %8.6E   %8.6E   %8.6E   %8.6E'
                   '   %8.6E\n' % (name, PCE, FF, Pmax, Jsc, Voc, P_sol, A))

    # with open(file_name, 'r') as file2:
    #     last_line_number = sum(1 for _ in file2)
    #
    # if last_line_number == 1:
    #     time = 0
    # else:
    #     with open(file_name, 'r') as file2:
    #         reader = csv.reader(file2, delimiter='\t')
    #         next(reader)
    #         init_time = next(reader)[0]
    #         time = int(name) - int(init_time)
    #
    # with open(file_name, 'a', newline='') as file2:
    #     fieldnames = ['File', 'PCE', 'FF', 'Pmax (W/cm2)',
    #                   'Jsc (A/cm2)', 'Voc (V)', 'P_sol (W/cm2)',
    #                   'area (cm2)', 'time']
    #     writer = csv.DictWriter(file2, fieldnames=fieldnames, delimiter='\t')
    #
    #     writer.writerow({'File': name,
    #                      'PCE': '%8.6E' % PCE,
    #                      'FF': '%8.6E' % FF,
    #                      'Pmax (W/cm2)': '%8.6E' % Pmax,
    #                      'Jsc (A/cm2)': '%8.6E' % Jsc,
    #                      'Voc (V)': '%8.6E' % Voc,
    #                      'P_sol (W/cm2)': '%8.6E' % P_sol,
    #                      'area (cm2)': '%8.6E' % A,
    #                      'time': str(time)})


def calculate_pv_param(data, area=0.14, light_power=0.1):
    """Calculate Photo Voltaic Parameters from data measured, as FF and PCE.

    :param data: Numpy array with three columns (V, I, t).
    :param area: Cell's area in [cm2].
    :param light_power: Light Power in [W/cm2].
    :return: A dict with keys: {PCE, FF, iPmax, Pmax, Jsc, Voc, P_sol, A}.
    """
    V = data[:, 0]
    I = data[:, 1]
    A = float(area)
    P_sol = float(light_power)

    Vab = np.absolute(V)
    Iab = np.absolute(I)
    iVabmin = np.argmin(Vab)
    iIabmin = np.argmin(Iab)

    Voc = float(V[iIabmin])
    Jsc = float(-I[iVabmin] / A)

    if iVabmin > iIabmin:
        P = (-V[iIabmin:iVabmin + 1] * I[iIabmin:iVabmin + 1]) / A
        iP0 = iIabmin

    elif iIabmin > iVabmin:
        P = (-V[iVabmin:iIabmin + 1] * I[iVabmin:iIabmin + 1]) / A
        iP0 = iVabmin

    else:
        P = np.array([0, 1])
        iP0 = 0
        print('Error when calculating P (power).')

    iPmax = np.argmax(P)
    Pmax = float(P[iPmax])
    iPmax = int(iPmax + iP0)
    FF = float(Pmax / (Voc * Jsc))
    PCE = float(Pmax / P_sol)

    result = {'PCE': PCE, 'FF': FF, 'iPmax': iPmax, 'Pmax': Pmax,
              'Jsc': Jsc, 'Voc': Voc, 'P_sol': P_sol, 'A': A}

    return result
