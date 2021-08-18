"""Linear regression."""


def linear_regression(x, y):
    """Linear regression algorithm.

    Equation: y = a*x + b

    :param x: X data (list).
    :param y: Y data (list).
    :return: Regression parameters (a, b) of equation y=ax+b.
    """

    if len(x) == len(y):
        data = list(zip(x, y))
    else:
        raise ValueError('The length of `x` must be equal to the `y`.')

    x = list(x)
    y = list(y)
    xy = []
    xx = []
    yy = []
    for i in data:
        xy.append(i[0] * i[1])
        xx.append(i[0] ** 2)
        yy.append(i[1] ** 2)

    a = len(x) * sum(xy) - sum(x) * sum(y)
    a /= len(x) * sum(xx) - sum(x) ** 2

    b = sum(y) - sum(x)
    b /= len(x)

    return a, b
