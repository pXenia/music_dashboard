import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
html.Div(style={"display": "none"}, children=[
        html.Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
        )
    ]),
    html.H1("Музыкальный дашборд", className="my-3"),
    dbc.Nav([
        dbc.NavLink("Страница 1", href="/page1", active="exact"),
        dbc.NavLink("Страница 2", href="/page2", active="exact"),
    ], pills=True),
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)