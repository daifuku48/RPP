import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize, minimize_scalar


# Определение функции
def objective(x, y):
    return 3 * x ** 2 + x * y - 2 * y ** 2 - x - 4 * y


x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
X, Y = np.meshgrid(x, y)
Z = objective(X, Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Будування поверхні
surf = ax.plot_surface(X, Y, Z, cmap='viridis')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Графік z = 3x^2 + xy - 2y^2 - x - 4y')
fig.colorbar(surf)
plt.show()


def z(x):
    x, y = x
    return 3 * x ** 2 + x * y - 2 * y ** 2 - x - 4 * y


# Начальное приближение для поиска минимума
initial_guess_min = [1, 1]

# Нахождение минимума
result_min = minimize(z, initial_guess_min, method='BFGS')

x_optimal, y_optimal = result_min.x
z_optimal = result_min.fun

print(f"Значення глобального екстремуму z = {z_optimal}")
print(f"x_optimal = {x_optimal}, y_optimal = {y_optimal}")

# Нахождение максимума на заданном интервале
result_max = minimize_scalar(lambda x: -z([x, 0]), bounds=(-10, 10), method='bounded')

if result_max.success:
    x_max = result_max.x
    z_max = -result_max.fun
    print(f"Max: x = {x_max}, y = 0, z = {z_max}")
else:
    print("Error.")
