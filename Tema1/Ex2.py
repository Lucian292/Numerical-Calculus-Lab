import random

x = 1.0
y = 1e-15  # u=10^(-15)
z = 1e-15  # u=-10^(-15)

expr1 = (x + y) + z
expr2 = x + (y + z)

print("expresia 1: ", expr1)
print("expresia 2: ", expr2)

if expr1 != expr2:
    print("operatia de adunare este neasociativa")
else:
    print("operatia de adunare este asociativa")

b = 1e-15
c = 1e-15
#a = 1.0
a=random.uniform(b, c)
print(a)
for i in range(0, 325):
    #b = 10**(-i) # i
    #c = 10**(-i) # i
    #print(b, c)
    a *= 10
    if (((a * b) * c) != (a * (b * c))):
        print("expresia 3: ", (a * b) * c)
        print("expresia 4: ", a * (b * c))
        break

if (a * b) * c != a * (b * c):
    print("operatia de inmultire este neasociativa")
else:
    print("operatia de inmultire este asociativa")






