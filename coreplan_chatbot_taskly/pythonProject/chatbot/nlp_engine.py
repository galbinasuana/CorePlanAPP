import re
import string
from collections import defaultdict
from difflib import SequenceMatcher
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

INTENT_KEYWORDS = {
    "workflow": ["workflow", "appointment", "schedule", "calendar", "meeting", "task"],
    "clients": ["client", "customer", "prospect", "crm", "follow up", "contacts"],
    "reminders": ["reminder", "alert", "missed", "notify", "check", "follow-up"],
    "reports": ["report", "sales", "progress", "overview", "status", "insight"],
    "suggestions": ["suggestion", "recommendation", "optimize", "tip", "strategy"],
    "notes": ["note", "log", "meeting", "record", "observation"],
    "tools": ["tool", "focus", "inactive", "utility", "feature"]
}

def preprocess(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    tokens = text.split()
    return [lemmatizer.lemmatize(token) for token in tokens]

def fuzzy_match(word, keyword):
    return SequenceMatcher(None, word, keyword).ratio() > 0.85

def detect_intent(user_input):
    tokens = preprocess(user_input)
    scores = defaultdict(int)

    for intent, keywords in INTENT_KEYWORDS.items():
        for token in tokens:
            for keyword in keywords:
                if token == keyword or fuzzy_match(token, keyword):
                    scores[intent] += 1

    if not scores:
        return "unknown"

    best_match = max(scores, key=scores.get)
    confidence = scores[best_match] / len(INTENT_KEYWORDS[best_match])

    if confidence < 0.3:
        return "unknown"

    return best_match
