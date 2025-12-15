import streamlit as st
from mock_db import init_mock_db, get_all_products
from agents import InventoryAgent, SalesAgent

# 1. Setup
st.set_page_config(page_title="ABFRL Agentic AI Demo", layout="wide")
init_mock_db()


st.markdown("""
<style>
    /* 1. Fix the Urgency Text Color (Darker Text on Light Background) */
    .critical { 
        border-left: 5px solid #ff4b4b; 
        background-color: #ffecec; 
        color: #8b0000;  /* Dark Red Text */
        padding: 10px; 
        border-radius: 5px; 
        font-weight: 500;
    }
    
    .warning { 
        border-left: 5px solid #ffa500; 
        background-color: #fff8e6; 
        color: #856404; /* Dark Gold/Brown Text */
        padding: 10px; 
        border-radius: 5px;
        font-weight: 500;
    }
    
    .normal { 
        border-left: 5px solid #4caf50; 
        background-color: #e8f5e9; 
        color: #155724; /* Dark Green Text */
        padding: 10px; 
        border-radius: 5px;
        font-weight: 500;
    }

    /* 2. Fix the Empty Space at the Top of Cards */
    /* This removes the extra padding Streamlit puts inside columns */
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0px;
    }
    
    /* Make images fill the width nicely */
    img {
        width: 100%;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    /* Headers inside cards */
    h3 {
        margin-top: -10px !important;
        padding-top: 0px !important;
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Controls
st.sidebar.title("🛠️ Simulation Controls")

if st.sidebar.button("💥 Trigger Viral Spike (Manga)"):
    st.session_state.inventory_db["SKU-104"]["active_carts"] = 100
    st.session_state.inventory_db["SKU-104"]["online_stock"] = 1
    st.toast("🚨 Manga Viral Spike Activated!")

if st.sidebar.button("🔄 Reset Data"):
    del st.session_state["inventory_db"]
    st.rerun()

# 3. Main UI
st.title("🤖 Retail Agentic AI Prototype")
tab1, tab2 = st.tabs(["📊 Demand Sensing Dashboard (Internal)", "💬 Customer Chat (External)"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.markdown("### Agent Insights: Live Inventory & Demand Analysis")
    
    agent = InventoryAgent()
    products = get_all_products()
    
    # Create rows of 6 columns each to handle more items
    items_list = list(products.items())
    
    # Batch items into groups of 3 for layout
    for i in range(0, len(items_list), 3):
        cols = st.columns(3)
        batch = items_list[i:i+3]
        
        for idx, (sku, item) in enumerate(batch):
            analysis = agent.check_stock_status(sku)
            
            with cols[idx]:
                with st.container(border=True):
                    # Image
                    st.image(item["img"], width=True)
                    
                    # Title (Spacing fixed via CSS above)
                    st.markdown(f"### {item['name']}")
                    
                    # Metrics
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Online", item["online_stock"])
                    c2.metric("Store", item["store_stock"])
                    c3.metric("Carts", item["active_carts"])
                    
                    st.write("") # Spacer
                    
                    # Insight Card (Colors fixed via CSS above)
                    if analysis["status"] == "CRITICAL_DEMAND":
                        st.markdown(f"<div class='critical'><b>🔥 URGENCY ALERT</b><br>{analysis['insight']}</div>", unsafe_allow_html=True)
                    elif analysis["status"] == "OMNICHANNEL_OPP":
                        st.markdown(f"<div class='warning'><b>📍 OMNI SAVE</b><br>{analysis['insight']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='normal'><b>✅ HEALTHY</b><br>{analysis['insight']}</div>", unsafe_allow_html=True)

# --- TAB 2: CHATBOT ---
with tab2:
    st.markdown("### 🛍️ Conversational Sales Agent")
    st.markdown("Try asking for 'Manga', 'Sneakers', or the 'Red Dress'.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What are you looking for?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        sales_bot = SalesAgent()
        response = sales_bot.chat(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)