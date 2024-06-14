import dash
from dash import callback, html, dcc, dash_table
import pandas as pd
from dash.dependencies import Input, Output

from scipy.stats import chi2_contingency
from scipy.stats.contingency import association

dash.register_page(__name__, name='Tabla de Contingencia', order=3)

data_path = 'data/HR_Analytics.csv'

df = pd.read_csv(data_path, sep=';')

columns = ['Attrition', 'BusinessTravel', 'Department', 'Education', 'JobLevel', 'EducationField', 'EnvironmentSatisfaction', 'Gender',
           'JobInvolvement', 'JobRole', 'JobSatisfaction', 'MaritalStatus', 'OverTime', 'RelationshipSatisfaction', 'WorkLifeBalance']

layout = html.Div(
    children=[
        html.Div([
            html.H1('Tabla de Contingencia'),
            html.H4('Selecciona la variable independiente (eje-x)'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[1]
            ),
            html.H4('Selecciona la variable dependiente (eje-y)',
                    style={'margin-top': '10px'}),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[2]
            ),
            html.H3('',  style={'margin-top': '20px'}),
            dash_table.DataTable(
                id='contingency',
                page_size=20,
                style_table={'overflowX': 'auto'},
            ),
            html.H4('Coeficientes:',  style={'margin-top': '10px'}),
            dash_table.DataTable(
                id='statistics',
                page_size=20,
                style_table={'overflowX': 'auto'},
            )
        ]),
    ], style={'padding': '20px'}
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


@callback(
    [Output('statistics', 'data'), Output('statistics', 'columns')],
    [Input('xaxis-column', 'value'), Input('yaxis-column', 'value')]
)
def update_statistics(xaxis_column_name, yaxis_column_name):
    contingency = pd.crosstab(df[xaxis_column_name], df[yaxis_column_name])
    chi2, p, dof, expected = chi2_contingency(contingency)

    C = association(contingency, method="pearson")
    T = association(contingency, method="tschuprow")
    
    results = pd.DataFrame({
        'Coeficiente': ['Chi-square', 'Pearson\'s C', 'Tschuprow\'s T'],
        'Valor': [chi2, C, T],
        'P-valor': [p, 'n/a', 'n/a']
    })
    columns = [{"name": i, "id": i} for i in results.columns]
    data = results.to_dict('records')
    return data, columns
