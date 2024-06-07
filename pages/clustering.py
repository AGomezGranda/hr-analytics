import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
import plotly.express as px
from dash.dependencies import Input, Output

import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans


dash.register_page(__name__, name='Clustering', order=4)

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

# columns_pre = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked',
#                'PercentSalaryHike', 'TotalWorkingYears', 'YearsAtCompany']

# columns = ['MonthlyIncome', 'NumCompaniesWorked', 'TotalWorkingYears']

columns = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion']

def elbow_method(data, columns):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++',
                        max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data[columns])
        wcss.append(kmeans.inertia_)
    return go.Figure(data=go.Scatter(x=np.arange(1, 11), y=wcss), layout=go.Layout(title='Elbow Method', xaxis=dict(title='Number of clusters'), yaxis=dict(title='WCSS')))


def kmeans_clustering(data, columns):
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++',
                    max_iter=300, n_init=10, random_state=0)
    data['cluster'] = kmeans.fit_predict(data[columns])

    # Crear una figura de Plotly con un scatter plot para cada cluster
    fig = go.Figure()
    for i in range(n_clusters):
        cluster_data = data[data['cluster'] == i]
        fig.add_trace(go.Scatter(
            # Asume que columns tiene al menos dos elementos
            x=cluster_data[columns[0]],
            y=cluster_data[columns[1]],
            mode='markers',
            name=f'Cluster {i}'
        ))

    return fig


def kmeans_clustering_3d(data, columns):
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++',
                    max_iter=300, n_init=10, random_state=0)
    data['cluster'] = kmeans.fit_predict(data[columns])

    # Crear una figura de Plotly con un scatter plot 3D para cada cluster
    fig = go.Figure()
    for i in range(n_clusters):
        cluster_data = data[data['cluster'] == i]
        fig.add_trace(go.Scatter3d(
            # Asume que columns tiene al menos tres elementos
            x=cluster_data[columns[0]],
            y=cluster_data[columns[1]],
            z=cluster_data[columns[2]],
            mode='markers',
            name=f'Cluster {i}'
        ))

    return fig

# Layout:
layout = html.Div(
    children=[
        html.Div([
            html.H1('Clustering  K-means'),

            html.H3('Método del codo', style={'margin-top': '20px'}),
            # Elbow Method Graph
            dcc.Graph(id='elbow_method'),

            html.H3('Gráfico bidimensional Clusters',
                    style={'margin-top': '20px'}),
            dcc.Graph(id='kmeans'),

            html.H3('Gráfico tridimensional Clusters',
                    style={'margin-top': '20px'}),
            dcc.Graph(id='kmeans_3d'),

        ]),
    ], style={'padding': '20px'}
)


#calculate via the elbow method the optimal number of clusters
@callback(
        Output('elbow_method', 'figure'),
        Input('elbow_method', 'id')
)
def update_graph(id):
    return elbow_method(data, columns)

#calculate the kmeans clustering


@callback(
    Output('kmeans', 'figure'),
    [Input('kmeans', 'id')]
)
def update_kmeans(id):
    return kmeans_clustering(data, columns)


@callback(
    Output('kmeans_3d', 'figure'),
    [Input('kmeans_3d', 'id')]
)
def update_kmeans_3d(id):
    return kmeans_clustering_3d(data, columns)
