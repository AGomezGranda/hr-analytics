import dash
from dash import Dash, html, dcc
import pandas as pd

app = Dash(__name__, use_pages=True)
df = pd.read_csv('Data/HR_Analytics.csv')

app.layout = html.Div([
    html.Div([
        html.H1('HR Analytics Dashboard'),
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']}", href=page["relative_path"], style={
                    'textDecoration': 'none',
                    'fontSize': '20px',
                    'color': '#000000',
                    'margin-top': '15px',
                })
            ) for page in dash.page_registry.values()
        ], style={'width': '20%', 'float': 'left', 'border':'1px solid #111', 'padding': '5px'}),  # Estilo del menú de navegación
    ]),
    html.Div([
        dash.page_container
    ], style={'width': '78%', 'float': 'right', 'border': '1px solid #111'}),  # Estilo del contenedor de la página
],
    style={'font-family': 'Arial, sans-serif', 'margin': '20px'}
)

if __name__ == '__main__':
    app.run(debug=True)
