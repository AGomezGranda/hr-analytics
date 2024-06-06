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

df = pd.read_csv(data_path)


columns = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'JobLevel', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

#Layout:
layout = html.Div(
    children=[
        html.H1('Análisis Unidimensional'),
        html.H3('Selecciona la primera columna:', style={
            'display': 'inline-block', 'margin-right': '10px'}),
        dcc.Dropdown(
            id='column-select',
            options=[{'label': i, 'value': i} for i in columns],
            value=columns[0],
            style={'width': '50%', 'display': 'inline-block',
                   'margin-left': '20px'}
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
    ], style={'margin': '20px'}
)

# Callbacks:
@callback(
    [Output('table', 'data'), Output('table', 'columns'), Output('histogram', 'figure'), Output(
        'box_fig_outliers', 'figure'), Output('box_fig_strip', 'figure')],
    [Input('column-select', 'value')]
)
def update_output(column):
    stats = {
        'Moda': round(df[column].mode()[0], 6),
        'Rango': round(df[column].max() - df[column].min(), 6),
        'Q1': round(df[column].quantile(0.25), 6),
        'Mediana Q2': round(df[column].median(), 6),
        'Q3': round(df[column].quantile(0.75), 6),
        'std': round(df[column].std(), 6),
        'var': round(df[column].var(), 6),
        'CV': round(df[column].std() / df[column].mean(), 6),
        'Min': round(df[column].min(), 6),
        'Máx': round(df[column].max(), 6),
        'Media': round(df[column].mean(), 6),
        'Asimetría': round(df[column].skew(), 6),
        'Curtosis': round(df[column].kurt(), 6),
    }
    df_stats = pd.DataFrame.from_records([stats])
    table_data = df_stats.to_dict('records')
    table_columns = [{"name": i, "id": i} for i in df_stats.columns]

    # histogram for the column selected
    num_bins = np.sqrt(len(df[column]))
    num_bins = int(num_bins)

    density = gaussian_kde(df[column])
    x_values = np.linspace(min(df[column]), max(df[column]), 200)
    y_values = density(x_values)

    hist = px.histogram(df, x=column, nbins=num_bins,
                        histnorm='probability density')
    fig = hist.update_layout(bargap=0.01)
    hist.add_trace(go.Scatter(x=x_values, y=y_values,
                   mode='lines', name='Density'))

    # box plot for the column selected
    box_fig_outliers = go.Figure(
        data=[{'y': df[column], 'type': 'box',
               'name': column, 'boxpoints': 'outliers'}],
    )

    box_fig_strip = px.strip(df[column], title=column)

    return table_data, table_columns, hist, box_fig_outliers, box_fig_strip
