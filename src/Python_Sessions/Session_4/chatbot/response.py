import json
import random

# Load responses from JSON file
with open('new.json', 'r', encoding='utf-8') as file:
    responses = json.load(file)

# Function to get a response based on user input
def get_response(user_input):
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
   
    return random.choice(responses["default"])