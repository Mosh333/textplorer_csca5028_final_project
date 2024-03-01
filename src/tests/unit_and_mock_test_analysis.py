import unittest
from collections import Counter
from unittest.mock import patch

from src.analysis import basic_text_analysis, full_analysis, nlp_analysis, sentiment_analysis


class TestBasicTextAnalysis(unittest.TestCase):

    def setUp(self) -> None:
        self.sample_text = """
        A file system is a method an operating system uses to store, organize, and manage files and directories on a storage device.
        Some common types of file systems include: FAT (File Allocation Table): An older file system used by older versions of Windows and other operating systems.
        NTFS (New Technology File System): A modern file system used by Windows. It supports features such as file and folder permissions, compression, and encryption. ext (Extended File System):
        A file system commonly used on Linux and Unix-based operating systems. HFS (Hierarchical File System): A file system used by macOS. APFS (Apple File System):
        A new file system introduced by Apple for their Macs and iOS devices.    
        """

    def test_word_count(self):
        self.assertEqual(basic_text_analysis.word_count(self.sample_text), 113)

    def test_num_characters_without_spaces(self):
        self.assertEqual(basic_text_analysis.num_characters_without_spaces(self.sample_text), 590)

    def test_num_syllables(self):
        self.assertEqual(basic_text_analysis.num_syllables(self.sample_text), 193)

    def test_num_sentences(self):
        self.assertEqual(basic_text_analysis.num_sentences(self.sample_text), 7)

    def test_num_paragraphs(self):
        self.assertEqual(basic_text_analysis.num_paragraphs(self.sample_text), 1)

    def test_average_word_size(self):
        self.assertAlmostEqual(basic_text_analysis.average_word_size(self.sample_text), 4.17, delta=0.01)

    def test_average_sentences_size(self):
        self.assertAlmostEqual(basic_text_analysis.average_sentences_size(self.sample_text), 20.0, delta=0.01)

    def test_estimated_reading_time(self):
        self.assertAlmostEqual(basic_text_analysis.estimated_reading_time(self.sample_text), 2.00, delta=0.01)

    def test_top_n_words(self):
        expected_top_words = [('file', 13), ('system', 11), ('used', 4), ('operating', 3), ('systems', 3)]
        self.assertEqual(basic_text_analysis.top_n_words(self.sample_text), expected_top_words)

    def test_get_difficulty_level(self):
        self.assertEqual(basic_text_analysis.get_difficulty_level(self.sample_text), "High School")


class TestNLPAnalysis(unittest.TestCase):
    def setUp(self):
        # Sample text for testing
        self.sample_text = "Google is currently earning record breaking revenue despite hard times."

    def test_pos_tagging(self):
        expected_pos_counts = Counter({'NN': 3, 'NNP': 1, 'VBZ': 1, 'RB': 1,
                                       'VBG': 1, 'IN': 1, 'JJ': 1, 'NNS': 1, '.': 1})
        self.assertEqual(nlp_analysis.pos_tagging(self.sample_text), expected_pos_counts)

    def test_ner(self):
        expected_named_entities = [('GPE', 'Google')]
        self.assertEqual(nlp_analysis.ner(self.sample_text), expected_named_entities)


