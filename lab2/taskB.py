import numpy as np
from scipy.optimize import curve_fit

# Введені дані
x_data = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
y_data = np.array([0.541, 0.398, 0.232, 0.106, 0.052])


def f(x, a, b):
    return a * x * np.exp(b * x)


# curve_fit для підбору коефіцієнтів a і b
params, covariance = curve_fit(f, x_data, y_data)

# Значення коефіцієнтів a і b
a, b = params

print(f"Коефіцієнт a: {a}")
print(f"Коефіцієнт b: {b}")

# відхилення
residuals = y_data - f(x_data, a, b)
std_deviation = np.std(residuals)

print(f"Стандартне відхилення: {std_deviation}")
