class SessionContextManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "channel": "Mobile App",
                "cart": [],
                "intent": ""
            }
        return self.sessions[session_id]

    def switch_channel(self, session_id, new_channel):
        self.get_session(session_id)["channel"] = new_channel

    def add_to_cart(self, session_id, item):
        self.get_session(session_id)["cart"].append(item)

    # ✅ NEW: Remove item from cart
    def remove_from_cart(self, session_id, item):
        cart = self.get_session(session_id)["cart"]
        if item in cart:
            cart.remove(item)

    # ✅ NEW: Clear cart after checkout
    def clear_cart(self, session_id):
        self.get_session(session_id)["cart"] = []
