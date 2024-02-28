# pretty hard to get linguistic methods to work perfectly (probably needs deep expertise),
# just my naive implementation for the sake of getting something implemented
# for the assignment
import string
from collections import Counter

import nltk
import textstat  # https://pypi.org/project/textstat/
from nltk.corpus import stopwords

# Download NLTK resources if these resources do not exist to avoid deployment issues in heroku system
if not nltk.data.find('tokenizers/punkt'):
    # https://www.nltk.org/api/nltk.tokenize.punkt.html
    nltk.download('punkt')
if not nltk.data.find('corpora/stopwords'):
    # https://www.nltk.org/search.html?q=stopwords
    nltk.download('stopwords')


def word_count(text: str) -> int:
    # Count the number of words in the given text.
    words = text.split()

    return len(words)


def num_characters_without_spaces(text: str) -> int:
    # replace spaces then count the characters
    return len(text.replace(" ", ""))


# inspiration from https://stackoverflow.com/a/46759549
def num_syllables(text: str) -> int:
    # conservative syllables counting since excluding 'y'
    syllable_count = 0
    # for sake of simplicity, will exclude 'y'
    vowels = "aeiou"
    text = text.lower()

    if text[0] in vowels:
        syllable_count += 1
    for index in range(1, len(text)):
        if text[index] in vowels and text[index - 1] not in vowels:
            syllable_count += 1
    if text.endswith('e'):
        syllable_count -= 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count


def num_sentences(text: str) -> int:
    sentence_endings = ['.', '!', '?']

    count_sentences = 0  # same as number of sentence endings

    for char in text:
        if char in sentence_endings:
            count_sentences += 1

    return max(1, count_sentences)


def num_paragraphs(text: str) -> int:
    # check if the text is empty
    if not text.strip():
        return 0
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    count_paragraphs = len(paragraphs)

    # make simplifying su
    return max(1, count_paragraphs)


# https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize
def average_word_size(text: str) -> float:
    words = nltk.word_tokenize(text)
    num_words = len(words)
    total_characters = sum(len(word) for word in words)
    if num_words > 0:
        return total_characters / num_words
    else:
        return 0


# https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize
def average_sentences_size(text: str) -> float:
    sentences = nltk.sent_tokenize(text)
    num_sentences = len(sentences)
    num_words = len(nltk.word_tokenize(text))
    if num_sentences > 0:
        return num_words / num_sentences
    else:
        return 0.0


# https://en.wikipedia.org/wiki/Silent_reading#Eye_movement_and_silent_reading_rate
def estimated_reading_time(text: str, words_per_minute: int = None) -> int:
    # do averaging arithmetic to compute the reading time assuming a normal adult reads 250 char per min

    if text is None or text == "":
        return 0

    if words_per_minute is None:
        words_per_minute = 250

    if words_per_minute <= 0:
        words_per_minute = 250

    words = nltk.word_tokenize(text)
    num_words = len(words)

    total_characters = 0
    for word in words:
        total_characters += len(word)

    if num_words > 0:
        average_word_size = total_characters / num_words
    else:
        average_word_size = 0

    reading_time = num_words * average_word_size / words_per_minute

    return round(reading_time)


def top_n_words(text: str, n: int = 5) -> list:
    # Remove punctuations then join back the string
    exclude_punctuation = set(string.punctuation) - {'-', "'", '_'}  # Exclude hyphen, apostrophe, and underscore
    text = ''.join(char for char in text if char not in exclude_punctuation).lower()

    words = nltk.word_tokenize(text)

    # Remove common words (stop words)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # https://docs.python.org/3/library/collections.html#collections.Counter
    word_freq = Counter(words)

    most_common_words = word_freq.most_common(n)

    return most_common_words


# https://pypi.org/project/textstat/
# https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
def get_difficulty_level(text: str) -> str:
    # Calculate the Flesh-Kincaid Grade Level
    grade_level = textstat.flesch_kincaid_grade(text)

    if grade_level < 6:
        return "Elementary"
    elif grade_level < 9:
        return "Middle School"
    elif grade_level < 13:
        return "High School"
    else:
        return "University"

# sample_text = """
# A file system is a method an operating system uses to store, organize, and manage files and directories on a storage device.
# Some common types of file systems include: FAT (File Allocation Table): An older file system used by older versions of Windows and other operating systems.
# NTFS (New Technology File System): A modern file system used by Windows. It supports features such as file and folder permissions, compression, and encryption. ext (Extended File System):
# A file system commonly used on Linux and Unix-based operating systems. HFS (Hierarchical File System): A file system used by macOS. APFS (Apple File System):
# A new file system introduced by Apple for their Macs and iOS devices.
# """
#
# # Test word_count
# print("Word Count:", word_count(sample_text))
#
# print("Number of Characters (excluding spaces):", num_characters_without_spaces(sample_text))
#
# print("Number of Syllables:", num_syllables(sample_text))
#
# print("Number of Sentences:", num_sentences(sample_text))
#
# print("Number of Paragraphs:", num_paragraphs(sample_text))
#
# print("Average Word Size:", average_word_size(sample_text))
#
# print("Average Sentence Size:", average_sentences_size(sample_text))
#
# print("Estimated Reading Time:", estimated_reading_time(sample_text), "minutes")
#
# top_words = top_n_words(sample_text)
# print("Top 5 Most Common Words:")
# for word, freq in top_words:
#     print(word, "-", freq)
#
# print("Difficulty Level:", get_difficulty_level(sample_text))
