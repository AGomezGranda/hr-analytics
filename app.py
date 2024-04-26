import dash
from dash import Dash, html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True,
           external_stylesheets=[dbc.themes.SPACELAB])
df = pd.read_csv('data/HR_Analytics.csv')

# app.layout = html.Div([
#     html.Div([
#         html.H1('HR Analytics Dashboard'),
#         # html.Div([
#         #     html.Div(
#         #         dbc.Link(f"{page['name']}", href=page["relative_path"], style={
#         #             'textDecoration': 'none',
#         #             'fontSize': '20px',
#         #             'margin-top': '15px',
#         #             'color': '#111',

#         #         })
#         #     ) for page in dash.page_registry.values()
#         # ], style={'width': '20%', 'float': 'left', 'border': '1px solid #111', 'border-radius': '5px', 'padding': '5px', 'background-color': '#f2f2f2'}),

#         dbc.Nav(
#             [
#                 dbc.NavItem(
#                     [
#                         html.Div(page["name"],  className="ms-2"),
#                     ],
#                     href=page["relative_path"],
#                     active="exact",
#                 )
#                 for page in dash.page_registry.values()
#             ],
#             vertical=True,
#             className="bg-light",
#         )
#     ]),
#     html.Div([
#         dash.page_container
#     ], style={'width': '78%', 'float': 'right', 'border': '1px solid #111', 'border-radius': '5px', 'margin-bottom': '5px', 'background-color': '#f2f2f2'}),
# ],
#     style={'font-family': 'sans-serif', 'margin': '20px'}
# )


app.layout = dbc.Container(

    dbc.Row([

        html.H1('HR Analytics Dashboard', className="display-5"),

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
            ], style={'border': '1px solid #111', 'border-radius': '5px', 'margin-bottom': '5px', 'background-color': '#f2f2f2'}),
            width=9
        ),
    ]),
    fluid=True,
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
