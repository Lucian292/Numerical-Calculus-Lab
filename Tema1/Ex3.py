import math
import random

# definirea functiilor rationale T(i, a)
def T4(x, a):
    return x * (a[0] + x**2 * (a[1] + x**2 * (a[2] + x**2 * a[3])))

def T5(x, a):
    return (a[0] + x**2 * (a[1] + x**2 * (a[2] + x**2 * a[3]))) / (1 + x**2 * (a[4] + x**2 * a[5]))

def T6(x, a):
    return x * (a[0] + x**2 * (a[1] + x**2 * a[2])) / (1 + x**2 * (a[3] + x**2 * (a[4] + x**2 * a[5])))

def T7(x, a):
    return (a[0] + x**2 * (a[1] + x**2 * a[2])) / (1 + x**2 * (a[3] + x**2 * a[4] * x**2 * a[5]))

def T8(x, a):
    return (a[0] + x**2 * a[1]) / (1 + x**2 * (a[2] + x**2 * (a[3] + x**2 * a[4])))

def T9(x, a):
    return (a[0] + x**2 * (a[1] + x**2 * a[2])) / (1 + x**2 * (a[3] + x**2 * (a[4] + x**2 * a[5])))

# definirea functiei tangenta exacte
def tan_exact(x):
    return math.tan(x)

# generarea a 10.000 de numere aleatoare in intervalul [-pi/2, pi/2]
numere_aleatoare = [random.uniform(-math.pi/2, math.pi/2) for _ in range(10000)]

# definirea coeficientilor pentru cele 6 funcții T(i, a)
coefficient_sets = {
    4: [0.0, 1.0/3, 0.0, -1.0/45],
    5: [0.0, 1.0/3, 0.0, -1.0/45, 2.0/15, 0.0],
    6: [0.0, 1.0/3, 0.0, -1.0/45, 0.0, 1.0/315],
    7: [0.0, 1.0/3, 0.0, -1.0/45, 0.0, 1.0/315],
    8: [0.0, 1.0/3, 0.0, -1.0/45, 0.0],
    9: [0.0, 1.0/3, 0.0, -1.0/45, 0.0, 1.0/315]
}

# Calculul valorilor funcțiilor și determinarea celor mai bune aproximări pentru fiecare număr generat
rezultate = {}
for x in numere_aleatoare:
    aproximatii = {}
    for i in range(4, 10):
        func = globals()['T{}'.format(i)]
        approx_value = func(x, coefficient_sets[i])
        error = abs(approx_value - tan_exact(x))
        aproximatii[i] = error
    sorted_aproximatii = sorted(aproximatii.items(), key=lambda kv: kv[1])
    rezultate[x] = [sorted_aproximatii[0][0], sorted_aproximatii[1][0], sorted_aproximatii[2][0]]

# Determinarea frecvenței celor mai bune aproximări pentru fiecare funcție
frecventa = {i: [0, 0, 0] for i in range(4, 10)}
for _, approximations in rezultate.items():
    for i, approx in enumerate(approximations):
        frecventa[approx][i] += 1

# Afișarea ierarhiei funcțiilor
print("Ierarhia funcțiilor:")
for i in range(4, 10):
    print(f"T{i}: {frecventa[i]}")
