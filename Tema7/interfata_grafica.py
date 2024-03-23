import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np


def horner(poly, x):
    result = poly[0]
    for i in range(1, len(poly)):
        result = result * x + poly[i]
    return result


def horner_derivative(poly, x):
    n = len(poly) - 1
    result = poly[0] * n
    for i in range(1, n):
        result = result * x + poly[i] * (n - i)
    return result


def newton_n4(poly, eps=1e-6, max_iter=1000):
    R = (abs(poly[0]) + max([abs(a) for a in poly[1:]])) / abs(poly[0])
    x0 = np.random.uniform(-R, R)
    log_text.insert(tk.END, f"x0: {x0}\n")

    for _ in range(max_iter):
        y_n = x0 - horner(poly, x0) / horner_derivative(poly, x0)
        denominator = horner_derivative(poly, x0) * (horner(poly, x0) - horner(poly, y_n))
        if abs(denominator) < eps:
            break
        x1 = x0 - (horner(poly, x0) ** 2 + horner(poly, y_n) ** 2) / denominator

        if abs(x1 - x0) < eps:
            return x1

        x0 = x1

    log_text.insert(tk.END, "Algoritmul nu a convergat.\n")
    return None


def muller(poly, eps=1e-6, max_iter=1000):
    R = (abs(poly[0]) + max([abs(a) for a in poly[1:]])) / abs(poly[0])

    x0, x1, x2 = np.random.uniform(-R, R, 3)
    log_text.insert(tk.END, f"R: {R}\n")
    log_text.insert(tk.END, f"x0: {x0}, x1: {x1}, x2: {x2}\n")

    dx = np.inf
    k = 3
    while True:
        h0 = x1 - x0
        h1 = x2 - x1
        d0 = (horner(poly, x1) - horner(poly, x0)) / h0
        d1 = (horner(poly, x2) - horner(poly, x1)) / h1
        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = horner(poly, x2)
        if b ** 2 - 4 * a * c < 0:
            break
        if abs(b + np.sign(b) * np.sqrt(b ** 2 - 4 * a * c)) < eps:
            break
        dx = -2 * c / (b + np.sign(b) * np.sqrt(b ** 2 - 4 * a * c))
        x3 = x2 + dx
        if abs(dx) < eps or k > max_iter or abs(x3) > 1e8:
            break
        x0, x1, x2 = x1, x2, x3
        k += 1

    if abs(dx) < eps:
        return x2
    else:
        log_text.insert(tk.END, "Algoritmul nu a convergat.\n")
        return None


def calculate():
    poly_str = poly_entry.get()
    try:
        poly = [float(x) for x in poly_str.split(',')]
        root_muller = muller(poly)
        root_newton = newton_n4(poly)
        if root_muller is not None:
            result_muller_label.config(text=f"Radacina polinomului (Muller): {root_muller}")
        else:
            result_muller_label.config(text="Algoritmul Muller nu a convergat.")

        if root_newton is not None:
            result_newton_label.config(text=f"Radacina polinomului (Newton): {root_newton}")
        else:
            result_newton_label.config(text="Algoritmul Newton nu a convergat.")
    except ValueError:
        messagebox.showerror("Eroare", "Introduceti coeficientii polinomului corect!")


# Creare fereastra principala
root = tk.Tk()
root.title("Calculator de radacini polinomiale")

# Creare frame pentru input
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10)

label = tk.Label(root, text="Ex: 1, -6, 11, -6")
label.pack()

poly_label = ttk.Label(input_frame, text="Introduceti coeficientii polinomului (separati cu virgula):")
poly_label.grid(row=0, column=0, padx=5, pady=5)

poly_entry = ttk.Entry(input_frame, width=50)
poly_entry.grid(row=0, column=1, padx=5, pady=5)

calculate_button = ttk.Button(input_frame, text="Calculare", command=calculate)
calculate_button.grid(row=1, column=0, columnspan=2, pady=5)

# Creare frame pentru output
output_frame = ttk.Frame(root)
output_frame.pack(padx=10, pady=10)

result_muller_label = ttk.Label(output_frame, text="")
result_muller_label.grid(row=0, column=0, padx=5, pady=5)

result_newton_label = ttk.Label(output_frame, text="")
result_newton_label.grid(row=1, column=0, padx=5, pady=5)

# Creare caseta de text pentru log-uri
log_frame = ttk.Frame(root)
log_frame.pack(padx=10, pady=10)

log_label = ttk.Label(log_frame, text="Loguri:")
log_label.grid(row=0, column=0, padx=5, pady=5)

log_text = tk.Text(log_frame, height=10, width=50)
log_text.grid(row=1, column=0, padx=5, pady=5)

root.mainloop()
