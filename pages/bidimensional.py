import dash
import pandas as pd
import numpy as np
from dash import html, dcc, callback
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

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


columns = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'JobLevel', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

# Layout:
layout = html.Div(
    children=[
        html.Div([
            dcc.Graph(id='correlation'),

            html.H3('Select the first column (x-axis)'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[1]
            ),
            html.H3('Select the second column (y-axis)'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in columns],
                value=df.columns[1]
            ),
            dcc.Graph(id='heatmap'),
            dcc.Graph(id='scatterplot'),
            dcc.Graph(id='linear_regression'),
        ]),
    ]
)

# Callbacks:


@callback(
    [Output('correlation', 'figure'), Output('scatterplot', 'figure'), Output('heatmap', 'figure'), Output('linear_regression', 'figure')],
    [Input('xaxis-column', 'value'), Input('yaxis-column', 'value')]
)
def bi_dimensional_analysis(column1, column2):

    # Correlation matrix
    correlation_matrix = df[columns].corr()
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

    # Scatter plot
    scatter_fig = {
        'data': [go.Scatter(
            x=df[column1],
            y=df[column2],
            mode='markers',
            marker=dict(
                size=5,
                color='blue',
                opacity=0.8
            )
        )],
        'layout': go.Layout(
            title=f'{column1} vs {column2}',
            xaxis={'title': column1},
            yaxis={'title': column2}
        )
    }

    # Density heatmap
    heatmap_fig = px.density_heatmap(
        df, x=column1, y=column2, marginal_x="histogram", marginal_y="histogram")
    
    #Lienar regression (OLS)
    # linear_regression = px.scatter(df, x=column1, y=column2, trendline='ols')

    linear_regression = px.scatter(
        df, x=column1, y=column2, opacity=0.65,
        trendline='ols', trendline_color_override='darkblue'
    )
    
    return correlation_fig, scatter_fig, heatmap_fig, linear_regression
