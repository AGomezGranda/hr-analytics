import dash
import pandas as pd
from dash import html, dcc, dash_table


dash.register_page(__name__, path='/', name='Inicio', order=0)

data_path = 'data/HR_Analytics.csv'


def load_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8', sep=";")
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


data = load_data(data_path)

layout = html.Div(
    children=[
    html.H1('Inicio'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto'},        
    ),
    ], style={'padding': '20px'}
)
