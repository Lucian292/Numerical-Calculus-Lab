import numpy as np

# Implementarea algoritmului de descompunere LU
def descompunere_LU(A):
    n = len(A)
    L = np.eye(n)  # Matricea L începe ca identitatea
    U = np.zeros((n, n))

    for i in range(n):
        # Calculăm elementele matricei U
        for j in range(i, n):
            suma = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - suma

        # Calculăm elementele matricei L
        for j in range(i+1, n):
            suma = sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = (A[j][i] - suma) / U[i][i]

    return L, U

# Funcția de rezolvare a sistemului inferior triunghiular Ly = b
def solve_lower_triangular(L, b):
    n = len(L)
    y = np.zeros(n)

    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

    return y

# Funcția de rezolvare a sistemului superior triunghiular Ux = y
def solve_upper_triangular(U, y):
    n = len(U)
    x = np.zeros(n)

    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]

    return x

# Rezolvăm sistemul Ax = b folosind descompunerea LU
def solve_LU(L, U, b):
    y = solve_lower_triangular(L, b)
    x = solve_upper_triangular(U, y)
    return x


# Funcția de calcul a inversului unei matrice
def inverse_matrix(A):
    n = len(A)
    L, U = descompunere_LU(A)

    # Calculăm inversa matricei A rezolvând n sisteme liniare
    inv_A = np.zeros((n, n))
    for i in range(n):
        b = np.zeros(n)
        b[i] = 1
        inv_A[:, i] = solve_LU(L, U, b)

    return inv_A

# Citim dimensiunea sistemului și precizia calculelor
n = int(input("Introduceți dimensiunea sistemului: "))
precizie = float(input("Introduceți precizia calculelor: "))

# Generăm matricea A și vectorul b
A_init = np.random.rand(n, n)
b_init = np.random.rand(n)

# Păstrăm o copie a matricei A inițiale pentru a verifica eroarea mai târziu
A = np.copy(A_init)
b = np.copy(b_init)

# Descompunem matricea A în L și U
L, U = descompunere_LU(A)

# Calculăm determinantul matricei A
det_A = np.linalg.det(A)
det_LU = np.prod(np.diag(U))  # Produsul elementelor de pe diagonala lui U

# Verificăm dacă determinanta este nenulă
if abs(det_A) < precizie:
    print("Determinanta matricei A este foarte mică sau zero. Imposibil de continuat.")
else:
    print("Determinantul matricei A:", det_A)
    print("Determinantul matricei LU:", det_LU)

    # Calculăm soluția sistemului Ax = b folosind descompunerea LU
    x_LU = solve_LU(L, U, b)

    # Calculăm inversa matricei A
    inv_A = inverse_matrix(A)

    # Calculăm eroarea ||x_LU - x_init||_2
    eroare_x = np.linalg.norm(x_LU - np.linalg.solve(A_init, b_init))

    # Calculăm eroarea ||x_LU - A_inv * b_init||_2
    eroare_inv = np.linalg.norm(x_LU - np.dot(inv_A, b_init))

    print("Eroarea ||x_LU - x_init||_2:", eroare_x)
    print("Eroarea ||x_LU - A_inv * b_init||_2:", eroare_inv)
