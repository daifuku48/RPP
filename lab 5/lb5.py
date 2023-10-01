import pandas as pd

# Припустимо, що ви маєте список результатів розпізнавання тексту
recognized_texts = ["Текст 1", "Текст 2", "Текст 3"]

# Створення DataFrame з результатами
df = pd.DataFrame({'Розпізнаний текст': recognized_texts})

# Виведення DataFrame
print(df)

# Збереження результатів в CSV-файл
df.to_csv('recognized_texts.csv', index=False)