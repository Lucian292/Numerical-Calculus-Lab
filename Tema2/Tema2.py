import numpy as np

def print_L(A):
    n = len(A)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            L[i][j] = A[i][j]
    print("L =", L)

def print_U(A):
    n = len(A)
    U = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                U[i][j] = 1  # pe diagonala principala valorile sunt doar 1
            else:
                U[i][j] = A[i][j]
    print("U =", U)

def lu_decomposition(A):
    n = len(A)

    for p in range(n):
        # Calcularea elementelor coloanei p
        for i in range(p, n):
            sum = 0
            for k in range(p):
                sum += A[i][k] * A[k][p]
            A[i][p] = A[i][p] - sum

        # Verificarea dacă elementul de pe diagonala principală este zero
        if abs(A[p][p]) < eps:  # folosim variabila globală eps pentru precizie
            raise ValueError("Descompunerea LU nu este posibilă pentru matricea dată.")

        # Calcularea elementelor liniei p
        for i in range(p + 1, n):
            sum = 0
            for k in range(p):
                sum += A[p][k] * A[k][i]
            A[p][i] = (A[p][i] - sum) / A[p][p]

    return A  # A conține acum atât L (sub diagonala principală), cât și U (pe și deasupra diagonalei principale)


def matrix_multiplication(A, B):
    return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]

def determinant_LU(A):
    n = len(A)
    det_A = 1
    for i in range(n):
        det_A *= A[i][i]
    return det_A

def forward_substitution(A, b):
    n = len(A)
    y = [0] * n
    for i in range(n):
        y[i] = (b[i] - sum(A[i][j] * y[j] for j in range(i))) / A[i][i]
    return y

def backward_substitution(A, y):
    n = len(A)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))
    return x

def inverse_matrix(A):
    n = len(A)
    A_inv = []
    for i in range(n):
        e = [0] * n
        e[i] = 1
        y = forward_substitution(A, e)
        x = backward_substitution(A, y)
        A_inv.append(x)
    return list(zip(*A_inv))

def calculate_norm(xLU, xlib, A_inv_lib, b_init):
    norm1 = np.linalg.norm(np.dot(A_init, xLU) - b_init)
    norm2 = np.linalg.norm(xLU - np.dot(A_inv_lib, b_init))
    norm3 = np.linalg.norm(xLU - xlib)

    return norm1, norm2, norm3


def main():
    global A_init  # Declaram matricea A_init ca globala pentru a putea fi accesata in calculate_norm
    # Date de intrare
    n = 3  # Dimensiunea sistemului
    global eps  # Precizia calculelor
    eps = 1e-9
    # Matricea sistemului A și vectorul termenilor liberi b
    A = [
        [2.5, 2, 2],
        [5, 6, 5],
        [5, 6, 6.5]
    ]
    b = [2, 2, 2]

    # Copierea matricei A pentru a păstra datele inițiale
    A_init = np.copy(A)

    # Descompunerea LU a matricei A
    A = lu_decomposition(A)

    # Calculul determinantului matricei A
    det_A = determinant_LU(A)

    # Calculul soluției xLU folosind descompunerea LU și metodele substituției directe și inverse
    y = forward_substitution(A, b)
    xLU = backward_substitution(A, y)

    # Calculul inversului matricei A folosind biblioteca numpy
    A_inv_lib = inverse_matrix(A)

    # Calculul soluției inverse xlib
    xlib = np.dot(A_inv_lib, b)

    # Calculul normelor
    norm1, norm2, norm3 = calculate_norm(xLU, xlib, A_inv_lib, b)


    # Afișarea rezultatelor
    print("Descompunerea LU a matricei A:")
    print_L(A)
    print_U(A)
    print("\nDeterminantul matricei A:", det_A)
    print("\nSolutia sistemului Ax = b (xLU):", xLU)
    print("\nInversa matricei A (A_inv_lib):", A_inv_lib)
    print("\nNorma ||A_init*xLU - b_init||2:", norm1)
    print("Norma ||xLU - xlib||2:", norm3)
    print("Norma ||xLU - A_inv_lib*b_init||2:", norm2)

if __name__ == "__main__":
    main()

# Mai precis, codul:
#
# Definește o funcție lu_decomposition care calculează descompunerea LU a unei matrici date.
# Definește funcțiile forward_substitution și backward_substitution pentru a rezolva sistemele de ecuații liniare.
# Calculează determinantul matricei A folosind descompunerea LU.
# Calculează soluția sistemului Ax = b folosind descompunerea LU și metodele substituției directe și inverse.
# Calculează inversa matricei A folosind o bibliotecă externă (numpy).
# Calculează și afișează normele specificate.