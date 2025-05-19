import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/page2", name="Анализ музыкальных трендов")

# Загрузка данных
df = pd.read_csv("cleaned_dat.csv")

# Подготовка данных для карты
country_artist_counts = df.groupby('country')['artists'].nunique().reset_index()
country_artist_counts.columns = ['country', 'artist_count']

# Получаем топ-5 исполнителей по сумме popularity их треков
top_artists = df.groupby('artists').agg(
    total_popularity=('popularity', 'sum'),
    track_count=('track_name', 'nunique')
).reset_index().sort_values('total_popularity', ascending=False).head(5)
top_artists['rank'] = range(1, 6)

# Получаем топ-5 треков по popularity (уникальные треки)
top_tracks = df.sort_values('popularity', ascending=False).drop_duplicates('track_name').head(5)
top_tracks['rank'] = range(1, 6)

layout = dbc.Container([
    html.Div(style={"display": "none"}, children=[
        html.Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
        )
    ]),

    dbc.Row([
        # Левый столбец (43%)
        dbc.Col([

            # Чарт "Топ исполнителей"
            html.Div([
                html.H4("Топ исполнителей", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontWeight': 'bold',
                }),
                html.Div([
                    html.Table([
                        html.Thead([
                        html.Tr([
                            html.Th("Ранг", style={'color': 'white', 'padding': '12px 8px'}),
                            html.Th("Исполнитель", style={'color': 'white', 'padding': '12px 8px'}),
                            html.Th("Треков", style={'color': 'white', 'padding': '12px 8px'})
                        ])
                    ]),
                        html.Tbody([
                            html.Tr([
                                html.Td(f"{artist['rank']}.", style={
                                    'textAlign': 'left',
                                    'color': 'white',
                                    'fontWeight': 'bold',
                                    'padding': '12px 8px'  # Увеличенные отступы внутри ячейки
                                }),
                                html.Td(artist['artists'], style={
                                    'textAlign': 'left',
                                    'color': 'white',
                                    'fontWeight': 'bold',
                                    'padding': '12px 8px'  # Увеличенные отступы внутри ячейки
                                }),
                                html.Td(artist['track_count'], style={
                                    'textAlign': 'right',
                                    'color': 'white',
                                    'padding': '12px 8px'  # Увеличенные отступы внутри ячейки
                                })
                            ], style={'borderBottom': '1px solid #595959'}) for _, artist in top_artists.iterrows()
                        ])
                    ], style={
                        'width': '100%',
                        'borderCollapse': 'collapse',
                    })
                ], style={
                    'backgroundColor': 'transparent',
                    'padding': '10px'
                })
            ], style={
                'backgroundColor': '#242424',
                'borderRadius': '15px',
                'padding': '20px',
                'marginBottom': '20px'
            }),

            # Чарт "Топ треков"
            html.Div([
                html.H4("Топ треков", style={
                    'textAlign': 'center',
                    'color': 'white',
                    'marginBottom': '20px',
                    'fontWeight': 'bold'
                }),
                dbc.ListGroup([
                    dbc.ListGroupItem([
                        html.Div([
                            html.Div([
                                html.Span(f"{track['rank']}. ", style={
                                    'fontWeight': 'bold',
                                    'color': '#22919D'
                                }),
                                html.Span(track['track_name'], style={
                                    'fontWeight': 'bold',
                                    'color': 'white'
                                })
                            ]),
                            html.Div([
                                html.Small(track['artists'], style={
                                    'color': 'lightgray',
                                    'fontSize': '14px'
                                }),
                            ], style={'marginTop': '3px'})
                        ], style={'padding': '10px'})
                    ], style={
                        'backgroundColor': '#242424',
                        'borderColor': '#595959',
                        'borderLeft': f'4px solid #22919D',
                        'marginBottom': '10px'
                    }) for _, track in top_tracks.iterrows()
                ], flush=True)
            ], style={
                'backgroundColor': '#242424',
                'borderRadius': '15px',
                'padding': '10px'
            })
        ], width=5),  # 43% ширины

        # Правый столбец (57%) - Карта
dbc.Col([
    html.Div([
        html.H4("Популярные исполнители на карте мира", style={
            'textAlign': 'center',
            'color': 'white',
            'marginBottom': '20px',
            'fontWeight': 'bold'
        }),
        dcc.Graph(
            id='world-map',
            figure=px.choropleth(
                country_artist_counts,
                locations='country',
                locationmode='country names',
                color='artist_count',
                hover_name='country',
                color_continuous_scale='YlOrRd',
                labels={'artist_count': 'Кол-во'},
                projection='natural earth'
            ).update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                margin=dict(l=0, r=0, t=0, b=60),  # Увеличили нижний отступ для шкалы
                coloraxis_colorbar=dict(
                    title='Кол-во',
                    title_font=dict(color='white'),
                    tickfont=dict(color='white'),
                    x=0.01,
                    y=-0.4,  # Позиция шкалы (0-1, где 0 - низ)
                    len=0.7,  # Длина шкалы
                    thickness=15,
                    yanchor='bottom'  # Привязка к низу
                ),
                geo=dict(
                    bgcolor='rgba(0,0,0,0)',
                    lakecolor='#D2F2EF',
                    landcolor='#242424',
                    subunitcolor='grey',
                    center=dict(lon=0, lat=0),  # Центр карты
                    projection_scale=1  # Масштаб карты
                )
            ),
            style={
                'margin': '0 auto',
                'height': '70vh',
                'paddingBottom': '40px'  # Дополнительный отступ снизу
            }
        )
    ], style={
        'backgroundColor': '#242424',
        'borderRadius': '15px',
        'padding': '20px',
        'height': '100%'
    })
], width=7)
    ], style={'marginTop': '20px'})
], fluid=True, style={
    'padding': '20px',
    'background': 'linear-gradient(45deg, #D2F2EF, #9FD5D7)',
    'fontFamily': 'Inter, sans-serif',
    'minHeight': '100vh'
})


@callback(
    Output('world-map', 'figure'),
    Input('country-filter', 'value')
)
def update_map(selected_countries):
    filtered_data = df.copy()
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

    # Обновляем данные для карты
    country_counts = filtered_data.groupby('country')['artists'].nunique().reset_index()
    country_counts.columns = ['country', 'artist_count']

    # Создаем обновленную карту
    fig = px.choropleth(
    country_counts,
    locations='country',
    locationmode='country names',
    color='artist_count',
    hover_name='country',
    hover_data={'artist_count': True, 'country': False},
    color_continuous_scale='YlOrRd',
    labels={'artist_count': 'Количество исполнителей'},
    projection='natural earth'
).update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_colorbar=dict(
        title='Количество исполнителей',  # Более описательное название
        x=0.02,
        y=0.15,
        len=0.7,
        thickness=15,
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        lakecolor='#D2F2EF',
        landcolor='#242424',
        subunitcolor='grey'
    )
)

    return fig