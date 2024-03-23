import numpy as np
from scipy.linalg import qr as scipy_qr, inv as scipy_inv
import tkinter as tk
from tkinter import scrolledtext

n = 3
epsilon = 1e-10

class QRInterface:
    def __init__(self, master):
        self.master = master
        master.title("QR Decomposition")

        self.text_area = scrolledtext.ScrolledText(master, width=60, height=20)
        self.text_area.pack(expand=True, fill='both')

        self.run_button = tk.Button(master, text="Run QR Decomposition", command=self.run_qr)
        self.run_button.pack()

    def run_qr(self):
        A = np.random.rand(n, n)
        s = np.random.rand(n)
        # A = np.array([[1, 0, 0],
        #               [0, 2, 0],
        #               [0, 0, 3]], dtype=float)
        #
        # s = np.array([3, 2, 1], dtype=float)
        A_Copy = A.copy()

        Q, R = self.householder(A_Copy)
        Q_scipy, R_scipy = scipy_qr(A)
        x_scipy = np.linalg.solve(R_scipy, Q_scipy.T @ (A @ s))
        x_householder = np.linalg.solve(R, Q.T @ (A @ s))
        error_x = np.linalg.norm(x_scipy - x_householder)

        self.text_area.insert(tk.END, "Matrix A:\n" + str(A) + "\n\n")
        self.text_area.insert(tk.END, "Matrix Q:\n" + str(Q) + "\n\n")
        self.text_area.insert(tk.END, "Matrix R:\n" + str(R) + "\n\n")
        self.text_area.insert(tk.END, "Vector b:\n" + str(A @ s) + "\n\n")
        self.text_area.insert(tk.END, "Matrix x_QR din scipy:\n" + str(x_scipy) + "\n\n")
        self.text_area.insert(tk.END, "Matrix x_Householder:\n" + str(x_householder) + "\n\n")
        self.text_area.insert(tk.END, "Error |x_QR - x_Householder|_2: " + str(error_x) + "\n\n")

        A_reconstructed = Q @ R
        self.text_area.insert(tk.END, "Errors:\n" + str(np.abs(A_reconstructed - A)) + "\n\n")
        assert (np.abs(A_reconstructed - A) < epsilon).all(), "Descompunerea QR a esuat"

        A_inv_householder = np.linalg.inv(R) @ Q.T
        A_inv_lib = scipy_inv(A)
        norm_difference = np.linalg.norm(A_inv_householder - A_inv_lib)

        self.text_area.insert(tk.END, "Inversa lui A folosind Householder QR:\n" + str(A_inv_householder) + "\n\n")
        self.text_area.insert(tk.END, "Inversa lui A din bibliotecă:\n" + str(A_inv_lib) + "\n\n")
        self.text_area.insert(tk.END, "Eroarea dintre cele 2 metode de a calcula inversa:\n" + str(norm_difference) + "\n\n")

        epsilon_prime = 1e-6
        A_limit = self.calculate_limit(A, epsilon_prime)
        self.text_area.insert(tk.END, "Limita matricei A(k+1):\n" + str(A_limit) + "\n\n")

    def householder(self, A):
        n = A.shape[0]
        Q = np.identity(n)

        for r in range(n - 1):
            sigma = sum([A[i][r] ** 2 for i in range(r, n)])
            if sigma < epsilon:
                break

            k = np.sqrt(sigma) if A[r][r] <= 0 else -np.sqrt(sigma)
            beta = sigma - k * A[r][r]
            u = np.zeros(n)
            u[r] = A[r][r] - k

            for i in range(r + 1, n):
                u[i] = A[i][r]

            for j in range(r + 1, n):
                gamma = sum([u[i] * A[i][j] for i in range(r, n)]) / beta
                for i in range(r, n):
                    A[i][j] -= gamma * u[i]

            A[r][r] = k
            A[r+1:, r] = 0

            for j in range(n):
                gamma = sum([u[i] * Q[i][j] for i in range(r, n)]) / beta
                for i in range(r, n):
                    Q[i][j] -= gamma * u[i]

        return Q.T, A

    def calculate_limit(self, A, epsilon_prime):
        k = 0
        A_k = A

        while k < 1000:
            Q, R = self.householder(A_k)
            R[np.tril_indices_from(R, -1)] = 0
            A_k_next = R @ Q

            if np.linalg.norm(A_k_next - A_k) <= epsilon_prime:
                break

            A_k = A_k_next
            k += 1

        self.text_area.insert(tk.END, "Iterat pana la k = " + str(k) + "\n")
        return A_k_next

def main():
    root = tk.Tk()
    my_interface = QRInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
