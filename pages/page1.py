import dash
from dash import html, callback, Output, Input, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

dash.register_page(__name__, path="/", name="Страница 1")

# Загрузка данных
df = pd.read_csv("cleaned_dat.csv")
df['explicit'] = df['explicit'].fillna(False)

all_countries = df['country'].unique()


def ms_to_min_sec(duration_ms):
    seconds = int((duration_ms / 1000) % 60)
    minutes = int((duration_ms / (1000 * 60)) % 60)
    return f"{minutes}:{seconds:02d}"


def categorize_tempo(tempo):
    if tempo < 80:
        return "Медленный (0-80)"
    elif 80 <= tempo < 110:
        return "Средний (80-110)"
    else:
        return "Быстрый (110+)"


layout = dbc.Container([

    # Фильтры
    html.Div(
        dbc.Row([
            dbc.Col([
                dbc.Label('Страна исполнителя', style={'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(
                    id='country-filter',
                    options=[{'label': i, 'value': i} for i in all_countries],
                    value=[],
                    multi=True,
                    placeholder="Все страны",
                    style={
                        'backgroundColor': '#595959',
                        'borderRadius': '20px',
                        'color': 'black',
                        'fontSize': '16px'
                    }
                )
            ], width=12)
        ]),
        style={
            'width': '100%',
            'borderRadius': '45px',
            'backgroundColor': '#242424',
            'padding': '25px',
            'marginBottom': '30px'
        }
    ),

    # Графики и карточки
    dbc.Row([
        # Левый график (жанры по популярности)
        dbc.Col(
            html.Div([
                html.H4("Популярность жанров", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }),
                dcc.Graph(id='genre-popularity-chart', style={'height': '70vh'})
            ],
                style={
                    'borderRadius': '45px',
                    'backgroundColor': '#242424',
                    'padding': '25px'
                }),
            width=6
        ),

        # Центральная колонка с графиками
        dbc.Col([
            html.Div([
                html.H4("Доля треков с explicit-контентом", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }),
                dcc.Graph(id='explicit-progress', style={'height': '30vh'})
            ],
                style={
                    'borderRadius': '45px',
                    'backgroundColor': '#242424',
                    'padding': '25px',
                    'marginBottom': '20px'
                }),

            html.Div([
                html.H4("Распределение темпа треков", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }),
                dcc.Graph(id='tempo-distribution-chart', style={'height': '30vh'})
            ],
                style={
                    'borderRadius': '45px',
                    'backgroundColor': '#242424',
                    'padding': '25px'
                })
        ], width=3),

        # Правая колонка с карточками
        dbc.Col(
            html.Div([
                html.H4("Метрики треков", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }),
                # Карточка "Самый короткий трек"
                html.Div([
                    html.Div("Самый короткий трек", style={
                        'textAlign': 'left',
                        'color': 'white',
                        'fontSize': '16px',
                        'marginBottom': '8px'
                    }),
                    html.Div(id='shortest-track', style={
                        'textAlign': 'left',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'fontSize': '24px'
                    })
                ], style={
                    'padding': '20px',
                    'marginBottom': '20px',
                    'height': '20vh',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                }),

                # Карточка "Средняя продолжительность трека"
                html.Div([
                    html.Div("Средняя продолжительность трека", style={
                        'textAlign': 'left',
                        'color': 'white',
                        'fontSize': '16px',
                        'marginBottom': '8px'
                    }),
                    html.Div(id='avg-track', style={
                        'textAlign': 'left',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'fontSize': '24px'
                    })
                ], style={
                    'padding': '20px',
                    'marginBottom': '20px',
                    'height': '20vh',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                }),

                # Карточка "Самый длинный трек"
                html.Div([
                    html.Div("Самый длинный трек", style={
                        'textAlign': 'left',
                        'color': 'white',
                        'fontSize': '16px',
                        'marginBottom': '8px'
                    }),
                    html.Div(id='longest-track', style={
                        'textAlign': 'left',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'fontSize': '24px'
                    })
                ], style={
                    'padding': '20px',
                    'height': '20vh',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                })
            ], style={
                'borderRadius': '45px',
                'backgroundColor': '#242424',
                'padding': '25px',
                'width': '100%'
            }),
            width=3
        )
    ])
], fluid=True, style={
    'padding': '20px',
    'background': 'linear-gradient(45deg, #D2F2EF, #9FD5D7)',
    'fontFamily': 'Inter',
    'minHeight': '100vh'
})

