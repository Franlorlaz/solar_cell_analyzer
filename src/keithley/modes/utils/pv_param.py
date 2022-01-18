"""Managing PhotoVolatic parameters."""

import os
import csv
import datetime
import numpy as np

from pathlib import Path


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

    now = datetime.datetime.now()
    row = {'file': name,
           'PCE': PCE,
           'FF': FF,
           'Pmax(W/cm2)': Pmax,
           'Jsc(A/cm2)': Jsc,
           'Voc(V)': Voc,
           'P_sol(W/cm2)': P_sol,
           'area(cm2)': A,
           'datetime': str(now),
           'delta_time(min)': 0}

    file_name = Path(file_name).resolve()
    extension = file_name.suffix
    items = []
    if extension == '.csv' and os.path.exists(file_name):
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for item in reader:
                items.append(item)
    degrad0time_path = Path(__file__ + '/../../../../config/tmp/DegradationZeroTime.txt')
    with open(degrad0time_path.resolve(), 'r') as f:
        previous_time = f.read()
    if not previous_time == "0":
        previous_time = datetime.datetime.strptime(previous_time,
                                                   '%Y-%m-%d %H:%M:%S.%f')
        delta_time = (now - previous_time).total_seconds()
        row['delta_time(min)'] = delta_time/60

    with open(file_name, 'a') as file:
        if extension == '.txt':
            file.write('%17s     %8.6E   %8.6E   %8.6E   %8.6E   %8.6E   %8.6E'
                       '   %8.6E\n' % (name, PCE, FF, Pmax,
                                       Jsc, Voc, P_sol, A))
        elif extension == '.csv':
            writer = csv.DictWriter(file, fieldnames=tuple(row.keys()))
            writer.writerow(row)


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
    Vmax = float(V[iPmax])

    result = {'PCE': PCE, 'FF': FF, 'iPmax': iPmax, 'Pmax': Pmax,
              'Jsc': Jsc, 'Voc': Voc, 'P_sol': P_sol, 'A': A, 'Vmax': Vmax}

    return result
