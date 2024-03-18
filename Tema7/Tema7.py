import numpy as np

global dx

def horner(poly, x):
    result = poly[0]
    for i in range(1, len(poly)):
        result = result * x + poly[i]
    return result


def horner_derivative(poly, x):
    n = len(poly) - 1
    result = poly[0] * n
    for i in range(1, n):
        result = result * x + poly[i] * (n - i)
    return result


def newton_n4(poly, eps=1e-6, max_iter=1000):
    R = (abs(poly[0]) + max([abs(a) for a in poly[1:]])) / abs(poly[0])
    x0 = np.random.uniform(-R, R)
    print("x0: ", x0)

    for _ in range(max_iter):
        # calcularea lui y_n și x_{n+1}
        y_n = x0 - horner(poly, x0) / horner_derivative(poly, x0)
        denominator = horner_derivative(poly, x0) * (horner(poly, x0) - horner(poly, y_n))
        if abs(denominator) < eps:
            break  # intrerupe bucla dacă numitorul este prea aproape de zero
        x1 = x0 - (horner(poly, x0) ** 2 + horner(poly, y_n) ** 2) / denominator

        if abs(x1 - x0) < eps:
            return x1

        x0 = x1

    return None


def muller(poly, eps=1e-6, max_iter=1000):
    R = (abs(poly[0]) + max([abs(a) for a in poly[1:]])) / abs(poly[0])
    print("R: ", R)

    x0, x1, x2 = np.random.uniform(-R, R, 3)
    print("x0: ", x0, "x1: ", x1, "x2: ", x2)

    dx = np.inf
    k = 3
    while True:
        h0 = x1 - x0
        h1 = x2 - x1
        d0 = (horner(poly, x1) - horner(poly, x0)) / h0
        d1 = (horner(poly, x2) - horner(poly, x1)) / h1
        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = horner(poly, x2)
        if b ** 2 - 4 * a * c < 0:
            break
        if abs(b + np.sign(b) * np.sqrt(b ** 2 - 4 * a * c)) < eps:
            break
        dx = -2 * c / (b + np.sign(b) * np.sqrt(b ** 2 - 4 * a * c))
        x3 = x2 + dx
        if abs(dx) < eps or k > max_iter or abs(x3) > 1e8:
            break
        x0, x1, x2 = x1, x2, x3
        k += 1

    if abs(dx) < eps:
        return x2
    else:
        return None

poly = [1, -6, 11, -6]

root = muller(poly)

if root is not None:
    print("Radacina polinomului este:", root)
else:
    print("Algoritmul nu a convergat.")



root = newton_n4(poly)

if root is not None:
    print("Radacina polinomului este:", root)
else:
    print("Algoritmul nu a convergat.")