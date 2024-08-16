from utils.format_utils import format_menu_info

def get_menu(restaurant_name, flattened_data):
    entries = flattened_data.split("\n\n")
    for entry in entries:
        if f"restaurant: {restaurant_name.lower()}" in entry.lower():
            return format_menu_info(entry)
    return "No menu found for this restaurant."
