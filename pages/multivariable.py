import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
import plotly.express as px
from dash.dependencies import Input, Output

import statsmodels.api as sm

dash.register_page(__name__, name='Análisis Multivariable', order=3)

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


columns = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'JobLevel', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']


# Layout:
layout = html.Div(
    children=[
        html.Div([
            html.H1('Análisis Multivariable'),
            html.H3('Seleccina la primera columna (eje-x)'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[1]
            ),
            html.H3('Selecciona la segunda columna (eje-y)'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[5]
            ),
            html.H4('Regresión lineal'),
            dcc.Graph(id='linear_regression'),
            dash_table.DataTable(id='regression_results'),
        ]),
    ], style={'margin': '20px'}
)
# Callbacks:


@callback(
    Output('linear_regression', 'figure'),
    [Input('xaxis-column', 'value'), Input('yaxis-column', 'value')]
)
def multidimensional_analysis(column1, column2):

    linear_regression = px.scatter(
        df, x=column1, y=column2, opacity=0.65,
        trendline='ols', trendline_color_override='darkblue'
    )
    return linear_regression


@callback(
    Output('regression_results', 'data'),
    Output('regression_results', 'columns'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value')
)
def update_regression_results(column1, column2):
    df[column1] = pd.to_numeric(df[column1], errors='coerce')
    df[column2] = pd.to_numeric(df[column2], errors='coerce')
    df_clean = df.dropna(subset=[column1, column2])
    X = sm.add_constant(df_clean[column1])
    model = sm.OLS(df_clean[column2], X)
    results = model.fit()

    results_df = pd.DataFrame({
        'Métrica': ['R2', 'P-value'],
        'Valor': [results.rsquared, results.f_pvalue]
    })

    data = results_df.to_dict('records')
    columns = [{"name": i, "id": i} for i in results_df.columns]

    return data, columns
