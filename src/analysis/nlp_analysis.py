# pretty hard to get linguistic methods to work perfectly (probably needs deep expertise),
# just my naive implementation for the sake of getting something implemented
# for the assignment

import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Download NLTK resources
# https://www.nltk.org/api/nltk.tokenize.punkt.html
nltk.download('punkt')  # for tokenization

# https://www.nltk.org/_modules/nltk/tag/perceptron.html
# https://www.kaggle.com/datasets/nltkdata/averaged-perceptron-tagger
nltk.download('averaged_perceptron_tagger')  # for part of speech tagging

# https://www.nltk.org/_modules/nltk/chunk.html
# https://www.kaggle.com/datasets/nltkdata/maxent-ne-chunker
nltk.download('maxent_ne_chunker')  # for name entity relationship

nltk.download('words')  # for list of common English words


# if above does not work, see the download outputs from nltk.download("all")
# to see name changes from the documentation or worst case look at source code


# Unfortunately was not able to get spacy running since it was hard :(
# https://spacy.io/usage/spacy-101

# POS tagging
# https://www.nltk.org/book/ch05.html
def pos_tagging(text: str) -> dict:
    # Parts of speech, count instances of POS tags

    # Break it up into token of words
    words = word_tokenize(text)

    # Do the POS tagging
    pos_tags = nltk.pos_tag(words)

    pos_counts = Counter(tag for word, tag in pos_tags)

    return pos_counts

    # https://docs.python.org/3/library/collections.html#collections.Counter


# NER
# https://www.nltk.org/book/ch07.html

def ner(text: str) -> list:
    # Break it up into token of words
    words = word_tokenize(text)

    # Perform NEW
    tagged_words = nltk.pos_tag(words)
    ner_result = nltk.ne_chunk(tagged_words)

    # Extract named entities
    named_entities = []
    # Loop through each chunk in the NER result
    for chunk in ner_result:
        # Check if the chunk has a 'label' attribute to conclude that it is a named entity (ne_chunk labels it)
        if hasattr(chunk, 'label'):
            # print(chunk)
            # Create a tuple containing the label and the joined text of the chunk
            entity_text = ' '.join(c[0] for c in chunk)
            named_entities.append((chunk.label(), entity_text))

    return named_entities

# text = "Google is currently earning record breaking revenue despite hard times."
#
# # Perform POS tagging
# pos_counts_result = pos_tagging(text)
# print("POS Counts:", pos_counts_result)
#
# ner_result = ner(text)
# print("Named Entities:", ner_result)
