import dash
from dash import callback, html, dcc, dash_table
import pandas as pd
from dash.dependencies import Input, Output

dash.register_page(__name__)

data_path = 'data/HR_Analytics.csv'

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

data = load_data(data_path)

df = pd.read_csv(data_path)

columns = ['Attrition', 'BusinessTravel', 'Department', 'Education', 'EducationField', 'EnvironmentSatisfaction', 'Gender',
           'JobInvolvement', 'JobRole', 'JobSatisfaction', 'MaritalStatus', 'OverTime', 'RelationshipSatisfaction', 'WorkLifeBalance']

# Layout:
layout = html.Div(
    children=[
        html.Div([
            html.H3('Select the first column (x-axis)'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[3]
            ),
            html.H3('Select the second column (y-axis)'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[4]
            ),
            html.H3('Contingency Table:'),
            dash_table.DataTable(
                id='contingency',
                page_size=20,
                style_table={'overflowX': 'auto'},
            )
        ]),
    ], style={'margin': '20px'}
)

@callback(
    [Output('contingency', 'data'), Output('contingency', 'columns')],
    [Input('xaxis-column', 'value'), Input('yaxis-column', 'value')]
)
def update_table(xaxis_column_name, yaxis_column_name):
    contingency = pd.crosstab(df[xaxis_column_name], df[yaxis_column_name])
    contingency.columns = contingency.columns.astype(str)
    contingency.index = contingency.index.astype(str)
    contingency.reset_index(inplace=True)
    columns = [{"name": i, "id": i} for i in contingency.columns]
    data = contingency.to_dict('records')
    return data, columns
