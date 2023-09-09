from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt


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

# Определение функции
def f(x, y):
    return 3 * x**2 + x * y - 2 * y**2 - x - 4 * y

# Создание значений x и y
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)

# Создание сетки значений x и y
X, Y = np.meshgrid(x, y)

# Вычисление значений функции на сетке
Z = f(X, Y)

# Построение графика функции с линиями
plt.figure(figsize=(8, 6))
plt.contour(X, Y, Z, levels=15, colors='k')
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции f(x, y) с линиями')
plt.grid(True)
plt.show()