@callback(
    [Output('genre-popularity-chart', 'figure'),
     Output('explicit-progress', 'figure'),
     Output('tempo-distribution-chart', 'figure'),
     Output('shortest-track', 'children'),
     Output('avg-track', 'children'),
     Output('longest-track', 'children')],
    [Input('country-filter', 'value')]
)
def update_all_charts(selected_countries):
    filtered_data = df.copy()
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    # График 1: Топ жанров по популярности
    genre_stats = filtered_data.groupby('track_genre')['popularity'].mean().reset_index()
    genre_stats = genre_stats.sort_values('popularity', ascending=False).head(10)
    genre_fig = px.bar(
        genre_stats,
        x='track_genre',
        y='popularity',
        color_discrete_sequence=['#91C9C4']
    )
    genre_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        showlegend=True,  # Включить легенду
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis_title="Средняя популярность",
        xaxis_title="Жанр"
    )

    # График 2: Доля треков без explicit
    non_explicit_percent = (1 - filtered_data['explicit'].mean()) * 100
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=non_explicit_percent,
        number={'suffix': "%"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': 'white', 'tickwidth': 1},
            'bar': {'color': '#D2F2EF'},
            'bgcolor': '#242424',
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#595959'},
                {'range': [50, 80], 'color': '#595959'},
                {'range': [80, 100], 'color': '#595959'}],
        }
    ))
    gauge_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(l=50, r=50, t=10, b=10),  # Увеличиваем отступы
        height=200,
        showlegend=False,
        annotations=[
            dict(
                x=0.5,
                y=-0.2,  # Позиционируем текст под индикатором
                xref='paper',
                yref='paper',
                text="",
                showarrow=False,
                font=dict(size=14, color='white')
            )
        ]
    )

    # График 3: Распределение темпов
    tempo_data = filtered_data.copy()
    tempo_data['tempo_category'] = tempo_data['tempo'].apply(categorize_tempo)
    tempo_dist = tempo_data['tempo_category'].value_counts(normalize=True).reset_index()
    tempo_dist.columns = ['Tempo', 'Percentage']
    tempo_dist['Percentage'] = tempo_dist['Percentage'] * 100

    donut_fig = px.pie(
        tempo_dist,
        values='Percentage',
        names='Tempo',
        hole=0.5,
        color_discrete_sequence=['#64BDC6', '#D9B4A6', '#C3DAA7']
    )
    # В функции update_all_charts в page1.py измените код для donut_fig:

    donut_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        showlegend=True,
        legend=dict(
            orientation="h",  # Горизонтальная ориентация
            yanchor="top",  # Якорь вверху
            y=-0.1,  # Сдвигаем легенду ниже (отрицательное значение)
            xanchor="center",  # Центрируем по горизонтали
            x=0.5,
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0)',  # Прозрачный фон легенды
            bordercolor='rgba(0,0,0,0)'  # Прозрачная граница
        ),
        margin=dict(l=20, r=20, t=30, b=20),  # Увеличиваем нижний отступ для легенды
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    # Также можно добавить прозрачность для секторов диаграммы:
    donut_fig.update_traces(
        marker=dict(line=dict(color='#242424', width=2)),
        opacity=0.9  # Небольшая прозрачность
    )

    # Карточки с длительностью треков
    shortest = ms_to_min_sec(filtered_data['duration_ms'].min()) if not filtered_data.empty else "0:00"
    avg = ms_to_min_sec(filtered_data['duration_ms'].mean()) if not filtered_data.empty else "0:00"
    longest = ms_to_min_sec(filtered_data['duration_ms'].max()) if not filtered_data.empty else "0:00"

    return genre_fig, gauge_fig, donut_fig, shortest, avg, longest