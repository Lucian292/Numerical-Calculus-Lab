import numpy as np
import warnings
import tkinter as tk
from tkinter import ttk


# metoda analitica
def gradient_descent(F, dF, x_init, y_init, learning_rate, precision, max_iters):
    x, y = x_init, y_init
    x_new, y_new = x, y
    for i in range(max_iters):
        grad_x, grad_y = dF(x, y)
        x_new = x - learning_rate * grad_x
        y_new = y - learning_rate * grad_y
        if np.sqrt((x_new - x)**2 + (y_new - y)**2) <= precision:
            break
        x, y = x_new, y_new
    try:
        if np.sqrt((x_new - x) ** 2 + (y_new - y) ** 2) >= precision:
            raise RuntimeWarning("Divergenta")
    except RuntimeWarning:
        print("Divergenta")
    return x, y, i+1


def approx_gradient(F, x, y, h=1e-7):
    grad_x = (3 * F(x, y) - 4 * F(x - h, y) + F(x - 2*h, y)) / (2 * h)
    grad_y = (3 * F(x, y) - 4 * F(x, y - h) + F(x, y - 2*h)) / (2 * h)
    return np.array([grad_x, grad_y])

def F1(x, y):
    return x**2 + y**2 - 2*x - 4*y - 1

def dF1(x, y):
    return np.array([2*x - 2, 2*y - 4])

def F2(x, y):
    return 3*x**2 - 12*x + 2*y**2 + 16*y - 10

def dF2(x, y):
    return np.array([6*x - 12, 4*y + 16])

def F3(x, y):
    return x**2 - 4*x*y + 5*y**2 - 4*y + 3

def dF3(x, y):
    return np.array([2*x - 4*y, -4*x + 10*y - 4])

def F4(x, y):
    return x**2*y - 2*x*y**2 + 3*x*y + 4

def dF4(x, y):
    return np.array([2*x*y - 2*y**2 + 3*y, x**2 - 4*y*x + 3*x])

# Set the initial point, learning rate, precision and maximum number of iterations
x_init, y_init = np.random.rand(2)
learning_rate = 0.01
precision = 1e-5
max_iters = 30000

# List of functions and their gradients
functions = [(F1, dF1), (F2, dF2), (F3, dF3), (F4, dF4)]

results_analytic = []
results_approx = []

print("Metoda analitică:")

# Run the gradient descent algorithm for each function
for i, (F, dF) in enumerate(functions, start=1):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        x_min, y_min, iterations = gradient_descent(F, dF, x_init, y_init, learning_rate, precision, max_iters)
    results_analytic.append((x_min, y_min))
    if x_min == -np.inf or x_min == np.inf or y_min == -np.inf or y_min == np.inf:
        print("Pentru functia F" + str(i) + " - Divergenta")
        continue
    print("Pentru funcția F" + str(i) + ":", x_min, y_min, "iteratii: ", iterations)

print("\nMetoda aproximativă:")

functions = [F1, F2, F3, F4]

# Run the gradient descent algorithm for each function
for i, F in enumerate(functions, start=1):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        dF = lambda x, y: approx_gradient(F, x, y)
        x_min, y_min, iterations = gradient_descent(F, dF, x_init, y_init, learning_rate, precision, max_iters)
    results_approx.append((x_min, y_min))
    if x_min == -np.inf or x_min == np.inf or y_min == -np.inf or y_min == np.inf:
        print("Pentru functia F" + str(i) + " - Divergenta")
        continue
    print("Pentru funcția F" + str(i) + ":", x_min, y_min, "iteratii: ", iterations)

print("\nCompararea rezultatelor:")
for i in range(len(functions)):
    x_min_analytic, y_min_analytic = results_analytic[i]
    x_min_approx, y_min_approx = results_approx[i]
    print(f"Pentru funcția F{i+1} eroarea este {np.sqrt((x_min_analytic - x_min_approx)**2 + (y_min_analytic - y_min_approx)**2)}")

# GUI
root = tk.Tk()

# Create a treeview widget
tree = ttk.Treeview(root, columns=('Funtion', 'Analytical', 'Approximation', 'Error'), show='headings')
tree.heading('Funtion', text='Funtion')
tree.heading('Analytical', text='Analytical')
tree.heading('Approximation', text='Approximation')
tree.heading('Error', text='Error')
tree.pack()

for i in range(len(functions)):
    x_min_analytic, y_min_analytic = results_analytic[i]
    x_min_approx, y_min_approx = results_approx[i]
    error = np.sqrt((x_min_analytic - x_min_approx)**2 + (y_min_analytic - y_min_approx)**2)
    tree.insert("", "end", values=(f"F{i+1}", f"({x_min_analytic}, {y_min_analytic})", f"({x_min_approx}, {y_min_approx})", error))

root.mainloop()