from scipy.optimize import minimize
import numpy as np
from scipy.optimize import curve_fit


# Визначення функції
def objective_function(vars):
    x, y = vars
    return 3 * x ** 2 + x * y - 2 * y ** 2 - x - 4 * y


# Задача оптимізації: мінімізувати функцію
result = minimize(objective_function, [0, 0], method='BFGS')

# Вивід результатів
x_optimal, y_optimal = result.x
z_optimal = result.fun

print(f"Значення глобального екстремуму z = {z_optimal}")
print(f"x_optimal = {x_optimal}, y_optimal = {y_optimal}")

# Введені дані
x_data = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
y_data = np.array([0.541, 0.398, 0.232, 0.106, 0.052])

# Задайте функцію f(x), яку ви хочете підігнати під дані
def f(x, a, b):
    return a * x * np.exp(b * x)

# Використовуйте curve_fit для підбору коефіцієнтів a і b
params, covariance = curve_fit(f, x_data, y_data)

# Отримайте значення коефіцієнтів a і b
a, b = params

print(f"Коефіцієнт a: {a}")
print(f"Коефіцієнт b: {b}")

# Обчисліть стандартне відхилення
residuals = y_data - f(x_data, a, b)
std_deviation = np.std(residuals)

print(f"Стандартне відхилення: {std_deviation}")