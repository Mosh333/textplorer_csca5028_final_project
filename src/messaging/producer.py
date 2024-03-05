import os
import uuid
import pika
import json


def send_message_to_queue(selected_option, text_for_analysis, requestid: uuid.UUID):
    # Get the RabbitMQ connection URL from the environment variable
    rabbitmq_url = os.environ.get("CLOUDAMQP_URL")

    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    # Convert the dict to json string before sending, do not use str() or there will be a mismatch in the assert!!!
    message_data = {
        'selected_option': selected_option,
        "text_for_analysis": text_for_analysis,
        "requestid": str(requestid)
        # Convert UUID to hex string to perserve the uniqueness and allow consumer to reconstruct the UUID object
    }
    message_body = json.dumps(message_data)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message_body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )

    print(" [x] Sent %r" % message_body)

    connection.close()
