import dash
from dash import Dash, html
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True,
           external_stylesheets=[dbc.themes.FLATLY])
df = pd.read_csv('data/HR_Analytics.csv')

app.layout = dbc.Container(

    dbc.Row([

        html.H1('HR Analytics Dashboard', className="display-5", style={"margin-bottom": "10px", "margin-top": "20px"}),
        html.Hr(className="my-3"),

        dbc.Col(
            dbc.Nav(
                [
                    dbc.NavLink(
                        html.Div(page["name"],  className="ms-2"),
                        href=page["relative_path"],
                        active="exact",
                    )
                    for page in dash.page_registry.values()
                ],
                vertical=True,
                pills=True,
                className="bg-light",
            ),
            width=3,
            style={'height': '100vh'}
        ),
        dbc.Col(
            html.Div([
                dash.page_container
            ], style={'border': '1px none #111', 'border-radius': '5px', 'margin-bottom': '5px', 'background-color': '#ECF0F1'}),
            width=9
        ),
    ]),
    fluid=True,
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')