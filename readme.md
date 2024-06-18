# HR Analytics Application

## Description

HR Analytics is my Capstone project for my Bussiness Administration degree. It combines the knowledge I have acquired in the fields of Bussiness, Statistics and Computer Science.

This application is developed in Python and uses libraries like Plotly Dash, Numpy and Pandas. Also scikit-learn is used for the Machine Learning K-means clustering model.

## Access the Application

The application is hosted on AWS and can be accessed by clicking the link below:

[HR Analytics Application]()

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
