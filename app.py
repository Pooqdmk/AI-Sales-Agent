import base64
import streamlit as st
from mock_db import init_mock_db, get_all_products
from agents import InventoryAgent, SalesAgent
from session_context import SessionContextManager

# --------------------------------------------------
# 1. HELPER FUNCTIONS
# --------------------------------------------------

# FIX: Return HTML as one single line to prevent "Code Block" rendering errors
def get_product_tile(item_name):
    initials = item_name[:2].upper()
    colors = [
        ("linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%)", "#d63384"),
        ("linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)", "#6f42c1"),
        ("linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)", "#0c9567"),
        ("linear-gradient(135deg, #fccb90 0%, #d57eeb 100%)", "#b74b1e"),
        ("linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)", "#4a69bd"),
    ]
    bg_gradient, text_color = colors[len(item_name) % len(colors)]
    
    # COMPACT HTML STRING (No newlines, no indentation)
    return f'<div style="width:100%; height:140px; background-image:{bg_gradient}; border-radius:12px; margin-bottom:12px; display:flex; align-items:center; justify-content:center; color:{text_color}; font-weight:800; font-size:28px; letter-spacing:2px; box-shadow:inset 0 0 20px rgba(255,255,255,0.3);">{initials}</div>'

def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return "" 

# --------------------------------------------------
# 2. SETUP & CONFIGURATION
# --------------------------------------------------
st.set_page_config(page_title="ABFRL Agentic AI Demo", layout="wide")
init_mock_db()

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionContextManager()
session_manager = st.session_state.session_manager
SESSION_ID = "customer_001"

if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False

