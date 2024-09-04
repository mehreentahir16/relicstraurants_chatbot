import os
import openai
from flask_session import Session
from flask import Flask, request, jsonify, render_template, session
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent

from context import ChatContext
from services.restaurant_service import search_restaurants_by_cuisine, search_top_restaurants, find_restaurant_by_name, get_restaurant_info
from services.menu_service import get_menu
from services.order_service import handle_add_to_cart
from utils.intent_classifier import classify_intent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

file = "data/restaurants.txt"
with open(file, "r") as f:
    flattened_data = f.read().strip()

tools = [
    Tool(name="search_restaurants_by_cuisine", func=lambda cuisine: search_restaurants_by_cuisine(cuisine, flattened_data), description="Use this tool when the user wants to find restaurants based on a specific cuisine, like Mexican, Italian, African, etc."),
    Tool(name="search_top_restaurants", func=lambda: search_top_restaurants(flattened_data), description="Use this tool when user wants to find restaurants without specifying a particular cuisine."),
    Tool(name="get_restaurant_info", func=lambda name: get_restaurant_info(name, flattened_data), description="Use this tool when the user asks for information about a specific restaurant."),
    Tool(name="get_menu", func=lambda name: get_menu(name, flattened_data), description="Use this tool when the user asks for the menu of a specific restaurant.")
]

def create_agent():
    llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=api_key)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)
    return agent

agent = create_agent()

def get_chat_context():
    if 'chat_context' not in session:
        session['chat_context'] = ChatContext()
    return session['chat_context']

# Function to get OpenAI response
def get_openai_response(prompt, history):
    messages = [{"role": "system", "content": "You are an AI assistant for Relicstaurants. Your role is to assist customers in browsing restaurants from the given data, providing information, and guiding them through the checkout process. Be friendly and concise in your response."}] + history + [{"role": "user", "content": prompt}]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=250
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        return "Something went wrong while generating a response. Please try again."

@app.route('/')
def index():
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    history = session.get('history', [])
    chat_context = get_chat_context()
    history.append({"role": "user", "content": user_message})

    try:
        intent = classify_intent(user_message, client)
        if intent == 'search_restaurants':
            response = agent.run(f"Search for restaurants with cuisine: {user_message}")
            chat_context.clear()
        elif intent == 'get_restaurant_info':
            restaurant_name = find_restaurant_by_name(user_message, flattened_data)
            if restaurant_name:
                response = get_openai_response(user_message, history)
                chat_context.update_restaurant(restaurant_name)
            else:
                response = "Sorry, I couldn't find the restaurant you're asking for."
        elif intent == 'get_menu':
            if chat_context.current_restaurant:
                response = agent.run(f"Get menu for restaurant: {chat_context.current_restaurant}")
            else:
                restaurant_name = find_restaurant_by_name(user_message, flattened_data)
                if restaurant_name:
                    response = agent.run(f"Get menu for restaurant: {restaurant_name}")
                    chat_context.update_restaurant(restaurant_name, get_menu(restaurant_name, flattened_data))
                else:
                    response = "Please specify the restaurant name to get the menu."
        elif intent == 'add_to_cart':
            if chat_context.current_restaurant:
                response = handle_add_to_cart(user_message, chat_context)
            else:
                response = "Please specify the restaurant name first."
        elif intent == 'place_order':
            if chat_context.order_items:
                order_summary = ", ".join([f"{item['name']} (${item['price']})" for item in chat_context.order_items])
                total_amount = sum([item['price'] for item in chat_context.order_items])
                response = (f"As an AI-based chatbot, I cannot place the order for you. However, "
                            f"I can tell you that you have the following items in your cart: {order_summary}. "
                            f"The total amount is ${total_amount:.2f}. Please proceed to checkout on the Relicstraunts website.")
            else:
                response = "Your cart is empty. Please select a restaurant and specify items to add them to your cart."
        else:
            response = get_openai_response(user_message, history)

    except Exception as e:
        response = "There was an error while generating a response. Please try again."

    # Update conversation history
    history.append({"role": "assistant", "content": response})
    session['history'] = history

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