class TestSentimentAnalysis(unittest.TestCase):

    # Perform mock testing with TextBlob objects
    @patch('src.analysis.sentiment_analysis.TextBlob')
    def test_sentiment_emotion_analysis_positive(self, mock_TextBlob):
        mock_TextBlob.return_value.sentiment.polarity = 0.5
        sentiment, emotion = sentiment_analysis.sentiment_emotion_analysis("I love this!")
        self.assertEqual(sentiment, 'Positive')
        self.assertEqual(emotion, 'Positive')

    @patch('src.analysis.sentiment_analysis.TextBlob')
    def test_sentiment_emotion_analysis_negative(self, mock_TextBlob):
        mock_TextBlob.return_value.sentiment.polarity = -0.5
        sentiment, emotion = sentiment_analysis.sentiment_emotion_analysis("I hate this!")
        self.assertEqual(sentiment, 'Negative')
        self.assertEqual(emotion, 'Negative')

    @patch('src.analysis.sentiment_analysis.TextBlob')
    def test_sentiment_emotion_analysis_neutral(self, mock_TextBlob):
        mock_TextBlob.return_value.sentiment.polarity = 0.0
        sentiment, emotion = sentiment_analysis.sentiment_emotion_analysis("This is okay.")
        self.assertEqual(sentiment, 'Neutral')
        self.assertEqual(emotion, 'Neutral')

    def test_sentiment_domain_analysis_politics(self):
        text = "Government officials announced new policies today."
        domain_category = sentiment_analysis.sentiment_domain_analysis(text)
        self.assertEqual(domain_category, 'politics')

    def test_sentiment_domain_analysis_entertainment(self):
        text = "Taylor Swift ranked the most popular artist releases a new music video in 2023."
        domain_category = sentiment_analysis.sentiment_domain_analysis(text)
        self.assertEqual(domain_category, 'entertainment')

    def test_sentiment_domain_analysis_technology(self):
        text = "The new smartphone features cutting-edge technology."
        domain_category = sentiment_analysis.sentiment_domain_analysis(text)
        self.assertEqual(domain_category, 'technology')

    def test_sentiment_domain_analysis_not_categorized(self):
        text = "I went for a walk in the park."
        domain_category = sentiment_analysis.sentiment_domain_analysis(text)
        self.assertEqual(domain_category, 'Not categorized')


class TestFullAnalysis(unittest.TestCase):
    @patch('src.analysis.full_analysis.word_count', return_value=50)
    @patch('src.analysis.full_analysis.num_characters_without_spaces', return_value=200)
    @patch('src.analysis.full_analysis.num_syllables', return_value=100)
    @patch('src.analysis.full_analysis.num_sentences', return_value=5)
    @patch('src.analysis.full_analysis.num_paragraphs', return_value=3)
    @patch('src.analysis.full_analysis.average_word_size', return_value=4.0)
    @patch('src.analysis.full_analysis.average_sentences_size', return_value=10.0)
    @patch('src.analysis.full_analysis.estimated_reading_time', return_value=2)
    @patch('src.analysis.full_analysis.top_n_words', return_value=[('file', 3), ('system', 2)])
    @patch('src.analysis.full_analysis.get_difficulty_level', return_value='High School')
    @patch('src.analysis.full_analysis.sentiment_emotion_analysis', return_value=('Positive', 'Positive'))
    @patch('src.analysis.full_analysis.sentiment_domain_analysis', return_value='Technology')
    @patch('src.analysis.full_analysis.pos_tagging', return_value={'NN': 3, 'VBZ': 1})
    @patch('src.analysis.full_analysis.ner', return_value=[('GPE', 'Google')])
    def test_compute_full_analysis(self, mock_word_count, mock_num_chars, mock_num_syllables, mock_num_sentences,
                                   mock_num_paragraphs, mock_avg_word_size, mock_avg_sentences_size,
                                   mock_reading_time, mock_top_n_words, mock_difficulty_level, mock_sentiment_emotion,
                                   mock_sentiment_domain, mock_pos_tagging, mock_ner):
        sample_text = "Sample text for analysis"
        expected_result = {
            "basic_text_analysis_dict": {
                "word_count": 50,
                "num_characters_without_spaces": 200,
                "num_syllables": 100,
                "num_sentences": 5,
                "num_paragraphs": 3,
                "average_word_size": 4.0,
                "average_sentences_size": 10.0,
                "estimated_reading_time": 2,
                "top_n_words": [('file', 3), ('system', 2)],
                "difficulty_level": 'High School'
            },
            "sentiment_analysis_dict": {
                "sentiment": 'Positive',
                "emotion": 'Positive',
                "domain_category": 'Technology'
            },
            "nlp_analysis_dict": {
                "pos_count": {'NN': 3, 'VBZ': 1},
                "ner": [('GPE', 'Google')]
            }
        }
        result = full_analysis.compute_full_analysis(sample_text)
        self.assertEqual(result, expected_result)


# Good practice to include this in unit test files.
if __name__ == '__main__':
    unittest.main()
