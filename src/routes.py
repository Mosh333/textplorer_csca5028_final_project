# routes.py

from flask import request, redirect, url_for, render_template


def setup_routes(app):
    @app.route("/")
    def main():
        return render_template("index.html")

    @app.route("/echo_user_input", methods=["POST"])
    def echo_input():
        # Get the input from the form fields
        input_text = request.form.get("user_input", "")
        file_input = request.files.get("file_input")
        textarea_input = request.form.get("textarea_input", "")

        # Process the input
        file_size = len(file_input.read()) if file_input else 0  # Get the size of the uploaded file in bytes

        # Render the echo page with the input values
        return render_template("echo.html", input_text=input_text, file_size=file_size, textarea_input=textarea_input)
