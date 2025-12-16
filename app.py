import base64
import streamlit as st
from mock_db import init_mock_db, get_all_products
from agents import InventoryAgent, SalesAgent
from session_context import SessionContextManager


# ---------- SESSION FLAG ----------
if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False


# --------------------------------------------------
# 1. Setup
# --------------------------------------------------
st.set_page_config(page_title="ABFRL Agentic AI Demo", layout="wide")
init_mock_db()

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


#BG_IMAGE = get_base64_image("assets/Gemini_Generated_Image_sec3ygsec3ygsec3.png")
bg_image = get_base64_image("assets/Gemini_Generated_Image_sec3ygsec3ygsec3.png")

# ------------------- PERSISTENT SESSION -------------------
if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionContextManager()
session_manager = st.session_state.session_manager
SESSION_ID = "customer_001"

# --------------------------------------------------

# ---------------- WELCOME PAGE ----------------
# ---------------- WELCOME PAGE ----------------
if not st.session_state.show_main_app:
    st.markdown(f"""
        <style>
            .welcome-page {{
                background-image: url("data:image/jpg;base64,{bg_image}");
                background-size: cover;
                background-position: center;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: white;
                position: relative;
            }}

            .overlay {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.55);
            }}

            .content {{
                position: relative;
                z-index: 2;
                max-width: 800px;
            }}

            .content h1 {{
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 20px;
            }}

            .content p {{
                font-size: 1.4rem;
                margin-bottom: 40px;
            }}

            .stButton>button {{
                font-size: 1.2rem !important;
                padding: 14px 36px !important;
                border-radius: 14px !important;
                font-weight: 600 !important;
                background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
                color: white !important;
                border: none !important;
            }}

            .stButton>button:hover {{
                background: linear-gradient(90deg, #1d4ed8, #1e40af) !important;
            }}
        </style>

        <div class="welcome-page">
            <div class="overlay"></div>
            <div class="content">
                <h1>👋 Welcome to ABFRL Agentic AI Demo</h1>
                <p>Experience omnichannel retail AI with live inventory, conversational sales & smart cart</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Enter Demo"):
        st.session_state.show_main_app = True

    st.stop()




# 2. Styling / CSS
# --------------------------------------------------
st.markdown("""
<style>
html, body { background-color: #f5f7fb; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
h1 { font-size: 2.2rem !important; font-weight: 700 !important; color: #1f2937; }
h2, h3 { color: #111827; font-weight: 600; }

/* Product Card */
.product-card {
    background: white;
    padding: 14px;
    border-radius: 14px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.product-card:hover { transform: translateY(-4px); }
.product-name { font-size: 1.05rem; font-weight: 600; margin-top: 8px; }
.price { color: #16a34a; font-weight: 600; }

/* Cart Box */
.cart-box {
    background: #ffffff;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.07);
    margin-bottom: 16px;
}

/* Chat Box */
.chat-box {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
    font-weight: 600;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #1d4ed8, #1e40af);
}

/* Urgency Cards (Dashboard) */
.critical { border-left: 5px solid #ff4b4b; background-color: #ffecec; color: #8b0000; padding: 10px; border-radius: 5px; font-weight: 500; }
.warning { border-left: 5px solid #ffa500; background-color: #fff8e6; color: #856404; padding: 10px; border-radius: 5px; font-weight: 500; }
.normal { border-left: 5px solid #4caf50; background-color: #e8f5e9; color: #155724; padding: 10px; border-radius: 5px; font-weight: 500; }

img { width: 100%; border-radius: 5px; }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. Sidebar Controls
# --------------------------------------------------
st.sidebar.title("🛠️ Simulation Controls")

# Channel Switch
st.sidebar.markdown("### 🧭 Channel Switch")
if st.sidebar.button("📱 Mobile App"): session_manager.switch_channel(SESSION_ID, "Mobile App")
if st.sidebar.button("🏬 In-Store Kiosk"): session_manager.switch_channel(SESSION_ID, "In-Store Kiosk")
if st.sidebar.button("💬 WhatsApp"): session_manager.switch_channel(SESSION_ID, "WhatsApp")
st.sidebar.markdown("---")

# Viral Spike / Reset
if st.sidebar.button("💥 Trigger Viral Spike (Manga)"):
    st.session_state.inventory_db["SKU-104"]["active_carts"] = 100
    st.session_state.inventory_db["SKU-104"]["online_stock"] = 1
    st.toast("🚨 Manga Viral Spike Activated!")

if st.sidebar.button("🔄 Reset Data"):
    del st.session_state["inventory_db"]
    st.rerun()

# --------------------------------------------------
# 4. Main UI
# --------------------------------------------------
st.title("🤖 Retail Agentic AI Prototype")
tab1, tab2 = st.tabs(["📊 Demand Sensing Dashboard (Internal)", "💬 Customer Chat (External)"])

# --------------------------------------------------
# TAB 1 — DASHBOARD
# --------------------------------------------------
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
                    st.image(item["img"])
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

# --------------------------------------------------
# TAB 2 — CUSTOMER CHAT + CART + PRODUCTS
# --------------------------------------------------

with tab2:
    st.markdown("### 🧠 Live Session Context")
    st.json(session_manager.get_session(SESSION_ID))

    # ---------- LIVE CART BADGE ----------
    cart_items = session_manager.get_session(SESSION_ID)["cart"]
    cart_count = len(cart_items)
    st.markdown(f"""
    <div style='display:flex; align-items:center; justify-content:space-between; background:#ffffff; padding:12px 16px; border-radius:14px; box-shadow:0 6px 20px rgba(0,0,0,0.07); margin-bottom:16px;'>
        <div style='font-weight:600; font-size:1.2rem;'>🛒 Your Cart</div>
        <div style='background:#2563eb; color:white; padding:4px 12px; border-radius:12px; font-weight:600;'>{cart_count} item{'s' if cart_count!=1 else ''}</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- CART ITEMS ----------
    with st.container():
        st.markdown("<div class='cart-box'>", unsafe_allow_html=True)
        if cart_items:
            for item in cart_items:
                st.markdown(f"✔ **{item}**")
        else:
            st.markdown("🛍️ _Your cart is empty_")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PRODUCTS ----------
    st.markdown("### 🧾 Products")
    products = get_all_products()
    cols = st.columns(3)
    for idx, (sku, item) in enumerate(products.items()):
        with cols[idx % 3]:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.image(item["img"], use_container_width=True)
            st.markdown(f"<div class='product-name'>{item['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price'>₹{item.get('price', 1999)}</div>", unsafe_allow_html=True)
            if st.button("🛒 Add to Cart", key=sku):
                session_manager.add_to_cart(SESSION_ID, item["name"])
                st.toast(f"{item['name']} added to cart")
            st.markdown("</div>", unsafe_allow_html=True)


    # ---------- CHAT ----------
    st.markdown("### 💬 Chat")
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("What are you looking for?"):
        session_manager.get_session(SESSION_ID)["intent"] = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        bot = SalesAgent()
        response = bot.chat(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.markdown(response)

    st.markdown("</div>", unsafe_allow_html=True)
