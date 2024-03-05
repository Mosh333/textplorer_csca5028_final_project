import datetime
import json
import os
import time
import uuid

import pika
import logging

from src.analysis.full_analysis import compute_full_analysis
from src.data_collection.fetch_random_news_article import fetch_random_ctv_news_article_paragraphs, \
    fetch_random_aljazeeera_post_article_paragraphs, fetch_random_abcnews_post_article_paragraphs
from src.models.database import insert_analysis_results, fetch_database_info

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_message(message_data):
    # Extract selected_option, requestid, and text_for_analysis
    # print("pikachu")
    selected_option = message_data.get("selected_option")
    requestid_str = message_data.get("requestid")
    requestid = uuid.UUID(requestid_str)
    text_for_analysis = message_data.get("text_for_analysis")

    # Perform heavy computation based on the received message
    # For example, analyze the text_for_analysis data

    # Placeholder for heavy computation
    # ...
    if selected_option == "text_input":
        # Print the extracted data
        print("Selected Option:", selected_option)
        print("Request ID:", requestid)
        print("Text for Analysis:", text_for_analysis)
        try:
            analysis_result = compute_full_analysis(text_for_analysis)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # must send requestid as uuid.UUID not str
            insert_analysis_results(
                {"text_input": text_for_analysis, "analysis_result": analysis_result, "timestamp": timestamp},
                requestid)

            print('We are definitely returning the following: ', analysis_result)
            return analysis_result
        except Exception as e:
            logger.error("Error processing message: %s", e)
            return None
    elif selected_option == "files_input":
        # files_info looks like:
        # {dict1, dict2, dict3...}
        # where each dict looks like: {"filename": filename, "file_size": file_size, "text_content": text_data}
        # Print the extracted data
        analysis_results = {}
        files_info = message_data.get("text_for_analysis")

        print("Selected Option:", selected_option)
        print("Request ID:", requestid)
        print("Text for Analysis:", files_info)

        # Analyze contents of all the files
        for filename, file_info in files_info.items():
            text_content = file_info["text_content"]
            file_size = file_info["file_size"]
            # Analyze content of the given file
            single_analysis_result = compute_full_analysis(text_content)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            analysis_results[filename] = {
                "analysis_result": single_analysis_result,
                "text_content": text_content,
                "file_size": file_size,
                "timestamp": timestamp
            }
            insert_analysis_results(
                {"filename": filename, "analysis_result": single_analysis_result, "timestamp": timestamp},
                uuid.uuid4())

        print('We are definitely returning the following &&&&&&&&&&&&&&&&&&&&&&&&&&&&&: ')
        # add the bundle requestid identifier
        analysis_results['request_id'] = requestid
        return analysis_results
    elif selected_option == "news_article_sources":
        # Print the extracted data
        print("Selected Option:", selected_option)
        print("Request ID:", requestid)
        news_article_sources_value = text_for_analysis
        print("News Article Source to grab text:", news_article_sources_value)
        # Parse the JSON-like string to extract the name and URL
        selected_option_data = json.loads(news_article_sources_value)
        selected_name = selected_option_data["name"]
        selected_url = selected_option_data["url"]
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
            analysis_result["selected_name"] = selected_name
            analysis_result["selected_url"] = selected_url
            analysis_result["article_text_data"] = article_text_data
            analysis_result["article_link"] = article_link
            print('We are definitely returning the following: ', analysis_result)
            return analysis_result
        except Exception as e:
            logger.error("Error processing message: %s", e)
            return None
    else:
        # Handle other options (if any)
        logger.error("Invalid option selected: %s", selected_option)
        return None

    # Return the result of the computation
    logger.error("One of the three options were not invoked. Investigate issue.")
    return None


def receive_message_from_queue(selected_option, requestid):
    # Get the RabbitMQ connection URL from the environment variable
    rabbitmq_url = os.environ.get("CLOUDAMQP_URL")
    logger.info("Attempting to return the data from rabbitmq!!!")
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    method_frame, header_frame, body = channel.basic_get(queue='task_queue')

    if method_frame:
        print(" [x] Received %r" % body)
        # Decode the JSON message
        message_data = json.loads(body)

        # Process the message and perform necessary heavy computation
        analysis_result_data = process_message(message_data)

        channel.basic_ack(method_frame.delivery_tag)

        # either analysis_result or analysis_results depending on selected_option
        return analysis_result_data
    else:
        print('No message returned')

    connection.close()
    return None  # if not successful

# def receive_message_from_queue(selected_option, requestid_hex):
#     # Get the RabbitMQ connection URL from the environment variable
#     rabbitmq_url = os.environ.get("CLOUDAMQP_URL")
#     logger.info("Attempting to return the data from RabbitMQ!!!")
#     connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
#     channel = connection.channel()
#
#     channel.queue_declare(queue='task_queue', durable=True)
#
#     # Convert the requestid_hex string to a UUID object
#     requestid = uuid.UUID(hex=requestid_hex)
#
#     # Continuously retrieve messages until a message with the specified requestid is found
#     while True:
#         method_frame, header_frame, body = channel.basic_get(queue='task_queue')
#
#         if method_frame:
#             print(" [x] Received %r" % body)
#             # Decode the JSON message
#             message_data = json.loads(body)
#
#             # Check if the requestid matches the specified requestid
#             if message_data.get("requestid") == str(requestid):
#                 # Process the message and perform necessary heavy computation
#                 analysis_result_data = process_message(message_data)
#
#                 # Acknowledge the message
#                 channel.basic_ack(method_frame.delivery_tag)
#
#                 # Return the result of processing the message
#                 return analysis_result_data
#             else:
#                 # If the requestid doesn't match, requeue the message
#                 channel.basic_nack(method_frame.delivery_tag)
#         else:
#             # If no message is returned, break out of the loop
#             print('No message returned')
#             break
#
#         time.sleep(7)
#
#     # Close the connection
#     connection.close()
#     return None  # if not successful
