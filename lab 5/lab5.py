from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Завантаження зображення
image = Image.open('lab 5\img\img1.jpg')

# Кількість основних кольорів, які потрібно визначити
num_colors = 8

# Перетворення зображення у масив
image_array = np.array(image)

# Розмір масиву: (ширина x висота, кількість каналів)
pixels = image_array.reshape(-1, 3)

# Використання алгоритму K-means для визначення основних кольорів
kmeans = KMeans(n_clusters=num_colors)
kmeans.fit(pixels)

# Отримання RGB-значень основних кольорів
main_colors = kmeans.cluster_centers_.astype(int)

# Заміна кольорів у зображенні на основні кольори
labels = kmeans.predict(pixels)
compressed_pixels = main_colors[labels].reshape(image_array.shape)

# Створення стиснутого зображення
compressed_image = Image.fromarray(compressed_pixels.astype('uint8'), 'RGB')

# Збереження стиснутого зображення
compressed_image.save('compressed_image.jpg')

# Закриття початкового зображення
image.close()
