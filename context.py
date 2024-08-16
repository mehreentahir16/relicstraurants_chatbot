class ChatContext:
    def __init__(self):
        self.current_restaurant = None
        self.current_menu = None
        self.current_cuisine = None  # New attribute for tracking cuisine
        self.order_items = []
        self.user_preferences = {}

    def clear(self):
        self.current_restaurant = None
        self.current_menu = None
        self.current_cuisine = None  # Clear cuisine when resetting context
        self.order_items = []
        self.user_preferences = {}

    def update_restaurant(self, restaurant_name, menu=None, cuisine=None):
        self.current_restaurant = restaurant_name
        if menu:
            self.current_menu = menu
        if cuisine:
            self.current_cuisine = cuisine  # Update cuisine if provided

    def add_to_order(self, item_name):
        if self.current_menu:
            # Split the current_menu string into lines representing each menu item
            menu_lines = self.current_menu.split('\n')
            for line in menu_lines:
                # Each line should look like this: " - Item name ($price)"
                if item_name.lower() in line.lower():
                    # Extract the name and price
                    name_and_price = line.strip(" -").rsplit("(", 1)
                    item_name_from_menu = name_and_price[0].strip()
                    item_price = name_and_price[1].replace(")", "").strip("$")
                    
                    # Add to order items list
                    self.order_items.append({
                        "name": item_name_from_menu,
                        "price": float(item_price)
                    })
                    return  # Exit after adding to avoid duplicates
            # If the item is not found
            print(f"Item {item_name} not found in the menu.")
        else:
            print("No current menu found.")

    def __str__(self):
        return (f"Restaurant: {self.current_restaurant}, "
                f"Cuisine: {self.current_cuisine}, "  # Include cuisine in the string representation
                f"Order Items: {self.order_items}")
