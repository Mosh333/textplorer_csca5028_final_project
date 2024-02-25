# routes.py

from flask import request, render_template, json
from prometheus_client import metrics
from prometheus_flask_exporter import PrometheusMetrics


def setup_routes(app):
    @app.route("/")
    def main():
        return render_template("index.html")

    @app.route("/text-analy", methods=["POST"])
    def process_input_echo():
        # Get the selected option from the query parameters
        selected_option = request.args.get("selected_option")

        if selected_option == "text_input":
            # Handle large input option
            text_input = request.form.get("text_input", "")
            # Process the large input as needed
            return render_template("text-analysis.html", selected_option=selected_option, text_input=text_input)

        elif selected_option == "files_input":
            # Handle file upload
            uploaded_files = request.files.getlist("file_input")
            files_info = []
            for file in uploaded_files:
                # Process each uploaded file
                filename = file.filename
                file_size = len(file.read())
                # Add filename and file size to files_info list
                files_info.append({"filename": filename, "file_size": file_size})

            # Render the echo page with the uploaded file information
            return render_template("text-analysis.html", selected_option=selected_option, files_info=files_info)
        elif selected_option == "news_article_sources":
            # Receive the news_article_sources submitted
            news_article_sources_value = request.form.get("news_article_sources")
            # Parse the JSON-like string to extract the name and URL
            selected_option_data = json.loads(news_article_sources_value)
            selected_name = selected_option_data["name"]
            selected_url = selected_option_data["url"]
            # print(news_article_sources_value)
            return render_template("text-analysis.html", selected_option=selected_option, selected_name=selected_name,
                                   selected_url=selected_url)
        else:
            # Handle other options (if any)
            return "Invalid option selected"

    @app.route("/metrics")
    def production_monitoring():
        return PrometheusMetrics(app).export()

    @app.route("/monitoring")
    def monitoring():
        return render_template("prometheus.html")
