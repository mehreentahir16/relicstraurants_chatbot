from rapidfuzz import process, fuzz
from utils.format_utils import format_restaurant_info

def search_restaurants_by_cuisine(cuisine, flattened_data):
    results = []
    entries = flattened_data.split("\n\n")
    for entry in entries:
        if f"cuisine: {cuisine.lower()}" in entry.lower():
            restaurant_info = format_restaurant_info(entry)
            results.append(restaurant_info)
    if not results:
        return "No restaurants found for this cuisine." 
    return "\n\n".join(results)

def search_top_restaurants(flattened_data, limit=5):
    results = []
    entries = flattened_data.split("\n\n")
    for i in range(min(limit, len(entries))):
        restaurant_info = format_restaurant_info(entries[i])
        results.append(restaurant_info)
    return "\n\n".join(results)

def find_restaurant_by_name(query_name, flattened_data):
    entries = flattened_data.split("\n\n")
    restaurant_names = [entry.split("\n")[0].split(": ")[1].lower() for entry in entries]
    
    best_match, score, index = process.extractOne(query_name.lower(), restaurant_names, scorer=fuzz.partial_ratio)
    
    if score > 85:
        return restaurant_names[index]
    return None

def get_restaurant_info(restaurant_name, flattened_data):
    entries = flattened_data.split("\n\n")
    for entry in entries:
        if f"restaurant: {restaurant_name.lower()}" in entry.lower():
            return format_restaurant_info(entry)
    return "I couldn't find the restaurant you're looking for. Could you provide a different name or more details?"
