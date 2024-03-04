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

            print('We are definitely returning the follow: ', analysis_result)
            return analysis_result
        except Exception as e:
            logger.error("Error processing message: %s", e)
            return None
    elif selected_option == "files_input":
        print("Selected Option:", selected_option)
        print("Request ID:", requestid)
        print("Text for Analysis:", text_for_analysis)
    elif selected_option == "news_article_sources":
        print("Selected Option:", selected_option)
        print("Request ID:", requestid)
        print("Text for Analysis:", text_for_analysis)
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