# --------------------------------------------------
# 3. CSS STYLING
# --------------------------------------------------
st.markdown("""
<style>
html, body { background-color: #f5f7fb; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Product Card */
.product-card {
    background: white;
    padding: 10px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}
.product-name { font-size: 1rem; font-weight: 600; margin-top: 8px; color: #1f2937; }
.price { color: #16a34a; font-weight: 700; font-size: 1.1rem; }

/* Cart & Chat Box */
.cart-box { background: #ffffff; padding: 16px; border-radius: 14px; box-shadow: 0 6px 20px rgba(0,0,0,0.07); margin-bottom: 16px; }
.chat-box { background: white; padding: 16px; border-radius: 14px; box-shadow: 0 6px 18px rgba(0,0,0,0.06); margin-top: 20px; }

/* Urgency Alerts */
.critical { border-left: 5px solid #ff4b4b; background-color: #ffecec; color: #8b0000; padding: 10px; border-radius: 5px; font-weight: 600; }
.warning { border-left: 5px solid #ffa500; background-color: #fff8e6; color: #856404; padding: 10px; border-radius: 5px; font-weight: 600; }
.normal { border-left: 5px solid #4caf50; background-color: #e8f5e9; color: #155724; padding: 10px; border-radius: 5px; font-weight: 600; }

.stButton>button { width: 100%; border-radius: 10px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 4. WELCOME PAGE
# --------------------------------------------------
if not st.session_state.show_main_app:
    bg_b64 = get_base64_image("assets/Gemini_Generated_Image_sec3ygsec3ygsec3.png")
    st.markdown(f"""
        <style>
            .welcome-page {{
                background-image: url("data:image/jpg;base64,{bg_b64}");
                background-size: cover; height: 100vh; display: flex; flex-direction: column;
                justify-content: center; align-items: center; text-align: center; color: white;
            }}
            .overlay {{ background: rgba(0, 0, 0, 0.6); padding: 50px; border-radius: 20px; }}
            h1 {{ font-size: 3rem; margin-bottom: 10px; color: white !important; }}
            p {{ font-size: 1.5rem; margin-bottom: 30px; }}
        </style>
        <div class="welcome-page">
            <div class="overlay">
                <h1>👋 ABFRL Agentic Retail AI</h1>
                <p>Omnichannel Sales • Live Inventory • Smart Demand Sensing</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Launch Demo System"):
            st.session_state.show_main_app = True
            st.rerun()
    st.stop()

# --------------------------------------------------
# 5. SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.title("🛠️ Simulation Controls")

st.sidebar.markdown("### 🧭 Channel Switch")
if st.sidebar.button("📱 Mobile App"): 
    session_manager.switch_channel(SESSION_ID, "Mobile App")
    st.rerun()
if st.sidebar.button("🏬 In-Store Kiosk"): 
    session_manager.switch_channel(SESSION_ID, "In-Store Kiosk")
    st.rerun()
if st.sidebar.button("💬 WhatsApp"):
    session_manager.switch_channel(SESSION_ID, "WhatsApp")
    st.rerun()

st.sidebar.markdown("### ⚡ Live Events")
if st.sidebar.button("💥 Trigger Viral Spike (Manga)"):
    st.session_state.inventory_db["SKU-104"]["active_carts"] = 100
    st.session_state.inventory_db["SKU-104"]["online_stock"] = 1
    st.toast("🚨 Manga Viral Spike Activated!")

if st.sidebar.button("🔄 Reset Database"):
    del st.session_state["inventory_db"]
    st.rerun()

# --------------------------------------------------
# 6. MAIN APPLICATION
# --------------------------------------------------
st.title("🤖 Retail Agentic AI Prototype")
tab1, tab2 = st.tabs(["📊 Demand Sensing Dashboard (Internal)", "💬 Customer Chat (External)"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### Agent Insights: Live Inventory & Demand Analysis")
    agent = InventoryAgent()
    products = get_all_products()
    items = list(products.items())

    for i in range(0, len(items), 3):
        cols = st.columns(3)
        for idx, (sku, item) in enumerate(items[i:i+3]):
            analysis = agent.check_stock_status(sku)
            with cols[idx]:
                with st.container(border=True):
                    # 1. Use clean Tile HTML
                    tile_html = get_product_tile(item['name'])
                    st.markdown(tile_html, unsafe_allow_html=True)

                    st.markdown(f"### {item['name']}")
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Online", item["online_stock"])
                    c2.metric("Store", item["store_stock"])
                    c3.metric("Carts", item["active_carts"])
                    
                    if analysis["status"] == "CRITICAL_DEMAND":
                        st.markdown(f"<div class='critical'>🔥 {analysis['insight']}</div>", unsafe_allow_html=True)
                    elif analysis["status"] == "OMNICHANNEL_OPP":
                        st.markdown(f"<div class='warning'>📍 {analysis['insight']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='normal'>✅ {analysis['insight']}</div>", unsafe_allow_html=True)

# --- TAB 2: CUSTOMER VIEW ---
with tab2:
    st.markdown("### 🧠 Live Session Context")
    st.json(session_manager.get_session(SESSION_ID))

    # --- CART ---
    cart_items = session_manager.get_session(SESSION_ID)["cart"]
    cart_count = len(cart_items)
    
    st.markdown(f"""
    <div style='display:flex; align-items:center; justify-content:space-between; background:#ffffff; padding:12px 16px; border-radius:14px; box-shadow:0 6px 20px rgba(0,0,0,0.07); margin-bottom:16px;'>
        <div style='font-weight:600; font-size:1.2rem;'>🛒 Your Cart</div>
        <div style='background:#2563eb; color:white; padding:4px 12px; border-radius:12px; font-weight:600;'>{cart_count} item{'s' if cart_count!=1 else ''}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='cart-box'>", unsafe_allow_html=True)
        if cart_items:
            for idx, item_name in enumerate(cart_items):
                c1, c2 = st.columns([0.85, 0.15])
                with c1: st.markdown(f"**{item_name}**")
                with c2:
                    if st.button("❌", key=f"rm_{idx}"):
                        session_manager.remove_from_cart(SESSION_ID, item_name)
                        st.rerun()
        else:
            st.markdown("🛍️ _Your cart is empty_")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- PRODUCTS GRID ---
    st.markdown("### 🧾 Products")
    products = get_all_products()
    prod_cols = st.columns(3)
    
    for idx, (sku, item) in enumerate(products.items()):
        with prod_cols[idx % 3]:
            
            # 1. Get Clean HTML
            tile_html = get_product_tile(item['name'])
            
            # 2. Render Card (NO INDENTATION in HTML string)
            st.markdown(f"""<div class='product-card'>
{tile_html}
<div class='product-name'>{item['name']}</div>
<div class='price'>₹{item.get('price', 1999)}</div>
</div>""", unsafe_allow_html=True)
            
            if st.button("🛒 Add", key=f"add_{sku}"):
                session_manager.add_to_cart(SESSION_ID, item["name"])
                st.toast(f"{item['name']} added to cart")
                st.rerun()
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # --- CHAT ---
    st.markdown("### 💬 Chat")
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about products..."):
        session_manager.get_session(SESSION_ID)["intent"] = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        bot = SalesAgent()
        response = bot.chat(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.markdown(response)
    
    st.markdown("</div>", unsafe_allow_html=True)