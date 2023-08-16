# Public URL Microservice

This is a Flask microservice that provides an API endpoint to view the latest sensor log data. It connects to a MongoDB database to retrieve sensor logs based on provided parameters.

## Features

- Retrieve the latest sensor log data by specifying the sensor's unique ID.

## Getting Started

### 1.Clone the repository:

git clone https://github.com/your-username/publicurl.git
cd publicurl

### 2.Install the required dependencies:

pip install -r requirements.txt

### 3.Run the Flask app:
python app.py

### 4.Access the API:
Open a web browser or use curl to access the API endpoint:

http://127.0.0.1:5000/view/latest/sensor/data/public/?unique_id=<your_sensor_unique_id>


### 5.Dependencies
Flask
pymongo
gunicorn (for production deployment)