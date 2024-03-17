import numpy as np


# Definirea metodei lui Horner pentru evaluarea unui polinom într-un punct
def horner(poly, x):
    result = poly[0]
    for i in range(1, len(poly)):
        result = result * x + poly[i]
    return result


# Definirea metodei lui Muller pentru găsirea rădăcinilor unui polinom
def muller(poly, eps=1e-6, max_iter=1000):
    # Calcularea intervalului [-R, R]
    R = abs(poly[0]) + max([abs(a) for a in poly[1:]])

    # Generarea valorilor x0, x1, x2 aleatoriu din intervalul [-R, R]
    x0, x1, x2 = np.random.uniform(-R, R, 3)

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
    return x2


# Definirea coeficienților polinomului
poly = [1, -6, 11, -6]

# Apelarea metodei lui Muller pentru a găsi rădăcinile polinomului
root = muller(poly)

# Afișarea rădăcinilor
print("Rădăcina polinomului este:", root)
