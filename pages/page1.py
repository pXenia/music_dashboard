import dash
from dash import html, callback, Output, Input, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path="/page1", name="Страница 1")

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
                        'color': 'white',
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
            html.Div(
                dcc.Graph(id='genre-popularity-chart', style={'height': '70vh'}),
                style={
                    'borderRadius': '45px',
                    'backgroundColor': '#242424',
                    'padding': '25px'
                }
            ),
            width=6
        ),

        # Центральная колонка с графиками
        dbc.Col([
            html.Div(
                dcc.Graph(id='explicit-progress', style={'height': '30vh'}),
                style={
                    'borderRadius': '45px',
                    'backgroundColor': '#242424',
                    'padding': '25px',
                    'marginBottom': '20px'
                }
            ),
            html.Div(
                dcc.Graph(id='tempo-distribution-chart', style={'height': '30vh'}),
                style={
                    'borderRadius': '45px',
                    'backgroundColor': '#242424',
                    'padding': '25px'
                }
            )
        ], width=3),

        # Правая колонка с карточками
        dbc.Col(
            html.Div([
                html.Div([
                    html.H5("Самый короткий трек:", style={'textAlign': 'center', 'color': 'white'}),
                    html.H3(id='shortest-track', style={'textAlign': 'center', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'padding': '15px', 'marginBottom': '20px', 'height': '20vh'}),

                html.Div([
                    html.H5("Средняя продолжительность трека:", style={'textAlign': 'center', 'color': 'white'}),
                    html.H3(id='avg-track', style={'textAlign': 'center', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'padding': '15px', 'marginBottom': '20px', 'height': '20vh'}),

                html.Div([
                    html.H5("Самый длинный трек:", style={'textAlign': 'center', 'color': 'white'}),
                    html.H3(id='longest-track', style={'textAlign': 'center', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'padding': '15px', 'height': '20vh'})
            ], style={
                'borderRadius': '45px',
                'backgroundColor': '#242424',
                'padding': '25px'
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
        showlegend=False,
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
        margin=dict(l=20, r=20, t=50, b=20),
        height=300
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
    donut_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    # Карточки с длительностью треков
    shortest = ms_to_min_sec(filtered_data['duration_ms'].min()) if not filtered_data.empty else "0:00"
    avg = ms_to_min_sec(filtered_data['duration_ms'].mean()) if not filtered_data.empty else "0:00"
    longest = ms_to_min_sec(filtered_data['duration_ms'].max()) if not filtered_data.empty else "0:00"

    return genre_fig, gauge_fig, donut_fig, shortest, avg, longest