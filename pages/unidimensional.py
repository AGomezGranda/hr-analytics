import dash
import pandas as pd
import numpy as np
from dash import html, dcc, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from scipy.stats import gaussian_kde

dash.register_page(__name__, name='Análisis Unidimensional', order=1)

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

columns = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'JobLevel', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

#Layout:
layout = html.Div(
    children=[
        html.H1('Análisis Unidimensional'),
        html.H3('Selecciona la primera columna:', style={}),
        dcc.Dropdown(
            id='column-select',
            options=[{'label': i, 'value': i} for i in columns],
            value=columns[0],
        ),
        dash_table.DataTable(id='table'),
        dcc.Graph(id='histogram'),
        html.Div(
            children=[
                dcc.Graph(id='box_fig_outliers', style={
                          'display': 'inline-block', 'width': '50%'}),
                dcc.Graph(id='box_fig_strip', style={
                          'display': 'inline-block', 'width': '50%'})
            ]
        ),
    ], style={'padding': '20px'}
)

# Callbacks:
@callback(
    [Output('table', 'data'), Output('table', 'columns'), Output('histogram', 'figure'), Output(
        'box_fig_outliers', 'figure'), Output('box_fig_strip', 'figure')],
    [Input('column-select', 'value')]
)
def update_output(column):
    stats = {
        'Moda': round(data[column].mode()[0], 6),
        'Rango': round(data[column].max() - data[column].min(), 6),
        'Q1': round(data[column].quantile(0.25), 6),
        'Mediana Q2': round(data[column].median(), 6),
        'Q3': round(data[column].quantile(0.75), 6),
        'std': round(data[column].std(), 6),
        'var': round(data[column].var(), 6),
        'CV': round(data[column].std() / data[column].mean(), 6),
        'Min': round(data[column].min(), 6),
        'Máx': round(data[column].max(), 6),
        'Media': round(data[column].mean(), 6),
        'Asimetría': round(data[column].skew(), 6),
        'Curtosis': round(data[column].kurt(), 6),
    }
    data_stats = pd.DataFrame.from_records([stats])
    table_data = data_stats.to_dict('records')
    table_columns = [{"name": i, "id": i} for i in data_stats.columns]

    # histogram for the column selected
    num_bins = np.sqrt(len(data[column]))
    num_bins = int(num_bins)

    density = gaussian_kde(data[column])
    x_values = np.linspace(min(data[column]), max(data[column]), 200)
    y_values = density(x_values)

    hist = px.histogram(data, x=column, nbins=num_bins,
                        histnorm='probability density')
    fig = hist.update_layout(bargap=0.01)
    hist.add_trace(go.Scatter(x=x_values, y=y_values,
                   mode='lines', name='Density'))

    # box plot for the column selected
    box_fig_outliers = go.Figure(
        data=[{'y': data[column], 'type': 'box',
               'name': column, 'boxpoints': 'outliers'}],
    )

    box_fig_strip = px.strip(data[column], title=column)

    return table_data, table_columns, hist, box_fig_outliers, box_fig_strip
