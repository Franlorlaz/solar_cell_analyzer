"""Managing PhotoVolatic parameters."""

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

    file_name = Path(file_name).resolve()
    with open(file_name, 'a') as file:
        file.write('%17s     %8.6E   %8.6E   %8.6E   %8.6E   %8.6E   %8.6E'
                   '   %8.6E\n' % (name, PCE, FF, Pmax, Jsc, Voc, P_sol, A))


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

    Voc = V[iIabmin]
    Jsc = -I[iVabmin] / A

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
    Pmax = P[iPmax]
    iPmax = iPmax + iP0
    FF = Pmax / (Voc * Jsc)
    PCE = Pmax / P_sol

    result = {'PCE': PCE, 'FF': FF, 'iPmax': iPmax, 'Pmax': Pmax,
              'Jsc': Jsc, 'Voc': Voc, 'P_sol': P_sol, 'A': A}

    return result
