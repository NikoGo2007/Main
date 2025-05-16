import numpy as np

# Создаем два массива размерности (10, 4) со случайными числами от -5 до 5
ar1 = np.random.randint(-5, 6, size=(10, 4))
ar2 = np.random.randint(-5, 6, size=(10, 4))

# Удваиваем значения ar1, которые больше соответствующих значений ar2, остальные делаем 0
result = np.where(ar1 > ar2, ar1 * 2, 0)

print("Массив ar1:")
print(ar1)
print("\nМассив ar2:")
print(ar2)
print("\nРезультат:")
print(result)