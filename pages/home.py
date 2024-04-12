import dash
import pandas as pd
from dash import html, dcc, dash_table


dash.register_page(__name__, path='/')

df = pd.read_csv('data/HR_Analytics.csv')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
    dcc.Graph(
        id='employee-count',
        figure={
            'data': [
                {'labels': df['Department'], 'values': df['EmployeeCount'],
                 'type': 'pie', 'name': 'Employee Count'}
            ],
            'layout': {
                'title': 'Employee Count by Department'
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
                'title': 'Gender Distribution'
            }
        }
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=20,  # Muestra solo 20 filas a la vez
        # Asegura que la tabla no se expanda más allá de su contenedor
        style_table={'overflowX': 'auto'},
        # Agrega márgenes a los datos
        
    ),


])
