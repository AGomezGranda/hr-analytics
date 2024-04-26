import dash
import pandas as pd
from dash import html, dcc, dash_table


dash.register_page(__name__, path='/', name='Inicio', order=0)

df = pd.read_csv('data/HR_Analytics.csv')

layout = html.Div(
    children=[
    html.H1('Inicio'),
    dcc.Graph(
        id='employee-count',
        figure={
            'data': [
                {'labels': df['Department'], 'values': df['EmployeeCount'],
                 'type': 'pie', 'name': 'Employee Count'}
            ],
            'layout': {
                'title': 'Número de empleados por departamento'
            }
        }
    ),
    dcc.Graph(
        id='gender-distribution',
        figure={
            'data': [
                {'x': df['Gender'], 'type': 'histogram', 'name': 'gender'}
            ],
            'layout': {
                'title': 'Distibución de género'
            }
        }
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto'},        
    ),
    ], style={'margin': '20px'}
)
