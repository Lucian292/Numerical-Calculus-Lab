def gaseste_precizia_masina():
    m = 0
    while True:
        u = 10**(-m)
        rezultat = 1 + u
        if rezultat != 1:
            return u
        m += 1


precizia_masina = gaseste_precizia_masina()
print(precizia_masina)

# 2.220446049250313e-16