import streamlit as st

def init_mock_db():
    if "inventory_db" not in st.session_state:
        st.session_state.inventory_db = {
            "SKU-101": {
                "name": "Red Silk Dress",
                "price": 4500,
                "img": "https://via.placeholder.com/300/8B0000/FFFFFF?text=Red+Dress",
                "online_stock": 5,        
                "store_stock": 2,         
                "active_carts": 32,       
                "description": "Elegant evening wear, perfect for parties."
            },
            "SKU-102": {
                "name": "Blue Denim Jacket",
                "price": 2500,
                "img": "https://via.placeholder.com/300/00008B/FFFFFF?text=Denim+Jacket",
                "online_stock": 0,        
                "store_stock": 15,        
                "active_carts": 3,
                "description": "Classic rugged denim for casual outings."
            },
            "SKU-103": {
                "name": "White Cotton Tee",
                "price": 999,
                "img": "https://via.placeholder.com/300/FFFFFF/000000?text=White+Tee",
                "online_stock": 100,      
                "store_stock": 50,
                "active_carts": 5,
                "description": "Breathable summer essential."
            },
            # --- NEW ITEMS ADDED BELOW ---
            "SKU-104": {
                "name": "One Piece Manga Vol. 105",
                "price": 499,
                "img": "https://via.placeholder.com/300/FFA500/000000?text=Manga+Vol+105",
                "online_stock": 3,        # Very Low
                "store_stock": 0,         # None in store
                "active_carts": 45,       # EXTREME DEMAND (Viral Item)
                "description": "Latest volume, best-seller."
            },
            "SKU-105": {
                "name": "Air Retro Sneakers",
                "price": 12000,
                "img": "https://via.placeholder.com/300/333333/FFFFFF?text=Sneakers",
                "online_stock": 0,        
                "store_stock": 1,         # Only 1 left in store!
                "active_carts": 12,
                "description": "Limited edition street wear."
            },
             "SKU-106": {
                "name": "Digital Smart Watch",
                "price": 5999,
                "img": "https://via.placeholder.com/300/1C1C1C/FFFFFF?text=Smart+Watch",
                "online_stock": 200,      # Healthy
                "store_stock": 100,
                "active_carts": 15,
                "description": "Tracks heart rate and steps."
            }
        }

def get_product(sku):
    return st.session_state.inventory_db.get(sku)

def get_all_products():
    return st.session_state.inventory_db