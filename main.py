# Имя файла
filename = 'artists_cleaned - artists_cleaned.csv.csv'  # Замени на своё имя файла, если нужно

import csv


# Чтение и очистка
rows = []
with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        cleaned_row = []
        for cell in row:
            # Удаляем пробелы вокруг каждого тега
            tags = [tag.strip() for tag in cell.split(';')]
            cleaned_cell = ';'.join(tags)
            cleaned_row.append(cleaned_cell)
        rows.append(cleaned_row)

# Сохранение обратно в файл
with open(filename, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(rows)

print("Лишние пробелы удалены и файл успешно сохранён.")
