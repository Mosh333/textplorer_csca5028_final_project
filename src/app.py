# app.py

from flask import Flask
from routes import setup_routes

app = Flask(__name__)

# Call the setup_routes function to register routes with the Flask app
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
