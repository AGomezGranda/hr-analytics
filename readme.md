# HR Analytics Application

## Description

HR Analytics is my Capstone project for my Bussiness Administration degree. It combines the knowledge I have acquired in the fields of Bussiness, Statistics and Computer Science.

This application is developed in Python and uses libraries like Plotly Dash, Numpy and Pandas. Also scikit-learn is used for the Machine Learning K-means clustering model.

## Project Abstract

In this project, a dashboard is developed and deployed through a web application that allows the statistical analysis of business data. Specifically, this work shows the application for the study of a company's HR database. This public and easily accessible application is developed using Python and allows the performance of a one-dimensional and two-dimensional analysis. In addition, the k-means clustering model, a machine learning technique, has been applied to extract relevant information.

## Access the Application

The application is hosted on AWS and can be accessed by clicking the link below:

[HR Analytics Application](http://34.245.20.6:8050/)

It has been deployed using Docker and AWS ECS Fargate.

## Installation

### Manual Installation

To install the application, follow the steps below:

1. Clone the repository:

    ```bash
    git clone https://github.com/agomezgranda/hr-analytics.git
    ```

2. Navigate to the project directory:

    ```bash
    cd hr-analytics
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

### Docker Installation

To install the application using Docker, follow the steps below:

1. Clone the repository:

    ```bash
    git clone
    ```

2. Navigate to the project directory:

    ```bash
    cd hr-analytics
    ```

3. Build the Docker image:

    ```bash
    docker build -t hr-analytics .
    ```

4. Run the Docker container:

    ```bash
    docker run -p 8050:8050 hr-analytics
    ```
