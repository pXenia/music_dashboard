import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    'https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap'
                ])
server = app.server

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),

    html.H1("Музыкальный дашборд", style={
        'color': 'black',
        'marginBottom': '20px',
        'fontWeight': 'bold'
    }),

    dbc.Nav([
        dbc.NavLink(
            "Страница 1",
            href="/",
            id="nav-link-1",
            style={
                'color': '#242424',
                'marginRight': '10px',
                'padding': '8px 16px',
                'borderRadius': '5px',
                'transition': 'all 0.3s ease',
                'backgroundColor': '#D2F2EF'
            }
        ),
        dbc.NavLink(
            "Страница 2",
            href="/page2",
            id="nav-link-2",
            style={
                'color': '#242424',
                'marginRight': '10px',
                'padding': '8px 16px',
                'borderRadius': '5px',
                'transition': 'all 0.3s ease',
                'backgroundColor': '#D2F2EF'
            }
        ),
    ], pills=True, className="mb-4", style={
        'backgroundColor': '#D2F2EF',
        'borderRadius': '10px',
        'padding': '10px',
        'marginBottom': '20px'
    }),

    dash.page_container,

    # Скрытый компонент для callback'а
    html.Div(id='dummy-output', style={'display': 'none'})
], fluid=True, style={
    'padding': '20px',
    'background': 'linear-gradient(45deg, #D2F2EF, #9FD5D7)',
    'fontFamily': 'Inter',
    'minHeight': '100vh'
})

# Клиентский callback для выделения активной кнопки
app.clientside_callback(
    """
    function(pathname) {
        // Сбрасываем стили для всех кнопок
        document.querySelectorAll('[id^="nav-link-"]').forEach(link => {
            link.style.backgroundColor = '#D2F2EF';
            link.style.fontWeight = 'normal';
            link.style.boxShadow = 'none';
        });

        // Находим активную кнопку
        const activeLink = document.querySelector(`[href="${pathname}"]`);
        if (activeLink) {
            activeLink.style.backgroundColor = '#9FD5D7';
            activeLink.style.fontWeight = 'bold';
            activeLink.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        }

        return null;
    }
    """,
    Output('dummy-output', 'children'),
    Input('url', 'pathname')
)

if __name__ == "__main__":
    app.run(debug=True)