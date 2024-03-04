import json
import unittest
import time
from src.messaging import consumer, producer
from src.messaging.consumer import receive_message_from_queue
from src.messaging.producer import send_message_to_queue


class TestMessaging(unittest.TestCase):
    def test_messaging(self):
        # Send a message to the queue
        selected_option = "option1"
        text_for_analysis = "This is a sample text"
        requestid = "12345"
        send_message_to_queue(selected_option, text_for_analysis, requestid)

        # Wait for a few seconds to ensure the message is processed
        time.sleep(2)

        # Receive the message from the queue
        received_message_bytes = receive_message_from_queue(selected_option, requestid)
        received_message = received_message_bytes.decode('utf-8')
        print(received_message)

        # Assert that the received message matches the sent message
        received_message_dict = json.loads(received_message)
        expected_message_dict = {
            "selected_option": selected_option,
            "text_for_analysis": text_for_analysis,
            "requestid": requestid
        }
        self.assertEqual(received_message_dict, expected_message_dict)


if __name__ == '__main__':
    unittest.main()
