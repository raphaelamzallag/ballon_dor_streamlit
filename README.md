# Ballon d'Or Streamlit App

This project visualizes statistics for 5 of the top 2024 Ballon d'Or contenders using a Streamlit web application.

## Prerequisites

- Docker (if you want to run the app in a container)
- Python 3.9 (if you want to run the app locally)
- pip (Python package installer)

## Running the App Locally

1. Clone the repository:

    ```sh
    git clone https://github.com/raphaelamzallag/ballon_dor_streamlit
    cd ballon_dor_streamlit
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

4. Open your web browser and go to `http://localhost:8501` to view the app.

## Running the App in a Docker Container

1. Clone the repository:

    ```sh
    git clone https://github.com/raphaelamzallag/ballon_dor_streamlit
    cd ballon_dor_streamlit
    ```

2. Build the Docker image:

    ```sh
    docker build -t ballon-dor-streamlit .
    ```

3. Run the Docker container:

    ```sh
    docker run -p 8501:8501 ballon-dor-streamlit
    ```

4. Open your web browser and go to `http://localhost:8501` to view the app.

## Project Structure

- `app.py`: Main application file.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Docker configuration file.
- `player_stats`: CSV of the Data used for the streamlit.
- `get_data.ipynb`: Notebook to get data from API.
