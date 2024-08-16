def format_restaurant_info(entry):
    lines = entry.split("\n")
    restaurant_name = lines[0].split(": ")[1]
    cuisine = lines[1].split(": ")[1]
    location = lines[2].split(": ")[1]
    opens = lines[3].split(", ")[0].split(": ")[1]
    closes = lines[3].split(", ")[1].split(": ")[1]
    rating = lines[4].split(", ")[0].split(": ")[1]
    price_level = lines[4].split(", ")[1].split(": ")[1]
    description = lines[-1].split(": ")[1]

    formatted_restaurant = (
        f"Restaurant: {restaurant_name}\n"
        f"Cuisine: {cuisine}\n"
        f"Location: {location}\n"
        f"Opens: {opens} | Closes: {closes}\n"
        f"Rating: {rating} | Price Level: {price_level}\n"
        f"Description: {description}\n"
    )
    return formatted_restaurant

def format_menu_info(entry):
    menu_line = [line for line in entry.split("\n") if line.startswith("Menu:")][0]
    menu_items = menu_line.split("Menu: ")[1].split(", ")
    formatted_menu = "Menu:\n" + "\n".join([f"  - {item}" for item in menu_items])
    return formatted_menu
