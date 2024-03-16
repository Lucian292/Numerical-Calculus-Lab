import numpy as np
from scipy.linalg import qr as scipy_qr, inv as scipy_inv

# Initialize data
n = 3  # You can change the size of the system
epsilon = 1e-10  # Precision of calculations

# Random initialization of square matrix A and vector s
A = np.random.rand(n, n)
s = np.random.rand(n)

print("Matrix A:")
print(A)

# A = np.array([[0, 0, 4],
#               [1, 2, 3],
#               [0, 1, 2]], dtype=float)
#
# s = np.array([3, 2, 1], dtype=float)

# Calculate vector b
b = A @ s

# Householder transformation
def householder(A):
    m, n = A.shape
    Q = np.eye(m)
    R = A.copy()

    for j in range(min(m, n)):
        x = R[j:, j]
        normx = np.linalg.norm(x)
        rho = -np.sign(x[0])
        u1 = x[0] - rho * normx
        if np.abs(u1) < epsilon:  # Add this check
            continue
        u = x / u1
        u[0] = 1

        beta_prevent_zero_division_error = epsilon if (u @ u.T) == 0 else (u @ u.T)

        beta = 2 / (beta_prevent_zero_division_error)

        R[j:, :] -= beta * (u.reshape(-1, 1) @ (u.reshape(1, -1) @ R[j:, :]))

        Q[:, j:] -= beta * (Q[:, j:] @ u.reshape(-1, 1)) @ u.reshape(1, -1)

    return Q, R

Q, R = householder(A)

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

A_reconstructed = Q.dot(R)[:n, :]
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
print(norm_difference)

# Bonus
epsilon_prime = 1e-6


def calculate_limit(A, epsilon_prime):
    k = 0
    A_k = A

    while True:
        Q, R = householder(A_k)
        A_k_next = R @ Q

        if np.linalg.norm(A_k_next - A_k) <= epsilon_prime:
            break

        A_k = A_k_next
        k += 1

    return A_k_next


A_limit = calculate_limit(A, epsilon_prime)

print("\nLimit matrix A(k+1):")
print(A_limit)