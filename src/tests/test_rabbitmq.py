import json
import unittest
import time
from collections import Counter
from decimal import Decimal
from uuid import UUID

from src.messaging import consumer, producer
from src.messaging.consumer import receive_message_from_queue
from src.messaging.producer import send_message_to_queue


class TestMessaging(unittest.TestCase):
    def test_messaging(self):
        # Send a message to the queue
        selected_option = "text_input"
        text_for_analysis = "This is a sample text"
        input_requestid = UUID('123c4567-b69b-12d3-a456-123456784000')
        send_message_to_queue(selected_option, text_for_analysis, input_requestid)

        # Wait for a few seconds to ensure the message is processed
        time.sleep(2)

        # Receive the message from the queue
        received_message_dict = receive_message_from_queue(selected_option, input_requestid)
        # received_message = received_message_bytes.decode('utf-8')
        print(received_message_dict)

        expected_message_dict = {
            'basic_text_analysis_dict': {'word_count': 5, 'num_characters_without_spaces': 17, 'num_syllables': 6,
                                         'num_sentences': 1, 'num_paragraphs': 1, 'average_word_size': Decimal('3.4'),
                                         'average_sentences_size': Decimal('5.0'), 'estimated_reading_time': 0,
                                         'top_n_words': [('sample', 1), ('text', 1)], 'difficulty_level': 'Elementary'},
            'sentiment_analysis_dict': {'sentiment': 'Neutral', 'emotion': 'Neutral',
                                        'domain_category': 'Not categorized'},
            'nlp_analysis_dict': {'pos_count': Counter({'DT': 2, 'VBZ': 1, 'JJ': 1, 'NN': 1}), 'ner': []}}
        self.assertEqual(received_message_dict, expected_message_dict)


if __name__ == '__main__':
    unittest.main()
