import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output

from sklearn.decomposition import PCA
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans

import dash_bootstrap_components as dbc
from sklearn.discriminant_analysis import StandardScaler

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

columns = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked', 'PercentSalaryHike',
           'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion']


def elbow_method(data, columns):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++',
                        max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data[columns])
        wcss.append(kmeans.inertia_)
    return go.Figure(data=go.Scatter(x=np.arange(1, 11), y=wcss), layout=go.Layout(xaxis=dict(title='Número de clusters'), yaxis=dict(title='WCSS')))


def kmeans_clustering(data, columns):
    n_clusters = 3
    n_components = 2

    # Estandarizar los datos
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[columns])

    pca = PCA(n_components=n_components)
    data_pca = pca.fit_transform(data_scaled)
    # data_pca = pca.fit_transform(data[columns])

    kmeans = KMeans(n_clusters=n_clusters, init='k-means++',
                    max_iter=300, n_init=10, random_state=0)
    clusters = kmeans.fit_predict(data_pca)

    fig = go.Figure()

    # Agregar los puntos de los clusters al gráfico
    for i in range(n_clusters):
        cluster_data = data_pca[clusters == i]
        fig.add_trace(go.Scatter(
            x=cluster_data[:, 0],
            y=cluster_data[:, 1],
            mode='markers',
            name=f'Cluster {i}',
        ))

    # Agregar los centroides de los clusters al gráfico
    centroids = kmeans.cluster_centers_
    fig.add_trace(go.Scatter(
        x=centroids[:, 0],
        y=centroids[:, 1],
        mode='markers',
        marker=dict(
            size=10,
            color='rgba(0, 0, 0, 1)',
            line=dict(
                width=2,
                color='rgba(255, 255, 255, .5)'
            )
        ),
        name='Centroides'
    ))

    # Agregar las varianzas explicadas por cada componente principal
    variance_ratio = pca.explained_variance_ratio_
    for i, ratio in enumerate(variance_ratio):
        fig.add_annotation(
            x=i / (n_components - 1),
            y=1.1,
            text=f'Componente {i + 1}: {ratio:.2%}',
            showarrow=False,
            xref='paper',
            yref='paper'
        )

    # Configurar los ejes y el título
    fig.update_layout(
        xaxis_title='Dim 1',
        yaxis_title='Dim 2',
        margin=dict(l=0, r=0, t=40, b=0)
    )

    data['Cluster'] = clusters
    means = data.groupby('Cluster')[columns].mean().round(2).reset_index()

    return fig, means


def kmeans_clustering_3d(data, columns):
    n_components = 3
    n_clusters = 3

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[columns])

    pca = PCA(n_components=n_components)
    data_pca = pca.fit_transform(data_scaled)

    kmeans = KMeans(n_clusters=n_clusters, init='k-means++',
                    max_iter=300, n_init=10, random_state=0)
    clusters = kmeans.fit_predict(data_pca)

    # Crear una figura de Plotly con un scatter plot 3D para cada cluster
    fig = go.Figure()
    for i in range(n_clusters):
        cluster_data = data_pca[clusters == i]
        fig.add_trace(go.Scatter3d(
            x=cluster_data[:, 0],
            y=cluster_data[:, 1],
            z=cluster_data[:, 2],
            mode='markers',
            name=f'Cluster {i}'
        ))

    centroids = kmeans.cluster_centers_
    fig.add_trace(go.Scatter3d(
        x=centroids[:, 0],
        y=centroids[:, 1],
        z=centroids[:, 2],
        mode='markers',
        marker=dict(
            size=10,
            color='rgba(0, 0, 0, 1)',
            line=dict(
                width=2,
                color='rgba(255, 255, 255, .5)'
            )
        ),
        name='Centroides'
    ))

    variance_ratio = pca.explained_variance_ratio_
    for i, ratio in enumerate(variance_ratio):
        fig.add_annotation(
            x=i / (n_components - 1),
            y=1.1,
            text=f'Componente {i + 1}: {ratio:.2%}',
            showarrow=False,
            xref='paper',
            yref='paper'
        )


    fig.update_layout(
        scene=dict(
            xaxis_title='Dim 1',
            yaxis_title='Dim 2',
            zaxis_title='Dim 3'
        )
    )

    return fig


layout = html.Div(
    children=[
        html.Div([
            html.H1('Clustering  K-means'),
            dbc.Tabs([
                dbc.Tab(label='Método del codo', children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H3('Método del codo', style={
                                    'margin-top': '20px'}),
                            dcc.Graph(id='elbow_method'),
                        ]),
                    ]),
                ]),
                dbc.Tab(label='Representacion gráfica', children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H3('Gráfico bidimensional Clusters',
                                    style={'margin-top': '20px'}),
                            dcc.Graph(id='kmeans'),
                            html.H4('Características de los Clusters',
                                    style={'margin-top': '20px'}),
                            dash_table.DataTable(
                                id='kmeans-table',
                                columns=[{'name': col, 'id': col}
                                         for col in ['Cluster'] + columns],
                                data=[],
                                style_table={'overflowX': 'auto'},
                            ),
                            html.H3('Gráfico tridimensional Clusters', style={'margin-top': '20px'}),
                            dcc.Graph(id='kmeans_3d'),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ], style={'padding': '20px'}
)


@callback(
    Output('elbow_method', 'figure'),
    Input('elbow_method', 'id')
)
def update_graph(id):
    return elbow_method(data, columns)


@callback(
    [Output('kmeans', 'figure'),
     Output('kmeans-table', 'data')],
    [Input('kmeans', 'id')]
)
def update_kmeans(id):
    fig, table_data = kmeans_clustering(data, columns)
    return fig, table_data.to_dict('records')


@callback(
    Output('kmeans_3d', 'figure'),
    [Input('kmeans_3d', 'id')]
)
def update_kmeans_3d(id):
    return kmeans_clustering_3d(data, columns)
