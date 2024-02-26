u = 1

x = 1.0
y = u
z = u

partea_stanga = (x + y) + z
partea_dreapta = x + (y + z)

neasociativitate = partea_stanga != partea_dreapta

if neasociativitate:
    print("(x +_c y) +_c z nu este egal cu x +_c (y +_c z)")
else:
    print("(x +_c y) +_c z este egal cu x +_c (y +_c z)")
