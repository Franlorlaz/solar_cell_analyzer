
import numpy as np


def save_pv_param(file_name, name, values):
    """A function to save calculated Photo Voltaic Parameters.

    :param file_name: Specifies the file's name where to save results.
    :param name: Name of electrode. Must be equal to the file's name of data
    measured.
    :param values: A tuple with values to write. Must be like:
    (PCE, FF, iPmax, Pmax, Jsc, Voc, P_sol, A).
    :return: None.
    """

    with open(file_name, 'a') as file:
        file.write('%17s     %8.6E   %8.6E   %8.6E   %8.6E   %8.6E   '
                   '%8.6E   %8.6E\n' % (name, values[0], values[1],
                                        values[3], values[4], values[5],
                                        values[6], values[7]
                                        )
                   )


def pv_param(data, area=0.14, light_power=0.1):
    """Calculate Photo Voltaic Parameters from data measured, as FF and PCE.

    :param data: Numpy array with three columns (V, I, t).
    :param area: Cell's area in [cm2].
    :param light_power: Light Power in [W/cm2].
    :return: A tuple like (PCE, FF, iPmax, Pmax, Jsc, Voc, P_sol, A).
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

    return PCE, FF, iPmax, Pmax, Jsc, Voc, P_sol, A
