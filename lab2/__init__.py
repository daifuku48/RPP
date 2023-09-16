from scipy.optimize import minimize



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
