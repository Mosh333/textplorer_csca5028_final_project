# pretty hard to get linguistic methods to work perfectly (probably needs deep expertise),
# just my naive implementation for the sake of getting something implemented
# for the assignment
from typing import Tuple

from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re

# Download NLTK resources
# https://www.nltk.org/api/nltk.tokenize.punkt.html
nltk.download('punkt')
# https://www.nltk.org/search.html?q=stopwords
nltk.download('stopwords')
# https://www.nltk.org/howto/wordnet.html
nltk.download('wordnet')


def preprocess_text(text: str) -> str:
    # Remove special characters and digits
    processed_text = re.sub(r'\W+', ' ', text)
    processed_text = re.sub(r'\d+', '', processed_text)
    # Convert to lowercase
    processed_text = processed_text.lower()
    return processed_text


def remove_stopwords(text: str) -> str:
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)


def lemmatize_text(text: str) -> str:
    lemmatizer = WordNetLemmatizer()
    word_tokens = word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in word_tokens]
    return ' '.join(lemmatized_text)


def sentiment_emotion_analysis(text: str) -> Tuple[str, str]:
    # Preprocess text
    text = preprocess_text(text)
    # Remove stopwords
    text = remove_stopwords(text)
    # Lemmatize text
    text = lemmatize_text(text)

    # Perform sentiment analysis
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        sentiment = 'Positive'
    elif sentiment_score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    # Perform emotion analysis
    emotion = 'Positive' if sentiment_score > 0 else ('Negative' if sentiment_score < 0 else 'Neutral')

    return sentiment, emotion


