# will compute the basic_text_analysis, nlp_analysis, and sentiment_analysis

import src.analysis.basic_text_analysis
import src.analysis.sentiment_analysis
import src.analysis.nlp_analysis


def process_text(text: str) -> int:
    # Count the number of words in the given text.
    words = text.split()

    return len(words)
