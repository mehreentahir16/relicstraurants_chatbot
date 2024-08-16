import openai

def classify_intent(user_message, client):
    prompt = f"Determine the user intent from the following message: '{user_message}'. The possible intents are: 'search_restaurants', 'get_restaurant_info', 'get_menu', 'add_to_cart', 'place_order', or 'general'. Respond only with the intent keyword."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()
