from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Загрузка данных
df = pd.read_csv("music_analysis_dashboard.csv")

# Получение уникальных значений для фильтров
all_countries = df['Country'].unique()
all_platforms = df['Streaming Platform'].unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    html.Div([
        html.H1("Анализ музыкальных предпочтений"),
        html.P(
            "Интерактивная панель для анализа поведения слушателей музыки. "
            "Используйте фильтры для настройки отображения данных."
        )
    ], style={
        'backgroundColor': 'rgb(230, 230, 250)',
        'padding': '10px 5px',
        'color': 'rgb(50, 50, 50)'
    }),

    html.Div([
        html.Div([
            html.Label('Страны'),
            dcc.Dropdown(
                id='country-filter',
                options=[{'label': i, 'value': i} for i in all_countries],
                value=['Germany', 'Japan'],
                multi=True
            )
        ], style={'width': '32%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Стриминговые платформы'),
            dcc.Dropdown(
                id='platform-filter',
                options=[{'label': i, 'value': i} for i in all_platforms],
                value=['Deezer', 'Tidal'],
                multi=True
            )
        ], style={'width': '32%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Показатели для анализа'),
            dcc.RadioItems(
                options=[
                    {'label': 'Минут прослушивания в день', 'value': 'Minutes Streamed Per Day'},
                    {'label': 'Количество лайкнутых песен', 'value': 'Number of Songs Liked'},
                    {'label': 'Популярность артиста', 'value': 'popularity'},
                    {'label': 'Танцевальность', 'value': 'danceability'},
                ],
                id='metric-selector',
                value='Minutes Streamed Per Day',
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            )
        ], style={'width': '32%', 'float': 'right', 'display': 'inline-block'}),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(248, 248, 255)',
        'padding': '10px 5px'
    }),

    html.Div([
        html.Div(
            dcc.Graph(id='age-distribution'),
            style={'width': '49%', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Graph(id='top-genres'),
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ),
    ]),

    html.Div(
        dcc.Graph(id='time-distribution'),
        style={'width': '100%', 'display': 'inline-block'}
    ),

    html.Div(
        dcc.Graph(id='artist-popularity'),
        style={'width': '100%', 'display': 'inline-block'}
    )

], fluid=True)


# Колбэки для обновления графиков
@callback(
    Output('age-distribution', 'figure'),
    [Input('country-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('metric-selector', 'value')]
)
def update_age_distribution(countries, platforms, metric):
    filtered_data = df[df['Country'].isin(countries) &
                       df['Streaming Platform'].isin(platforms)]

    fig = px.box(
        filtered_data,
        x='Country',
        y=metric,
        color='Streaming Platform',
        title=f'Распределение {metric} по возрасту и странам',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig


@callback(
    Output('top-genres', 'figure'),
    [Input('country-filter', 'value'),
     Input('platform-filter', 'value')]
)
def update_top_genres(countries, platforms):
    filtered_data = df[df['Country'].isin(countries) &
                       df['Streaming Platform'].isin(platforms)]

    genre_counts = filtered_data['Top Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    fig = px.bar(
        genre_counts.head(10),
        x='Genre',
        y='Count',
        title='Топ 10 музыкальных жанров',
        color='Genre',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig


@callback(
    Output('time-distribution', 'figure'),
    [Input('country-filter', 'value'),
     Input('platform-filter', 'value')]
)
def update_time_distribution(countries, platforms):
    filtered_data = df[df['Country'].isin(countries) &
                       df['Streaming Platform'].isin(platforms)]

    time_dist = filtered_data['Listening Time (Morning/Afternoon/Night)'].value_counts().reset_index()
    time_dist.columns = ['Time', 'Count']

    fig = px.pie(
        time_dist,
        values='Count',
        names='Time',
        title='Распределение времени прослушивания',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig


@callback(
    Output('artist-popularity', 'figure'),
    [Input('country-filter', 'value'),
     Input('platform-filter', 'value')]
)
def update_artist_popularity(countries, platforms):
    filtered_data = df[df['Country'].isin(countries) &
                       df['Streaming Platform'].isin(platforms)]

    # Группируем по артистам и считаем среднюю популярность
    artist_pop = filtered_data.groupby('Most Played Artist')['popularity'].mean().reset_index()
    artist_pop = artist_pop.sort_values('popularity', ascending=False).head(20)

    fig = px.bar(
        artist_pop,
        x='Most Played Artist',
        y='popularity',
        title='Топ 20 артистов по популярности',
        color='Most Played Artist',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)