def sentiment_domain_analysis(text: str) -> str:
    # Preprocess text
    text = preprocess_text(text)
    # Remove stopwords
    text = remove_stopwords(text)
    # Lemmatize text - simplifying words to their base English form found in dictionaries
    # to help provide clearer and accurate analysis of the input data
    # running -> run
    text = lemmatize_text(text)

    # List of domain categories
    # generated keywords for various categories using https://relatedwords.io/, https://relatedwords.org/, and
    # looking at each relevant sections of https://www.ctvnews.ca/ to find relevant words (also using my brain to
    # come up with relevant words)
    domain_categories = {
        'world news': [
            "diplomacy", "conflict", "negotiation", "humanitarian", "summit", "tsunami", "hurricane", "tornado",
            "pandemic", "election", "revolution", "democracy", "propaganda", "lies", "deception", "war", "battle",
            "authoritarianism", "weather forecast", "civil war", "sanctions", "earthquake", "coup", "hunger", "famine",
            "social media", "press freedom", "treaty", "emergency", "disease", "epidemic", "peacekeeping", "protests",
            "military", "disaster", "human rights", "climate change", "migration", "energy", "president",
            "prime minister", "geopolitics", "terrorism", "corruption", "crisis", "whistleblower", "international",
            "journalism", "bomb", "guns", "nuclear"
        ],
        'entertainment': [
            "celebrities", "movies", "music", "television", "actors", "drama", "comedy", "documentaries", "pop music",
            "rock music", "action", "horror", "romance", "blockbusters", "oscars", "emmys", "premiere", "concerts",
            "music festivals", "albums", "record labels", "dancing", "film festivals", "independent films", "superhero",
            "animation", "reality TV", "soap operas", "musicals", "streaming", "netflix", "amazon prime",
            "stand-up comedy", "talent shows", "game shows", "music videos", "music awards", "radio stations",
            "talk shows", "late-night shows", "animation", "virtual reality", "youtube", "podcasts", "audio books",
            "magazines", "photography", "fine arts"
        ],
        'politics': [
            "government", "election", "policy", "politician", "legislation", "president", "parliament", "cabinet",
            "corruption", "democracy", "authoritarianism", "transparency", "accountability", "freedom of speech",
            "press freedom", "censorship", "political unrest", "revolution", "civil rights", "lobbying", "party",
            "opposition", "bureaucracy", "law enforcement", "sanctions", "constitution", "foreign policy",
            "trade agreement", "diplomacy", "ambassador", "intelligence", "espionage", "classified information",
            "campaign", "voting", "referendum", "lobbyist", "activist", "human rights", "civil liberties",
            "constitutional rights", "separation of powers", "checks and balances", "electoral college", "swing states",
            "political parties"
        ],
        'lifestyle': [
            "health", "wellness", "fitness", "nutrition", "exercise", "diet", "mental health", "self-care",
            "meditation", "yoga", "sleep", "stress", "happiness", "mindfulness", "motivation", "positivity",
            "productivity", "lifestyle", "self-improvement", "personal development", "relationships", "family",
            "parenting", "marriage", "friendship", "love", "dating", "socializing", "communication", "hobbies",
            "interests", "passions", "creativity", "art", "music", "dance", "literature", "writing", "reading",
            "cooking", "baking", "gardening", "travel", "adventure", "exploration", "culture", "fashion", "style",
            "beauty"
        ],
        'business': [
            "economy", "finance", "market", "investment", "stocks", "bonds", "trading", "stock market",
            "financial market", "wall street", "business", "entrepreneurship", "startup", "small business",
            "corporation", "company", "industry", "sector", "growth", "profit", "revenue", "income", "expenses",
            "budget", "strategy", "management", "leadership", "executive", "ceo", "board of directors", "shareholder",
            "stakeholder", "partnership", "merger", "acquisition", "banking", "insurance", "real estate", "commerce",
            "trade", "globalization", "supply chain", "logistics", "manufacturing", "production", "innovation",
            "digital", "internet"
        ],
        'technology': [
            "innovation", "software", "hardware", "internet", "computer", "programming", "coding", "algorithm", "data",
            "analytics", "big data", "artificial intelligence", "machine learning", "deep learning", "automation",
            "robotics", "cybersecurity", "encryption", "privacy", "cloud computing", "networking", "social media",
            "digital marketing", "e-commerce", "website", "mobile app", "user experience", "interface",
            "virtual reality", "augmented reality", "blockchain", "cryptocurrency", "bitcoin", "ethereum",
            "smart contracts", "internet of things", "iot", "wearable technology", "biotechnology", "genetics",
            "nanotechnology", "quantum computing", "3D printing", "smart home", "smart city", "autonomous vehicles",
            "drones", "space exploration", "satellite technology", "iPhone", "technology", "computer"
        ],
        'sports': [
            "football", "basketball", "soccer", "tennis", "golf", "rugby", "cricket", "baseball", "hockey",
            "volleyball", "swimming", "cycling", "running", "marathon", "triathlon", "skiing", "snowboarding",
            "surfing", "skateboarding", "climbing", "boxing", "martial arts", "wrestling", "athletics",
            "track and field", "gymnastics", "figure skating", "weightlifting", "powerlifting", "bodybuilding",
            "extreme sports", "adventure sports", "motor sports", "formula 1", "nascar", "mma", "ufc", "sportsmanship",
            "teamwork", "competition", "championship", "olympics", "paralympics", "sports science", "sports medicine",
            "injury prevention", "rehabilitation", "coaching", "training", "fitness"
        ]
    }

    # Initialize domain category counts
    domain_counts = {category: 0 for category in domain_categories}

    # Count occurrences of domain-related keywords
    for word in word_tokenize(text):
        for category, keywords in domain_categories.items():
            if word in keywords:
                domain_counts[category] += 1

    if all(count == 0 for count in domain_counts.values()):
        return "Not categorized"

    # Categorize the domain based on keyword counts
    max_category = max(domain_counts, key=domain_counts.get)

    return max_category


# Example usage:
text = "The new international policies to control global warming is underway."
sentiment, emotion = sentiment_emotion_analysis(text)
domain_category = sentiment_domain_analysis(text)

print("Sentiment:", sentiment)
print("Emotion:", emotion)
print("Domain Category:", domain_category)
text = "The iPhone technology is being released soon which will revolutionize everything!"
sentiment, emotion = sentiment_emotion_analysis(text)
domain_category = sentiment_domain_analysis(text)

print("Sentiment:", sentiment)
print("Emotion:", emotion)
print("Domain Category:", domain_category)
text = "The iPhone technology is being released soon which will revolutionize smartphones forever!"
sentiment, emotion = sentiment_emotion_analysis(text)
domain_category = sentiment_domain_analysis(text)

print("Sentiment:", sentiment)
print("Emotion:", emotion)
print("Domain Category:", domain_category)
text = "My cat is like a fat cat that eat cat food. Bites me too."
sentiment, emotion = sentiment_emotion_analysis(text)
domain_category = sentiment_domain_analysis(text)

print("Sentiment:", sentiment)
print("Emotion:", emotion)
print("Domain Category:", domain_category)
