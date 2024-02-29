import sys

def gaseste_precizia_masina():
    p = 1
    while 1 + 10 ** (-p) != 1:
        p += 1
    return p - 1

precizia_masina = gaseste_precizia_masina()
print(precizia_masina)
