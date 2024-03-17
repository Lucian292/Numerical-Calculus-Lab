import numpy as np

def gradient_descent(F, dF, x_init, y_init, learning_rate, precision, max_iters):
    x, y = x_init, y_init
    for _ in range(max_iters):
        grad_x, grad_y = dF(x, y)
        x_new = x - learning_rate * grad_x
        y_new = y - learning_rate * grad_y
        if np.sqrt((x_new - x)**2 + (y_new - y)**2) <= precision:
            break
        x, y = x_new, y_new
    return x, y

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

# Run the gradient descent algorithm for each function
for i, (F, dF) in enumerate(functions, start=1):
    x_min, y_min = gradient_descent(F, dF, x_init, y_init, learning_rate, precision, max_iters)
    print(f"The minimum point of the function F{i} is at ({x_min}, {y_min})")
