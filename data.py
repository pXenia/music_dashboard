import pandas as pd

import pandas as pd

import pandas as pd

# Загрузка данных из первой таблицы
url_table1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSOkW9JzizLG6c1Mg637Cx_HDOD7id5F1b9OlvDK4tQyryWYcLS08yD4j_ezOlF9RAuD1RBcPUw6CXE/pub?gid=588798097&single=true&output=csv'  # Замените на реальный URL
df_table1 = pd.read_csv(url_table1)

# Загрузка данных из второй таблицы
url_table2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSOkW9JzizLG6c1Mg637Cx_HDOD7id5F1b9OlvDK4tQyryWYcLS08yD4j_ezOlF9RAuD1RBcPUw6CXE/pub?gid=1666822727&single=true&output=csv'  # Замените на реальный URL
df_table2 = pd.read_csv(url_table2)

# Объединение таблиц по имени исполнителя
merged_df = pd.merge(
    df_table1,
    df_table2[['artist_mb', 'country_lastfm', 'tags_lastfm']],
    left_on='artists',
    right_on='artist_mb',
    how='left'
)

# Удаление временного столбца
if 'artist_mb' in merged_df.columns:
    merged_df.drop('artist_mb', axis=1, inplace=True)

# Переименование столбцов (country_lastfm -> style, tags_lastfm -> country)
merged_df.rename(
    columns={
        'country_lastfm': 'style',
        'tags_lastfm': 'country'
    },
    inplace=True
)

# Удаление строк с пропущенными значениями
df_cleaned = merged_df.dropna()

# Сохранение результата в файл
df_cleaned.to_csv('cleaned_data.csv', index=False)
