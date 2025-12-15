import streamlit as st

# --- WORKER AGENT: INVENTORY ---
class InventoryAgent:
    """
    [Source: 290] Checks real-time stock and calculates demand urgency.
    """
    def check_stock_status(self, sku):
        db = st.session_state.inventory_db
        item = db.get(sku)
        
        if not item:
            return None

        # Logic for Demand Sensing (The "Smart" Feature)
        status = "NORMAL"
        insight_msg = "Stock levels optimal."
        
        # Scenario 1: High Urgency
        if item["active_carts"] > item["online_stock"] * 2 and item["online_stock"] > 0:
            status = "CRITICAL_DEMAND"
            insight_msg = f"🔥 Velocity Alert: {item['active_carts']} carts vs {item['online_stock']} stock."
            
        # Scenario 2: Omnichannel Rescue
        elif item["online_stock"] == 0 and item["store_stock"] > 0:
            status = "OMNICHANNEL_OPP"
            insight_msg = "📍 Online Sold Out. Redirect to Store available."
            
        return {
            "sku": sku,
            "name": item["name"],
            "online": item["online_stock"],
            "store": item["store_stock"],
            "carts": item["active_carts"],
            "status": status,
            "insight": insight_msg
        }

# --- MASTER AGENT: SALES ORCHESTRATOR ---
class SalesAgent:
    """
    [Source: 289] Manages conversation and uses persuasive psychology.
    """
    def __init__(self):
        self.inventory_tool = InventoryAgent()

    def chat(self, user_input):
        # simple keyword matching for the demo
        user_input = user_input.lower()
        
        if "red" in user_input or "dress" in user_input:
            return self._generate_response("SKU-101")
        elif "blue" in user_input or "jacket" in user_input:
            return self._generate_response("SKU-102")
        elif "white" in user_input or "tee" in user_input:
            return self._generate_response("SKU-103")
        elif "manga" in user_input or "piece" in user_input:
            return self._generate_response("SKU-104")
        elif "sneaker" in user_input or "shoes" in user_input:
            return self._generate_response("SKU-105")
        else:
            return "I can help you shop! We have a Red Dress, Blue Jacket, and White Tee. Which one interests you?"

    def _generate_response(self, sku):
        # Orchestration: Call the Worker Agent
        data = self.inventory_tool.check_stock_status(sku)
        
        # Persuasive Logic [Source: 297]
        if data["status"] == "CRITICAL_DEMAND":
            return (
                f"**{data['name']}**: Great choice! ⚠️ **Honest heads-up:** \n\n"
                f"This is trending *hard* right now. My system sees **{data['carts']} people have it in their cart**, "
                f"but we only have **{data['online']} left**. I'd recommend checking out now!"
            )
        
        elif data["status"] == "OMNICHANNEL_OPP":
            return (
                f"**{data['name']}**: It looks like this just sold out online. 😔 \n\n"
                f"BUT! Good news — I checked local inventory and found **{data['store']} available at the Downtown Store**. "
                f"Shall I reserve one for you for 'Click & Collect'?"
            )
        
        else:
            return f"**{data['name']}**: We have plenty in stock! It's a best-seller. Shall I add it to your cart?"