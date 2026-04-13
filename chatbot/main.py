import random

print("Bot: Hello. I am your intelligent assistant.")
print("Bot: You can talk to me about general things. Type 'exit' to quit.\n")

# Memory
user_profile = {
    "name": None,
    "last_intent": None,
    "mood": None
}

# Response database
responses = {
    "greeting": ["Hello.", "Hi there.", "Greetings."],
    "ask_user": ["How are you doing today?", "How is your day going?"],
    "positive": ["That is good to hear.", "Glad things are going well."],
    "negative": ["That sounds difficult.", "I hope things improve soon."],
    "purpose": ["I simulate conversation using rule-based logic and pattern matching."],
    "creator": ["I was developed as part of an AI internship project."],
    "help": ["You can ask about my purpose, introduce yourself, or have a simple conversation."],
    "thanks": ["You are welcome.", "Glad I could assist."],
    "fallback": ["I did not fully understand that.", "Could you clarify your question?"]
}

# Keyword groups (synonym handling)
keywords = {
    "greeting": ["hi", "hello", "hey"],
    "positive": ["good", "fine", "great", "awesome"],
    "negative": ["bad", "sad", "tired", "upset", "stress"],
    "purpose": ["what can you do", "purpose", "function"],
    "creator": ["who created you", "who made you"],
    "help": ["help", "assist"],
    "thanks": ["thank", "thanks"]
}

def detect_intent(user_input):
    """Detect intent using keyword + pattern matching"""

    # Name pattern
    if "my name is" in user_input:
        return "name"

    # Check keyword groups
    for intent, words in keywords.items():
        for word in words:
            if word in user_input:
                return intent

    # Special patterns
    if "how are you" in user_input:
        return "ask_bot"

    return "unknown"


def handle_response(intent, user_input):
    """Generate response based on intent + context"""

    # Name storing
    if intent == "name":
        name = user_input.replace("my name is", "").strip()
        user_profile["name"] = name
        return "Nice to meet you, " + name + "."

    # Greeting
    elif intent == "greeting":
        if user_profile["name"]:
            return "Hello " + user_profile["name"] + "."
        return random.choice(responses["greeting"])

    # Ask bot status
    elif intent == "ask_bot":
        user_profile["last_intent"] = "ask_bot"
        return "I am functioning properly. " + random.choice(responses["ask_user"])

    # Positive sentiment
    elif intent == "positive":
        user_profile["mood"] = "positive"
        return random.choice(responses["positive"])

    # Negative sentiment
    elif intent == "negative":
        user_profile["mood"] = "negative"
        return random.choice(responses["negative"])

    elif intent == "purpose":
        return random.choice(responses["purpose"])

    elif intent == "creator":
        return random.choice(responses["creator"])

    elif intent == "help":
        return random.choice(responses["help"])
    
    elif intent == "thanks":
        return random.choice(responses["thanks"])

    elif intent == "unknown":
        if user_profile["last_intent"] == "ask_bot":
            return "You mentioned your day. Would you like to tell me more about it?"
        if user_profile["mood"] == "negative":
            return "If you want, you can share more about what is bothering you."
        return random.choice(responses["fallback"])


# Main loop
while True:
    user_input = input("You: ").lower().strip()

    if user_input in ["exit", "bye", "quit"]:
        print("Bot: Conversation ended. Take care.")
        break

    intent = detect_intent(user_input)
    response = handle_response(intent, user_input)

    print("Bot:", response)
