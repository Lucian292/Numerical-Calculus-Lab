# Pentru adunare
x = 1.0
y = 1e-16  # Valoare mică, pozitivă
z = -1e-16  # Valoare mică, negativă

# Verificăm neasociativitatea adunării
expr1 = (x + y) + z
expr2 = x + (y + z)

print("Expresia 1: ", expr1)
print("Expresia 2: ", expr2)

if expr1 != expr2:
    print("Operația de adunare este neasociativă.")
else:
    print("Operația de adunare este asociativă.")

# Pentru înmulțire
a = 1.0
b = 10**16
c = 10**-16

# Verificăm neasociativitatea înmulțirii
expr3 = (a * b) * c
expr4 = a * (b * c)

print("Expresia 3: ", expr3)
print("Expresia 4: ", expr4)

if expr3 != expr4:
    print("Operația de înmulțire este neasociativă.")
else:
    print("Operația de înmulțire este asociativă.")






