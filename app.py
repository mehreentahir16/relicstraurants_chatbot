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
    time.sleep(2)  # Introduce a delay to mimic slow response
    filtered_restaurants = [restaurant for restaurant in data if cuisine.lower() in restaurant['cuisine'].lower()]
    return filtered_restaurants

# Helper function to get menu of a restaurant
def get_menu(restaurant_name):
    time.sleep(2)  # Introduce a delay to mimic slow response
    for restaurant in data:
        if restaurant_name.lower() in restaurant['name'].lower():
            return restaurant['menuItems']
    return []

# Mock function to place an order
def place_order(restaurant_name, dishes):
    return f"Order placed successfully for {dishes} from {restaurant_name}. Your food will be ready for pickup soon!"

# Function to interact with OpenAI API
def get_openai_response(prompt, history):
    messages = [{"role": "system", "content": "You are an AI assistant for Relicstaurants. Your role is to assist customers in browsing restaurants from the given data, providing information, and guiding them through the checkout process. Br friendly and concise in your response"}] + history + [{"role": "user", "content": prompt}]

    if random.random() < 0.3:
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
    
    # Ensure the conversation history is updated
    history.append({"role": "user", "content": user_message})
    
    try:
        response = get_openai_response(user_message, history)
    except Exception as e:
        # newrelic.agent.record_exception()  # Log the error in New Relic
        response = "There was an error while generating response. Please try again."
    
    # Basic fallback for not finding specific cuisines or dishes
    if "couldn't find any restaurants" in response.lower():
        response += " However, we have other cuisines available. Would you like to try Italian, Mexican, or Chinese?"

    # Update conversation history
    history.append({"role": "assistant", "content": response})
    session['history'] = history

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