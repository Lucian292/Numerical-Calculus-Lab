import math
import random

def T4(a):
    return (105*a - 10*(a**3))/(105 - 45*(a**2) + a**4)

def T5(a):
    return (945*a - 105*(a**3) + a**5)/(945 - 420*(a**2) + 15*(a**4))

def T6(a):
    return (10395*a - 1260*(a**3) + 21*(a**5))/(10395 - 4725*(a**2) + 210*(a**4) - a**6)

def T7(a):
    return (135135*a - 17325*(a**3) + 378*(a**5) - a**7)/(135135 - 62370*(a**2) + 3150*(a**4) - 28*(a**6))

def T8(a):
    return (2027025*a - 270270*(a**3) + 6930*(a**5) - 36*(a**7))/(2027025 - 945945*(a**2) + 51975*(a**4) - 630*(a**6) + a**8)

def T9(a):
    return (34459425*a - 4729725*(a**3) + 135135*(a**5) - 990*(a**7) + a**9)/(34459425 - 16216200*(a**2) + 945945*(a**4) - 13860*(a**6) + 45*(a**8))

def S(n, a):
    T = globals()[f"T{n}"]
    return T(a) / math.sqrt(1 + T(a)**2)

def C(n, a):
    T = globals()[f"T{n}"]
    return 1 / math.sqrt(1 + T(a)**2)

random_numbers = [random.uniform(-math.pi/2, math.pi/2) for _ in range(10000)]

# calculul valorilor exacte ale funcеiilor tangent sinus cosinus
exact_values_tan = [math.tan(x) for x in random_numbers]
exact_values_sin = [math.sin(x) for x in random_numbers]
exact_values_cos = [math.cos(x) for x in random_numbers]

# calculul valorilor aproximarilor si erorilor pentru tangent
approximation_functions_tan = [T4, T5, T6, T7, T8, T9]
errors_tan = [[] for _ in range(6)]

for func_index, func in enumerate(approximation_functions_tan):
    for a, v_exact in zip(random_numbers, exact_values_tan):
        error = abs(func(a) - v_exact)
        errors_tan[func_index].append(error)

        # retine cea mai mica eroare pentru fiecare functie de aproximare tangent
        if len(errors_tan[func_index]) == 1 or error < min(errors_tan[func_index]):
            min_error = error

    print(f"cea mai mică eroare pentru T{func_index + 4}: {min_error}")

# identificarea celor mai mici trei erori pentru fiecare numar generat pentru tangent
top_three_indices_tan = [sorted(range(len(errors_tan)), key=lambda i: errors_tan[i][j])[:3] for j in range(10000)]

# calcularea frecventei aparitiilor functiilor in topurile cu cele mai mici erori pentru tangent
frequency_count_tan = {i: [0] * 6 for i in range(10000)}

for i, indices in enumerate(top_three_indices_tan):
    for index in indices:
        frequency_count_tan[i][index] += 1

# ierarhizarea functiilor in functie de frecvenaa lor in topurile cu cele mai mici erori pentru tangent
function_ranking_tan = sorted(range(6), key=lambda i: sum(frequency_count_tan[j][i] for j in range(10000)), reverse=True)

print("Ierarhia funcțiilor pentru tangentă:")
for i, func_index in enumerate(function_ranking_tan):
    print(f"{i+1}. T{func_index + 4}")

# identificarea celor mai mici trei erori pentru fiecare numar generat pentru sinus si cosinus
errors_sin = []
errors_cos = []

for a, v_exact_sin, v_exact_cos in zip(random_numbers, exact_values_sin, exact_values_cos):
    errors_sin.append([abs(S(n, a) - v_exact_sin) for n in range(4, 10)])
    errors_cos.append([abs(C(n, a) - v_exact_cos) for n in range(4, 10)])

# identificarea celor mai mici trei erori pentru sinus
top_three_indices_sin = [sorted(range(6), key=lambda i: errors_sin[j][i])[:3] for j in range(10000)]

# identificarea celor mai mici trei erori pentru cosinus
top_three_indices_cos = [sorted(range(6), key=lambda i: errors_cos[j][i])[:3] for j in range(10000)]

# calcularea frecventei aparitiilor funcțiilor in topurile cu cele mai mici erori pentru sinus și cosinus
frequency_count_sin = {i: [0] * 6 for i in range(10000)}
frequency_count_cos = {i: [0] * 6 for i in range(10000)}

for i, indices in enumerate(top_three_indices_sin):
    for index in indices:
        frequency_count_sin[i][index] += 1

for i, indices in enumerate(top_three_indices_cos):
    for index in indices:
        frequency_count_cos[i][index] += 1

# ierarhizarea functiilor in functie de frecvența lor în topurile cu cele mai mici erori pentru sinus
function_ranking_sin = sorted(range(6), key=lambda i: sum(frequency_count_sin[j][i] for j in range(10000)), reverse=True)

# ierarhizarea functiilor in functie de frecventa lor in topurile cu cele mai mici erori pentru cosinus
function_ranking_cos = sorted(range(6), key=lambda i: sum(frequency_count_cos[j][i] for j in range(10000)), reverse=True)

print("\nIerarhia funcțiilor pentru sinus:")
for i, func_index in enumerate(function_ranking_sin):
    print(f"{i+1}. S{func_index + 4}")

print("\nIerarhia funcțiilor pentru cosinus:")
for i, func_index in enumerate(function_ranking_cos):
    print(f"{i+1}. C{func_index + 4}")

