from rapidfuzz import fuzz

def get_order_items(user_message, menu):
    menu_items = [line.split(" ($")[0].strip() for line in menu.split('\n') if line.strip()]
    order_items = []

    for item in menu_items:
        if fuzz.partial_ratio(item.lower(), user_message.lower()) > 80:
            order_items.append(item)

    return order_items

def handle_add_to_cart(user_message, chat_context):
    if chat_context.current_restaurant:
        order_items = get_order_items(user_message, chat_context.current_menu)

        if order_items:
            for item in order_items:
                chat_context.add_to_order(item)
            order_summary = ", ".join([f"{item['name']} (${item['price']})" for item in chat_context.order_items])
            response = f"The following items have been added to your cart: {order_summary}."
        else:
            response = "I couldn't find the items in the menu. Please specify the exact items you want to order."
    else:
        response = "Please specify the restaurant name to place an order."

    return response
