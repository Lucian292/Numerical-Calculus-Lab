import numpy as np

def print_L(L):
    n = int((len(L) * 2) ** 0.5)
    for i in range(n):
        for j in range(n):
            if j > i:
                print("0", end="\t")
            else:
                print(L[i * (i + 1) // 2 + j], end="\t")
        print()

def print_U(U):
    n = int((len(U) * 2) ** 0.5)
    for i in range(n):
        for j in range(n):
            if j < i:
                print("0", end="\t")
            else:
                print(U[i * (i + 1) // 2 + j], end="\t")
        print()

def lu_decomposition(A):
    n = len(A)
    L = [0] * (n * (n + 1) // 2)  # Vector pentru matricea L
    U = [0] * (n * (n + 1) // 2)  # Vector pentru matricea U
    idx = 0  # Indicele pentru vectorii L și U

    for j in range(n):
        for i in range(j, n):
            sum_ = 0
            for k in range(j):
                sum_ += L[i * (i + 1) // 2 + k] * U[k * (k + 1) // 2 + j]
            U[i * (i + 1) // 2 + j] = A[i][j] - sum_

        for i in range(j + 1, n):
            sum_ = 0
            for k in range(j):
                sum_ += L[j * (j + 1) // 2 + k] * U[k * (k + 1) // 2 + i]
            if U[j * (j + 1) // 2 + j] == 0:
                raise ValueError("Descompunerea LU nu este posibila pentru matricea data.")
            L[i * (i + 1) // 2 + j] = (A[i][j] - sum_) / U[j * (j + 1) // 2 + j]

    print("Matricea U înainte de apariția erorii:")
    print_U(U)

    return L, U

def forward_substitution(L, b):
    n = int((len(L) * 2) ** 0.5)
    y = [0] * n
    for i in range(n):
        sum_ = sum(L[i * (i + 1) // 2 + j] * y[j] for j in range(i))
        if L[i * (i + 1) // 2 + i] == 0:
            raise ValueError("Descompunerea LU nu este posibila pentru matricea data.")
        y[i] = (b[i] - sum_) / L[i * (i + 1) // 2 + i]
    return y

def backward_substitution(U, y):
    n = int((len(U) * 2) ** 0.5)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i] - sum(U[i * (i + 1) // 2 + j] * x[j] for j in range(i + 1, n))
        x[i] /= U[i * (i + 1) // 2 + i]
    return x

def main():
    A = [
        [1, 2, 1, 1],
        [1, 4, -1, 7],
        [4, 9, 5, 11],
        [1, 0, 6, 4]
    ]
    b = [0, 20, 18, 1]

    L, U = lu_decomposition(A)

    y = forward_substitution(L, b)
    xLU = backward_substitution(U, y)

    print("Matricea L:")
    print_L(L)
    print("\nMatricea U:")
    print_U(U)
    print("\nSolutia sistemului Ax = b (xLU):", xLU)

if __name__ == "__main__":
    main()
