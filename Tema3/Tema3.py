import numpy as np
from scipy.linalg import qr as scipy_qr, inv as scipy_inv

# Initialize data
n = 3  # You can change the size of the system
epsilon = 1e-10  # Precision of calculations

# Random initialization of square matrix A and vector s
A = np.random.rand(n, n)
s = np.random.rand(n)

# A = np.array([[0, 0, 4],
#               [1, 2, 3],
#               [0, 1, 2]], dtype=float)
#
#
# s = np.array([3, 2, 1], dtype=float)

A_Copy = A.copy()

print("Matrix A:")
print(A)

# Calculate vector b
b = A @ s

# Householder transformation
def householder(A):
    n = A.shape[0]
    Q = np.identity(n)

    for r in range(n - 1):
        # Construcția matricei Pₚ - constanta β și vectorul u
        sigma = sum([A[i][r] ** 2 for i in range(r, n)])

        if sigma < epsilon:  # Use the same epsilon as defined above
            break

        k = np.sqrt(sigma) if A[r][r] <= 0 else -np.sqrt(sigma)

        beta = sigma - k * A[r][r]
        u = np.zeros(n)
        u[r] = A[r][r] - k

        for i in range(r + 1, n):
            u[i] = A[i][r]

        # A = Pₚ * A
        # Transformarea coloanelor j = r + 1, ..., n
        for j in range(r + 1, n):
            gamma = sum([u[i] * A[i][j] for i in range(r, n)]) / beta
            for i in range(r, n):
                A[i][j] -= gamma * u[i]

        # Transformarea coloanei r matricei A
        A[r][r] = k
        A[r+1:, r] = 0

        # Q = Pₚ * Q
        for j in range(n):
            gamma = sum([u[i] * Q[i][j] for i in range(r, n)]) / beta
            for i in range(r, n):
                Q[i][j] -= gamma * u[i]

    return Q.T, A


Q, R = householder(A_Copy)

# Solve the linear system using QR decomposition from scipy
Q_scipy, R_scipy = scipy_qr(A)
x_scipy = np.linalg.solve(R_scipy, Q_scipy.T @ b)

# Solve the linear system using the QR decomposition calculated at point 2
x_householder = np.linalg.solve(R, Q.T @ b)

# Calculate and display the errors
error_x = np.linalg.norm(x_scipy - x_householder)
error_Ax_init = np.linalg.norm(A @ x_scipy - b)
error_Ax_QR = np.linalg.norm(A @ x_householder - b)
error_x_householder_s = np.linalg.norm(x_householder - s)/np.linalg.norm(s)
error_x_QR_s = np.linalg.norm(x_scipy - s)/np.linalg.norm(s)

print("\nMatrix Q:")
print(Q)

print("\nMatrix R:")
print(R)

print("\nVector b:")
print(b)

A_reconstructed = Q @ R
print("\nErorile sunt:")
print(np.abs(A_reconstructed - A))
print('\n')
assert (np.abs(A_reconstructed - A) < epsilon).all(), "Descompunerea QR a eșuat"

print("\nMatrix x_QR from scipy:")
print(x_scipy)

print("\nMatrix x_Householder:")
print(x_householder)

print("\nError |x_QR - x_Householder|_2: ", error_x)
print("Error |A*x_init - b|_2: ", error_Ax_init)
print("Error |A*x_QR - b|_2: ", error_Ax_QR)
print("Error |x_Householder - s|_2 / s: ", error_x_householder_s)
print("Error |x_QR - s|_2 / s: ", error_x_QR_s)

# Calculate inverse of A using Householder QR decomposition
A_inv_householder = np.linalg.inv(R) @ Q.T

# Calculate inverse of A using library function
A_inv_lib = scipy_inv(A)

# Calculate norm of the difference between two inverses
norm_difference = np.linalg.norm(A_inv_householder - A_inv_lib)

print("\nInverse of A using Householder QR:")
print(A_inv_householder)

print("\nInverse of A using library function:")
print(A_inv_lib)

print("\nNorm of the difference between two inverses: ")
print(norm_difference, "\n")

# Bonus
epsilon_prime = 1e-6

def calculate_limit(A, epsilon_prime):
    k = 0
    A_k = A

    while k<1000:
        Q, R = householder(A_k)
        R[np.tril_indices_from(R, -1)] = 0
        A_k_next = R @ Q

        if np.linalg.norm(A_k_next - A_k) <= epsilon_prime:
            break

        A_k = A_k_next
        k += 1

    print("Stop at k = ", k)
    return A_k_next

A_limit = calculate_limit(A, epsilon_prime)

print("\nLimit matrix A(k+1):")
print(A_limit)