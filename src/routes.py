# routes.py

from flask import request, render_template, json
from prometheus_client import metrics
from prometheus_flask_exporter import PrometheusMetrics
from src.analysis.full_analysis import compute_full_analysis
from src.data_collection.fetch_random_news_article import fetch_random_ctv_news_article_paragraphs, \
    fetch_random_aljazeeera_post_article_paragraphs, fetch_random_abcnews_post_article_paragraphs
from src.models.database import insert_analysis_results


def setup_routes(app):
    @app.route("/")
    def main():
        return render_template("index.html")

    @app.route("/text-analy", methods=["POST"])
    def process_input():
        # Get the selected option from the query parameters
        selected_option = request.args.get("selected_option")

        if selected_option == "text_input":
            # Handle large input option
            text_input = request.form.get("text_input", "")
            analysis_result = compute_full_analysis(text_input)
            insert_analysis_results({"text_input": text_input, "analysis_result": analysis_result})
            # Process the large input as needed
            return render_template("text-analysis.html", selected_option=selected_option, text_input=text_input,
                                   analysis_result=analysis_result)

        elif selected_option == "files_input":
            # Handle file upload
            uploaded_files = request.files.getlist("file_input")
            files_info = []
            analysis_results = {}
            for file in uploaded_files:
                # Process each uploaded file
                filename = file.filename
                file_size = len(file.read())
                # Add filename and file size to files_info list
                files_info.append({"filename": filename, "file_size": file_size})

                # Analyze content of each file
                file.seek(0)
                text_data = file.read().decode("utf-8")
                single_analysis_result = compute_full_analysis(text_data)
                analysis_results[filename] = single_analysis_result

            # perform an insert for each file input
            for filename, result in analysis_results.items():
                insert_analysis_results({"filename": filename, "analysis_result": result})

            # Render the echo page with the uploaded file information
            return render_template("text-analysis.html", selected_option=selected_option, files_info=files_info,
                                   analysis_results=analysis_results)
        elif selected_option == "news_article_sources":
            # Receive the news_article_sources submitted
            news_article_sources_value = request.form.get("news_article_sources")
            # Parse the JSON-like string to extract the name and URL
            selected_option_data = json.loads(news_article_sources_value)
            selected_name = selected_option_data["name"]
            selected_url = selected_option_data["url"]
            # print(news_article_sources_value)
            try:
                if selected_name == "CTV News":
                    article_text_data, article_link = fetch_random_ctv_news_article_paragraphs()
                elif selected_name == "ABC News":
                    article_text_data, article_link = fetch_random_abcnews_post_article_paragraphs()
                elif selected_name == "Al Jazeera":
                    article_text_data, article_link = fetch_random_aljazeeera_post_article_paragraphs()
                else:
                    return "Invalid news outlet source selected"

                analysis_result = compute_full_analysis(article_text_data)

                insert_analysis_results({"selected_name": selected_name, "selected_url": selected_url,
                                         "article_text_data": article_text_data, "analysis_result": analysis_result})

                return render_template("text-analysis.html", selected_option=selected_option,
                                       selected_name=selected_name,
                                       selected_url=selected_url, analysis_result=analysis_result,
                                       article_link=article_link)
            except Exception as e:
                return f"An error occurred with the fetch news article method: {str(e)}"
        else:
            # Handle other options (if any)
            return "Invalid option selected"

    @app.route("/metrics")
    def production_monitoring():
        return PrometheusMetrics(app).export()

    @app.route("/monitoring")
    def monitoring():
        return render_template("prometheus.html")
