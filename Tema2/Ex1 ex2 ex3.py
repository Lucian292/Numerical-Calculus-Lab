import numpy as np

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def lu_decomposition(A):
    n = len(A)
    L = identity_matrix(n)
    U = [[0] * n for _ in range(n)]

    for i in range(n):
        # Upper Triangular
        for k in range(i, n):
            sum = 0
            for j in range(i):
                sum += L[i][j] * U[j][k]
            U[i][k] = A[i][k] - sum

        # Lower Triangular
        for k in range(i, n):
            if i == k:
                L[i][i] = 1  # diagonal as 1
            else:
                sum = 0
                for j in range(i):
                    sum += L[k][j] * U[j][i]
                L[k][i] = (A[k][i] - sum) / U[i][i]

    return L, U

def forward_substitution(L, b):
    n = len(L)
    y = [0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][j] * y[j] for j in range(i))) / L[i][i]
    return y

def backward_substitution(U, y):
    n = len(U)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def matrix_multiplication(A, B):
    return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]

def inverse_matrix(A):
    n = len(A)
    identity = identity_matrix(n)
    L, U = lu_decomposition(A)
    A_inv = []
    for i in range(n):
        e = [0] * n
        e[i] = 1
        y = forward_substitution(L, e)
        x = backward_substitution(U, y)
        A_inv.append(x)
    return list(zip(*A_inv))

def determinant_LU(L, U):
    det_L = 1
    det_U = 1
    n = len(L)

    for i in range(n):
        det_L *= L[i][i]
        det_U *= U[i][i]

    return det_L * det_U

def calculate_norm(xLU, xlib, Ainv_lib, b_init):
    norm1 = np.linalg.norm(np.dot(A_init, xLU) - b_init)
    norm2 = np.linalg.norm(xLU - np.dot(Ainv_lib, b_init))
    return norm1, norm2

def main():
    global A_init  # Declaram matricea A_init ca globala pentru a putea fi accesata in calculate_norm
    # Date de intrare
    n = 3  # Dimensiunea sistemului
    eps = 1e-9  # Precizia calculelor

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
    L, U = lu_decomposition(A)

    # Calculul determinantului matricei A
    det_A = determinant_LU(L, U)

    # Calculul soluției xLU folosind descompunerea LU și metodele substituției directe și inverse
    y = forward_substitution(L, b)
    xLU = backward_substitution(U, y)

    # Calculul inversului matricei A folosind biblioteca numpy
    A_inv_lib = inverse_matrix(A)

    # Calculul soluției inverse xlib
    xlib = np.dot(A_inv_lib, b)

    # Calculul normelor
    norm1, norm2 = calculate_norm(xLU, xlib, A_inv_lib, b)

    # Afișarea rezultatelor
    print("Descompunerea LU a matricei A:")
    print("L =", L)
    print("U =", U)
    print("\nDeterminantul matricei A:", det_A)
    print("\nSolutia sistemului Ax = b (xLU):", xLU)
    print("\nInversa matricei A (A_inv_lib):", A_inv_lib)
    print("\nNorma ||A_init*xLU - b_init||2:", norm1)
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