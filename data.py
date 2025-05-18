import pandas as pd

import pandas as pd

df = pd.read_csv('cleaned_dataset.csv',low_memory=False)

df_cleaned = df.dropna()


df_cleaned.to_csv('cleaned_dataset.csv', index=False)

print("Пустые строки удалены. Результат сохранён в 'cleaned_dataset.csv'.")