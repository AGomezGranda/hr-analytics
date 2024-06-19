import dash
import pandas as pd
import numpy as np
from dash import html, dcc, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import statsmodels.api as sm
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Análisis Bidimensional', order=2)

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

columns = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

layout = html.Div(
    children=[
        html.Div([
            html.H1('Análisis Bidimensional'),

            dbc.Tabs([
                dbc.Tab(label='Correlación', children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H3('Matriz de Correlación', style={
                                'margin-top': '20px'}),
                            dcc.Graph(id='correlation'),

                        ]),
                    ]),
                ]),
                dbc.Tab(label='Mapa de Calor', children=[
                    dbc.Card([
                        dbc.CardBody([

                            html.H3('Mapa de calor',  style={
                                    'margin-top': '20px'}),

                            html.H4('Seleccina la primera columna (eje-x)',
                                    style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='heatmap-xaxis-column',
                                options=[{'label': i, 'value': i}
                                         for i in columns],
                                value=data.columns[0]
                            ),
                            html.H4('Selecciona la segunda columna (eje-y)',
                                    style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='heatmap-yaxis-column',
                                options=[{'label': i, 'value': i}
                                         for i in columns],
                                value=data.columns[3]
                            ),

                            dcc.Graph(id='heatmap'),
                        ]),
                    ]),
                ]),

                dbc.Tab(label='Regresión Lineal', children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H3('Regresión lineal',  style={
                                    'margin-top': '20px'}),

                            html.H4('Seleccina la primera columna (eje-x)',
                                    style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='xaxis-column',
                                options=[{'label': i, 'value': i}
                                         for i in columns],
                                value=data.columns[0]
                            ),
                            html.H4('Selecciona la segunda columna (eje-y)',
                                    style={'margin-top': '10px'}),
                            dcc.Dropdown(
                                id='yaxis-column',
                                options=[{'label': i, 'value': i}
                                         for i in columns],
                                value=data.columns[3]
                            ),

                            dcc.Graph(id='linear_regression'),
                            dcc.Graph(id='residual_plot'),
                            dash_table.DataTable(id='regression_results'),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ], style={'padding': '20px'}
)


@callback(
    [Output('correlation', 'figure'), Output('heatmap', 'figure')],
    [Input('heatmap-xaxis-column', 'value'), Input('heatmap-yaxis-column', 'value')]
)
def bi_dimensional_analysis(column1, column2):

    # Correlation matrix
    correlation_matrix = data[columns].corr()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    masked_correlation_matrix = correlation_matrix.mask(mask)

    correlation_fig = ff.create_annotated_heatmap(
        z=masked_correlation_matrix.values,
        x=list(masked_correlation_matrix.columns),
        y=list(masked_correlation_matrix.index),
        annotation_text=masked_correlation_matrix.round(2).values,
        colorscale='Viridis',
        showscale=True,
        hoverinfo="none",
        xgap=1,
        ygap=1
    )

    correlation_fig.update_layout(
        height=750,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        yaxis_autorange='reversed',
        template='plotly_white'
    )

    for i in range(len(correlation_fig.layout.annotations)):
        if correlation_fig.layout.annotations[i].text == 'nan':
            correlation_fig.layout.annotations[i].text = ""

    # Density heatmap
    heatmap_fig = px.density_heatmap(
        data, x=column1, y=column2, marginal_x="histogram", marginal_y="histogram")

    return correlation_fig, heatmap_fig


@callback(
    [Output('linear_regression', 'figure'), Output('regression_results', 'data'), Output(
        'regression_results', 'columns'), Output('residual_plot', 'figure')],
    [Input('xaxis-column', 'value'), Input('yaxis-column', 'value')]
)
def linear_regression(column1, column2):
    linear_regression = px.scatter(
        data, x=column1, y=column2, opacity=0.65,
        trendline='ols', trendline_color_override='darkblue'
    )

    # Regression results, residuals and residual plot
    data[column1] = pd.to_numeric(data[column1], errors='coerce')
    data[column2] = pd.to_numeric(data[column2], errors='coerce')
    data_clean = data.dropna(subset=[column1, column2])
    X = sm.add_constant(data_clean[column1])
    model = sm.OLS(data_clean[column2], X)
    results = model.fit()

    # Calcula los residuos
    residuals = data_clean[column2] - results.fittedvalues

    # Crea el gráfico de residuos
    residual_plot = go.Figure()
    residual_plot.add_trace(go.Scatter(
        x=results.fittedvalues, y=residuals, mode='markers'))
    residual_plot.update_layout(title='Gráfico de Residuos',
                                xaxis_title='Fitted Values', yaxis_title='Residuals')

    results_data = pd.DataFrame({
        'Métrica': ['R2', 'P-value'],
        'Valor': [results.rsquared.round(4), results.f_pvalue.round(4)]
    })

    res_data = results_data.to_dict('records')
    res_columns = [{"name": i, "id": i} for i in results_data.columns]

    return linear_regression, res_data, res_columns, residual_plot
