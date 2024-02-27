# will compute the basic_text_analysis, nlp_analysis, and sentiment_analysis
from decimal import Decimal
from typing import Dict, Any, Tuple, List
# Importing necessary functions from each module with relative paths
# Below are pretty much the database structure/definition to be stored in NoSQL
from src.analysis.basic_text_analysis import (
    word_count,
    num_characters_without_spaces,
    num_syllables,
    num_sentences,
    num_paragraphs,
    average_word_size,
    average_sentences_size,
    estimated_reading_time,
    top_n_words,
    get_difficulty_level
)
from src.analysis.sentiment_analysis import (
    sentiment_emotion_analysis,
    sentiment_domain_analysis
)
from src.analysis.nlp_analysis import (
    pos_tagging,
    ner
)


# return a dictionary of dictionary containing the basic text, sentiment, and nlp analysis
def compute_full_analysis(input_text: str) -> Dict[str, Dict[str, any]]:
    # Basic English text analysis
    basic_text_analysis_dict: Dict[str, Any] = {
        "word_count": word_count(input_text),
        "num_characters_without_spaces": num_characters_without_spaces(input_text),
        "num_syllables": num_syllables(input_text),
        "num_sentences": num_sentences(input_text),
        "num_paragraphs": num_paragraphs(input_text),
        "average_word_size": average_word_size(input_text),
        "average_sentences_size": average_sentences_size(input_text),
        "estimated_reading_time": estimated_reading_time(input_text),
        "top_n_words": top_n_words(input_text),
        "difficulty_level": get_difficulty_level(input_text)
    }

    # Sentiment analysis
    sentiment, emotion = sentiment_emotion_analysis(input_text)
    domain_category = sentiment_domain_analysis(input_text)
    sentiment_analysis_dict: Dict[str, Any] = {
        "sentiment": sentiment,
        "emotion": emotion,
        "domain_category": domain_category
    }

    # NLP Analysis
    pos_count_result: Dict[str, int] = pos_tagging(input_text)
    ner_result: List[Tuple[str, str]] = ner(input_text)
    nlp_analysis_dict: Dict[str, Any] = {
        "pos_count": pos_count_result,
        "ner": ner_result
    }

    # Convert float to Decimal type for DynamoDB compatibility
    for key, val in basic_text_analysis_dict.items():
        if isinstance(val, float):
            basic_text_analysis_dict[key] = Decimal(str(val))

    full_analysis_dict: Dict[str, Dict[str, Any]] = {
        "basic_text_analysis_dict": basic_text_analysis_dict,
        "sentiment_analysis_dict": sentiment_analysis_dict,
        "nlp_analysis_dict": nlp_analysis_dict
    }

    return full_analysis_dict

# Sample text for analysis
# sample_text = """
# A file system is a method an operating system uses to store, organize, and manage files and directories on a storage device.
# Some common types of file systems include: FAT (File Allocation Table): An older file system used by older versions of Windows and other operating systems.
# NTFS (New Technology File System): A modern file system used by Windows. It supports features such as file and folder permissions, compression, and encryption. ext (Extended File System):
# A file system commonly used on Linux and Unix-based operating systems. HFS (Hierarchical File System): A file system used by macOS. APFS (Apple File System):
# A new file system introduced by Apple for their Macs and iOS devices.
# """
#
# full_analysis_results: Dict[str, Dict[str, Any]] = compute_full_analysis(sample_text)
# print(full_analysis_results)
