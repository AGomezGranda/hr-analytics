import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
import plotly.express as px
from dash.dependencies import Input, Output

import statsmodels.api as sm
import plotly.graph_objects as go

dash.register_page(__name__, name='Clustering', order=4)

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
            html.H1('Clustering'),
        ]),
    ], style={'margin': '20px'}
)
