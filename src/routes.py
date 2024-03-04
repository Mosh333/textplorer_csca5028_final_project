# routes.py
import datetime
import os
import uuid

import boto3
from flask import request, render_template, json, jsonify, current_app
from prometheus_client import metrics
from prometheus_flask_exporter import PrometheusMetrics
from src.analysis.full_analysis import compute_full_analysis
from src.data_collection.fetch_random_news_article import fetch_random_ctv_news_article_paragraphs, \
    fetch_random_aljazeeera_post_article_paragraphs, fetch_random_abcnews_post_article_paragraphs
from src.messaging.producer import send_message_to_queue
from src.messaging.consumer import receive_message_from_queue
from src.models.database import insert_analysis_results, fetch_database_info


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
            requestid = uuid.uuid4()

            # analysis_result = compute_full_analysis(text_input)
            # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # insert_analysis_results(
            #     {"text_input": text_input, "analysis_result": analysis_result, "timestamp": timestamp}, requestid)
            #
            # return render_template("text-analysis.html", selected_option=selected_option, text_input=text_input,
            #                        analysis_result=analysis_result, requestid=str(requestid))

            # offload the computation heavy workload to rabbitmq's producer end
            send_message_to_queue(selected_option, text_input, requestid)

            # consumer end will be invoked in the following route:
            # @app.route("/consumer/<selected_option>-<requestid>", methods=["GET"])
            # def perform_offloaded_computation(selected_option, requestid):
            # frontend code (text-analysis.html and render_data.js will poll via ajax to get the data from this route)
            # will dynamically render the data

            return render_template("text-analysis.html", selected_option=selected_option, text_input=text_input,
                                   requestid=str(requestid))

        elif selected_option == "files_input":
            # Handle file upload
            uploaded_files = request.files.getlist("file_input")
            files_info = []
            analysis_results = {}
            requestid_list = {}

            for file in uploaded_files:
                # Process each uploaded file
                filename = file.filename
                file_size = len(file.read())
                file.seek(0)
                text_data = file.read().decode("utf-8")
                # Add filename and file size to files_info list
                files_info.append({"filename": filename, "file_size": file_size, "text_content": text_data})

                # Analyze content of each file
                single_analysis_result = compute_full_analysis(text_data)
                analysis_results[filename] = single_analysis_result

                # Generate the requestid and pass it along
                requestid_list[filename] = uuid.uuid4()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_analysis_results(
                    {"filename": filename, "analysis_result": single_analysis_result, "timestamp": timestamp},
                    requestid_list[filename])

            print(analysis_results)
            # Render the echo page with the uploaded file information
            return render_template("text-analysis.html", selected_option=selected_option, files_info=files_info,
                                   analysis_results=analysis_results, requestid_list=requestid_list)
        elif selected_option == "news_article_sources":
            # Receive the news_article_sources submitted
            news_article_sources_value = request.form.get("news_article_sources")
            # Parse the JSON-like string to extract the name and URL
            selected_option_data = json.loads(news_article_sources_value)
            selected_name = selected_option_data["name"]
            selected_url = selected_option_data["url"]
            requestid = uuid.uuid4()
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
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                insert_analysis_results({"selected_name": selected_name, "selected_url": selected_url,
                                         "article_text_data": article_text_data, "analysis_result": analysis_result,
                                         "timestamp": timestamp}, requestid)

                return render_template("text-analysis.html", selected_option=selected_option,
                                       selected_name=selected_name,
                                       selected_url=selected_url, analysis_result=analysis_result,
                                       article_link=article_link)
            except Exception as e:
                return f"An error occurred with the fetch news article method: {str(e)}"
        else:
            # Handle other options (if any)
            return "Invalid option selected"

    @app.route("/consumer/<selected_option>/<requestid>", methods=["GET"])
    def perform_offloaded_computation(selected_option, requestid):
        # this route will ensure consumer.py will be invoked and provide the requested data via the frontend polling
        try:
            # selected_option = request.args.get('selected_option')
            # requestid = request.args.get('requestid')

            # Access the values of selected_option and requestid here
            print("from perform_offloaded_computation(), what is selected_option?: ", selected_option)
            print("from perform_offloaded_computation(), what is requestid?: ", requestid)

            analysis_result = receive_message_from_queue(selected_option, requestid)
            print("from perform_offloaded_computation(), what is analysis_result?: ", analysis_result)
            if selected_option == "text_input":
                if analysis_result is None:
                    print("here1")
                    return jsonify({"status": "in_progress"})
                else:
                    print("here2")
                    return jsonify({"status": "complete", "analysis_result": analysis_result})
            elif selected_option == "files_input":
                print("Received files_input in perform_offloaded_computation")
                # Add your handling for files_input here
            elif selected_option == "news_article_sources":
                print("Received news_article_sources in perform_offloaded_computation")
                # Add your handling for news_article_sources here
            else:
                return jsonify({"error": "Unsupported selected option"}), 400
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {e}")
            # Return an error response
            return jsonify({"error": str(e)}), 500

    @app.route("/metrics")
    def production_monitoring():
        return PrometheusMetrics(app)  # .export()

    @app.route('/health_check')
    def health_check():
        health_status = application_is_healthy(current_app)
        if health_status["status"] == "ok":
            return jsonify(health_status)
        else:
            return jsonify(health_status), 500

    # Please note the below only works locally, for production monitoring, I have used Better Uptime's Better Stack
    # monitoring tool
    @app.route("/monitoring")
    def monitoring():
        return render_template("prometheus.html")

    @app.route("/database_info")
    def database_info():
        # looks like {'database_table_name': dynamodb_table, 'aws_region': aws_region, 'total_rows_data': count}
        database_dict = fetch_database_info()

        return render_template("database_info.html", database_dict=database_dict)


def application_is_healthy(flask_app):
    try:
        # Check database connection
        dynamodb = boto3.client('dynamodb',
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                region_name=os.getenv('AWS_REGION'))

        # List tables to check if the connection is successful
        tables = dynamodb.list_tables()

        # Check if the list_tables operation succeeded
        if 'TableNames' in tables:
            # Use Flask test client to check route accessibility
            with flask_app.test_client() as client:
                # Check if the "/" route is accessible
                response_root = client.get("/")
                response_database_info = client.get("/database_info")

                # Check if the responses are successful (status code 200)
                if response_root.status_code == 200 and response_database_info.status_code == 200:
                    return {"status": "ok"}
                else:
                    return {"status": "error", "message": "Failed to access one or more routes"}
        else:
            return {"status": "error", "message": "Failed to connect to the database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
