"""Linear regression."""

from numpy import polyfit, corrcoef, asarray


def linear_regression(x, y):
    """Linear regression algorithm.

    Equation: y = a*x + b

    :param x: X data (list).
    :param y: Y data (list).
    :return: Regression parameters (a, b) of equation y=ax+b.
    """
    if len(x) != len(y):
        raise ValueError('The length of `x` must be equal to the `y`.')

    x = asarray(list(x))
    y = asarray(list(y))
    coeffs = list(polyfit(x, y, 1))
    r2 = float((corrcoef(x, y)[0, 1])**2)
    a = coeffs[0]
    b = coeffs[1]

    return a, b, r2
