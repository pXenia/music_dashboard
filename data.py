import pandas as pd
import numpy as np

# Функция для правильной загрузки Google Sheets как CSV
def load_gsheet(url):
    # Преобразуем HTML-ссылку в ссылку на CSV
    csv_url = url.replace('/pubhtml?', '/pub?').replace('&single=true', '') + '&output=csv'
    try:
        return pd.read_csv(csv_url, low_memory=False)
    except Exception as e:
        print(f"Ошибка при загрузке данных:\n{e}{url}")
        return None

# Загрузка всех таблиц
df_listeners = load_gsheet("https://docs.google.com/spreadsheets/d/e/2PACX-1vR4NCQKSBWNI0Qah6fewhCM5G8wggJNZOd2m6Vv1CnfIfGhYh6b8veyyiDSZKfGi8eyYcli7aKhhxq7/pubhtml?gid=2018406825&single=true")
df_tracks = load_gsheet("https://docs.google.com/spreadsheets/d/e/2PACX-1vSOkW9JzizLG6c1Mg637Cx_HDOD7id5F1b9OlvDK4tQyryWYcLS08yD4j_ezOlF9RAuD1RBcPUw6CXE/pubhtml?gid=588798097&single=true")
df_artists = load_gsheet("https://docs.google.com/spreadsheets/d/e/2PACX-1vR_Bty1AnobFUGY_sa0cCM64scwyJjZgRahY9W13KzA5kQpoSBX3Yk2H8quKj_27wBv3c30wz5-Wtnp/pubhtml?gid=1595064807&single=true")

# Проверка загрузки данных
if df_listeners is None or df_tracks is None or df_artists is None:
    print("Не удалось загрузить один или несколько датасетов")
else:
    # Очистка строк
    df_listeners['Most Played Artist'] = df_listeners['Most Played Artist'].astype(str).str.strip()
    df_tracks['artists'] = df_tracks['artists'].astype(str).str.split(';').str[0].str.strip()
    df_artists['artist_lastfm'] = df_artists['artist_lastfm'].astype(str).str.strip()

    # Обработка числовых колонок
    numeric_cols = ['popularity', 'duration_ms', 'danceability', 'energy']
    for col in numeric_cols:
        df_tracks[col] = pd.to_numeric(df_tracks[col], errors='coerce')

    # Агрегация
    artist_stats = df_tracks.groupby('artists').agg({
        'popularity': 'mean',
        'duration_ms': 'mean',
        'explicit': lambda x: (x == False).mean() if 'explicit' in df_tracks.columns else np.nan,
        'danceability': 'mean',
        'energy': 'mean'
    }).reset_index().rename(columns={'artists': 'artist'})

    # Объединение таблиц
    df_merged = pd.merge(
        df_listeners,
        artist_stats,
        left_on='Most Played Artist',
        right_on='artist',
        how='left'
    )

    df_final = pd.merge(
        df_merged,
        df_artists,
        left_on='Most Played Artist',
        right_on='artist_lastfm',
        how='left'
    )

    df_final.to_csv('music_analysis_dashboard.csv', index=False)
    print("Датасет успешно сохранен в music_analysis_dashboard.csv")
