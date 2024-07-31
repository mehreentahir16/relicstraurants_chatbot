import json, time, random
import openai
from flask_session import Session
from flask import Flask, request, jsonify, render_template, session

import newrelic.agent

client = openai.OpenAI(api_key='OPENAI_API_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'  # Set a secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load the JSON data
with open('data/restaurants.json') as f:
    data = json.load(f)

# Helper function to search restaurants by cuisine
def search_restaurants(cuisine):
    start_time = time.time()
    time.sleep(2)  # Introduce a delay to mimic slow response
    newrelic.agent.add_custom_attribute("search_restaurants_delay", time.time() - start_time)
    filtered_restaurants = [restaurant for restaurant in data if cuisine.lower() in restaurant['cuisine'].lower()]
    return filtered_restaurants

# Helper function to get menu of a restaurant
def get_menu(restaurant_name):
    start_time = time.time()
    time.sleep(2)  # Introduce a delay to mimic slow response
    newrelic.agent.add_custom_attribute("get_menu_delay", time.time() - start_time)
    for restaurant in data:
        if restaurant_name.lower() in restaurant['name'].lower():
            return restaurant['menuItems']
    return []

# Function to place an order
def place_order(restaurant_name, dishes):
    return f"Order placed successfully for {dishes} from {restaurant_name}. Your food will be ready for pickup soon!"

# Function to interact with OpenAI API
def get_openai_response(prompt, history):
    messages = [{"role": "system", "content": "You are an AI assistant for Relicstaurants. Your role is to assist customers in browsing restaurants from the given data, providing information, and guiding them through the checkout process. Br friendly and concise in your response"}] + history + [{"role": "user", "content": prompt}]

    if any(keyword in prompt.lower() for keyword in ["dessert", "error"]):
        raise openai.error.OpenAIError("Simulated API failure for testing purposes.")
    else: 
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=250
        )
        return response.choices[0].message.content

@app.route('/')
def index():
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history = session.get('history', [])
    context = session.get('context', {})

    # Ensure the conversation history is updated
    history.append({"role": "user", "content": user_message})

    # Use OpenAI to determine intent and call appropriate function
    intent_prompt = f"Determine the user intent from the following message: '{user_message}'. The possible intents are: 'search_restaurants', 'get_menu', 'place_order', 'checkout', or 'general'. Respond only with the intent keyword."
    intent_response = get_openai_response(intent_prompt, history)
    intent = intent_response.strip().lower()

    response = ""
    if intent == "search_restaurants":
        cuisine = user_message.split("search")[1].strip()
        restaurants = search_restaurants(cuisine)
        if restaurants:
            response = f"Here are some {cuisine} restaurants:\n"
            for restaurant in restaurants:
                response += f"- {restaurant['name']} (Rating: {restaurant['rating']}, Price: {restaurant['price']})\n"
        else:
            response = f"Sorry, we couldn't find any {cuisine} restaurants."
        context['last_intent'] = 'search_restaurants'
        context['cuisine'] = cuisine
    elif intent == "get_menu":
        if 'restaurant' in context:
            restaurant_name = context['restaurant']
        else:
            restaurant_name = user_message.split("menu for")[1].strip()
        menu_items = get_menu(restaurant_name)
        if menu_items:
            response = f"Menu for {restaurant_name}:\n"
            for item in menu_items:
                response += f"- {item['name']}: ${item['price']}\n"
        else:
            response = "Sorry, we couldn't find the menu for that restaurant."
        context['last_intent'] = 'get_menu'
        context['restaurant'] = restaurant_name
    elif intent == "place_order":
        response = "To place an order, please provide the restaurant name and the items you'd like to order."
        context['last_intent'] = 'place_order'
    elif intent == "checkout":
        response = "To checkout, please confirm your order and provide your delivery address."
        context['last_intent'] = 'checkout'
    else:
        response = get_openai_response(user_message, history)
        context['last_intent'] = 'general'

    # Update conversation history and context
    history.append({"role": "assistant", "content": response})
    session['history'] = history
    session['context'] = context

    return jsonify({'response': response})

@app.route('/search_restaurants', methods=['POST'])
def search_restaurants_route():
    cuisine = request.json.get('cuisine')
    try:
        restaurants = search_restaurants(cuisine)
        response = {
            "status": "success",
            "restaurants": restaurants
        }
    except Exception as e:
        newrelic.agent.record_exception()  # Log the error in New Relic
        response = {
            "status": "error",
            "message": "Something went wrong while searching for restaurants. Please try again."
        }
    return jsonify(response)

@app.route('/get_menu', methods=['POST'])
def get_menu_route():
    restaurant_name = request.json.get('restaurant_name')
    try:
        menu = get_menu(restaurant_name)
        response = {
            "status": "success",
            "menu": menu
        }
    except Exception as e:
        newrelic.agent.record_exception()  # Log the error in New Relic
        response = {
            "status": "error",
            "message": "Something went wrong while fetching the menu. Please try again."
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)