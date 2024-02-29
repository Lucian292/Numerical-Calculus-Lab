import sys

def gaseste_precizia_masina():
    epsilon = sys.float_info.epsilon
    p = 1
    while 10**(-p) > epsilon:
        p += 1
    return p - 1

precizia_masina = gaseste_precizia_masina()
print(precizia_masina)
