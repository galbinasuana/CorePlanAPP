from nlp_engine import detect_intent
from intent_router import route_message

def get_bot_response(user_input):
    intent = detect_intent(user_input)
    return route_message(intent)
