import tkinter as tk
from tkinter import scrolledtext
import numpy as np

def create_entries():
    global matrix_entries, vector_b_entries

    # Șterge intrările vechi, dacă există
    if matrix_entries:
        for row in matrix_entries:
            for entry in row:
                entry.destroy()
        for entry in vector_b_entries:
            entry.destroy()
        matrix_entries.clear()
        vector_b_entries.clear()

    try:
        # Citirea dimensiunii matricei
        matrix_size = int(matrix_size_entry.get())

        # Crearea intrărilor pentru matrice și vectorul b
        for i in range(matrix_size):
            row_entries = []
            for j in range(matrix_size):
                entry = tk.Entry(matrix_frame, width=5)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            matrix_entries.append(row_entries)

            # Intrările pentru vectorul b
            b_entry = tk.Entry(vector_b_frame, width=5)
            b_entry.grid(row=i, column=0)
            vector_b_entries.append(b_entry)

    except ValueError:
        pass

def print_L(A):
    n = len(A)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            L[i][j] = A[i][j]
    return L

def print_U(A):
    n = len(A)
    U = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                U[i][j] = 1
            else:
                U[i][j] = A[i][j]
    return U

def lu_decomposition(A):
    n = len(A)
    eps = 1e-9

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

def calculate_norm(xLU, xlib, A_init, b_init):
    norm1 = np.linalg.norm(np.dot(A_init, xLU) - b_init)
    norm2 = np.linalg.norm(xLU - np.dot(inverse_matrix(A_init), b_init))
    norm3 = np.linalg.norm(xLU - xlib)

    return norm1, norm2, norm3

def run_code():
    text_area.delete('1.0', tk.END)

    # Obținerea valorilor matricei și a vectorului coloană b din câmpurile de intrare de text
    matrix_values = [[float(entry.get()) for entry in matrix_entries_row] for matrix_entries_row in matrix_entries]
    vector_b_values = [float(entry.get()) for entry in vector_b_entries]

    A = np.array(matrix_values)
    b = np.array(vector_b_values)

    A_init = np.copy(A)

    A = lu_decomposition(A)

    det_A = determinant_LU(A)

    y = forward_substitution(A, b)
    xLU = backward_substitution(A, y)

    A_inv_lib = inverse_matrix(A_init)

    # calculul solutiei inverse xlib
    xlib = np.dot(A_inv_lib, b)

    norm1, norm2, norm3 = calculate_norm(xLU, xlib, A_init, b)

    text_area.insert(tk.END, "Descompunerea LU a matricei A:\n")
    text_area.insert(tk.END, f"L = {print_L(A)}\n")
    text_area.insert(tk.END, f"U = {print_U(A)}\n")
    text_area.insert(tk.END, f"\nDeterminantul matricei A: {det_A}\n")
    text_area.insert(tk.END, f"\nSolutia sistemului Ax = b (xLU): {xLU}\n")
    text_area.insert(tk.END, f"\nInversa matricei A (A_inv_lib):\n{A_inv_lib}\n")
    text_area.insert(tk.END, f"\nNorma ||A_init*xLU - b_init||2: {norm1}\n")
    text_area.insert(tk.END, f"Norma ||xLU - xlib||2: {norm3}\n")
    text_area.insert(tk.END, f"Norma ||xLU - A_inv_lib*b_init||2: {norm2}\n")

# Crearea interfeței grafice
root = tk.Tk()
root.title("LU Decomposition")

# Frame pentru introducerea dimensiunii matricei
matrix_size_frame = tk.Frame(root)
matrix_size_frame.pack()

# Label pentru introducerea dimensiunii matricei
matrix_size_label = tk.Label(matrix_size_frame, text="Dimensiune Matrice:")
matrix_size_label.grid(row=0, column=0)

# Input pentru introducerea dimensiunii matricei
matrix_size_entry = tk.Entry(matrix_size_frame)
matrix_size_entry.grid(row=0, column=1)

# Buton pentru crearea intrărilor matricei și a vectorului b
create_entries_button = tk.Button(matrix_size_frame, text="Crează intrări", command=create_entries)
create_entries_button.grid(row=0, column=2)

# Frame
matrix_frame = tk.Frame(root)
matrix_frame.pack()

# Frame pentru vectorul coloană b
vector_b_frame = tk.Frame(root)
vector_b_frame.pack()

# Buton pentru rularea codului
run_button = tk.Button(root, text="Rulează codul", command=run_code)
run_button.pack()

# Text area pentru afișarea rezultatelor
text_area = scrolledtext.ScrolledText(root, width=60, height=20)
text_area.pack()

# Listele pentru intrările matricei și vectorului b
matrix_entries = []
vector_b_entries = []

root.mainloop()
