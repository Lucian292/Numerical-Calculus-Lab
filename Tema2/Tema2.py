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
                U[i][j] = 1
            else:
                U[i][j] = A[i][j]
    print("U =", U)

def lu_decomposition(A):
    n = len(A)

    for p in range(n):
        # calcularea elementelor coloanei p
        for i in range(p, n):
            sum = 0
            for k in range(p):
                sum += A[i][k] * A[k][p]
            A[i][p] = A[i][p] - sum

        # verificarea dacă elementul de pe diagonala principală este zero
        if abs(A[p][p]) < eps:
            raise ValueError("descompunerea LU nu este posibila pentru matricea data")

        # calcularea elementelor liniei p
        for i in range(p + 1, n):
            sum = 0
            for k in range(p):
                sum += A[p][k] * A[k][i]
            A[p][i] = (A[p][i] - sum) / A[p][p]

    return A

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
    return np.linalg.inv(A)

def calculate_norm(xLU, xlib, A_inv_lib, b_init):
    norm1 = np.linalg.norm(np.dot(A_init, xLU) - b_init)
    norm2 = np.linalg.norm(xLU - np.dot(A_inv_lib, b_init))
    norm3 = np.linalg.norm(xLU - xlib)

    return norm1, norm2, norm3


def main():
    global A_init
    global eps
    eps = 1e-9
    A = [
        [2.5, 2, 2],
        [5, 6, 5],
        [5, 6, 6.5]
    ]
    b = [2, 2, 2]

    A_init = np.copy(A)

    A = lu_decomposition(A)

    det_A = determinant_LU(A)

    y = forward_substitution(A, b)
    xLU = backward_substitution(A, y)

    A_inv_lib = inverse_matrix(A_init)

    # calculul solutiei inverse xlib
    xlib = np.dot(A_inv_lib, b)

    norm1, norm2, norm3 = calculate_norm(xLU, xlib, A_inv_lib, b)

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