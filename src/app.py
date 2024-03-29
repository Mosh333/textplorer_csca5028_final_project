# app.py

from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
from src.routes import setup_routes

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Call the setup_routes function to register routes with the Flask app
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
