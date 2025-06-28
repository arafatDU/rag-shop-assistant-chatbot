import streamlit as st
import requests
import json
import time

# Page configuration
st.set_page_config(
    page_title="🛒 Shop Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern dark theme CSS
st.markdown("""
<style>
    /* Global theme */
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Sidebar messenger style */
    .stSidebar {
        background: #1a1a1a !important;
        border-right: 1px solid #333 !important;
        width: 350px !important;
        min-width: 350px !important;
    }
    
    .stSidebar > div {
        background: #1a1a1a !important;
        padding: 0.5rem 1rem !important;
        width: 350px !important;
        min-width: 350px !important;
    }
    
    /* Sidebar header */
    .stSidebar .element-container:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove spacing after headers in sidebar */
    .stSidebar h3 {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Remove default element spacing in sidebar */
    .stSidebar .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Chat container specific positioning */
    .stSidebar .chat-container {
        margin-top: 0 !important;
    }
    
    /* Chat container */
    .chat-container {
        height: 500px;
        overflow: hidden;
        padding: 15px;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        margin: 0 !important;
        border: 1px solid #333;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    
    /* Chat messages area */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding-bottom: 15px;
        margin-bottom: 15px;
        min-height: 300px;
    }
    
    /* Chat input area */
    .chat-input-area {
        border-top: 1px solid #444;
        padding-top: 15px;
        margin-top: auto;
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Override Streamlit form styling inside chat */
    .chat-container .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Input styling inside chat container */
    .chat-container .stTextInput > div > div > input {
        background: #2a2a2a !important;
        border: 1px solid #555 !important;
        border-radius: 20px !important;
        color: #fff !important;
        padding: 10px 15px !important;
        font-size: 14px !important;
        width: 100% !important;
    }
    
    /* Send button inside chat container */
    .chat-container .stButton > button {
        background: #007bff !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 15px !important;
        font-size: 14px !important;
        min-width: 45px !important;
        height: 40px !important;
    }
    
    /* Clear chat button */
    .stButton[data-testid="baseButton-secondary"] > button {
        background: #dc3545 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 0.85rem !important;
        margin-top: 10px !important;
    }
    
    .stButton[data-testid="baseButton-secondary"] > button:hover {
        background: #c82333 !important;
    }
    
    /* Chat messages */
    .message {
        margin: 8px 0;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 85%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
        display: block;
        clear: both;
    }
    
    .user-message {
        background: #007bff;
        color: white;
        margin-left: auto;
        margin-right: 0;
        text-align: right;
        border-bottom-right-radius: 4px;
        float: right;
        clear: both;
    }
    
    .bot-message {
        background: #333;
        color: #fff;
        margin-left: 0;
        margin-right: auto;
        text-align: left;
        border-bottom-left-radius: 4px;
        float: left;
        clear: both;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: #2a2a2a !important;
        border: 1px solid #444 !important;
        border-radius: 20px !important;
        color: #fff !important;
        padding: 12px 16px !important;
        width: 100% !important;
        min-width: 250px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 0 1px #007bff !important;
    }
    
    /* Form container */
    .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Send button */
    .stButton > button {
        background: #007bff !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 12px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        min-width: 50px !important;
        width: 100% !important;
        white-space: nowrap !important;
        font-size: 16px !important;
    }
    
    .stButton > button:hover {
        background: #0056b3 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Form layout improvements */
    .stForm > div {
        gap: 8px !important;
    }
    
    .stForm .row-widget {
        gap: 8px !important;
    }
    
    /* Main content area adjustment for wider sidebar */
    .main .block-container {
        padding: 2rem !important;
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a) !important;
        border-radius: 15px !important;
        margin: 1rem !important;
        margin-left: 370px !important;
        border: 1px solid #333 !important;
    }
    
    /* When sidebar is collapsed */
    .stApp[data-sidebar-state="collapsed"] .main .block-container {
        margin-left: 1rem !important;
    }
    
    /* Product cards */
    .product-card {
        background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #007bff;
        box-shadow: 0 10px 30px rgba(0,123,255,0.2);
    }
    
    .product-title {
        color: #007bff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .product-brand {
        color: #ccc;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    
    .product-tags {
        display: flex;
        gap: 6px;
        margin: 10px 0;
    }
    
    .tag {
        background: rgba(0,123,255,0.2);
        color: #007bff;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .product-price {
        color: #28a745;
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: auto;
    }
    
    /* Filter controls */
    .stSelectbox > div > div {
        background: #2a2a2a !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        color: #fff !important;
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #fff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #007bff;
        border-radius: 3px;
    }
    
    /* Sidebar toggle button */
    .sidebar-toggle {
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1000;
        background: #007bff !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
        cursor: pointer !important;
    }
    
    .sidebar-toggle:hover {
        background: #0056b3 !important;
    }
    
    /* Hide toggle when sidebar is expanded */
    .stApp:not([data-sidebar-state="collapsed"]) .sidebar-toggle {
        display: none !important;
    }
    
    /* Show toggle when sidebar is collapsed */
    .stApp[data-sidebar-state="collapsed"] .sidebar-toggle {
        display: block !important;
    }
    .status-message {
        text-align: center;
        padding: 40px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .error-message {
        background: rgba(220,53,69,0.1);
        border: 1px solid rgba(220,53,69,0.3);
        color: #dc3545;
    }
    
    .loading-message {
        background: rgba(255,193,7,0.1);
        border: 1px solid rgba(255,193,7,0.3);
        color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "products" not in st.session_state:
    st.session_state.products = []
if "is_sending" not in st.session_state:
    st.session_state.is_sending = False

# API configuration
API_BASE_URL = "http://localhost:8000"

# Sidebar - Messenger Style Chat
with st.sidebar:
    # Chat input at the very top
    st.markdown('<div style="margin-top: -1rem;"></div>', unsafe_allow_html=True)
    
    # Open chat messages container
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for i in range(0, len(st.session_state.chat_history), 2):
            # User message
            if i < len(st.session_state.chat_history):
                user_msg = st.session_state.chat_history[i].replace("User: ", "")
                st.markdown(f'''
                <div class="message user-message">
                    {user_msg}
                </div>
                ''', unsafe_allow_html=True)
            
            # Bot message
            if i + 1 < len(st.session_state.chat_history):
                bot_msg = st.session_state.chat_history[i + 1].replace("Assistant: ", "")
                st.markdown(f'''
                <div class="message bot-message">
                    {bot_msg}
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="text-align: center; color: #666; padding: 20px; margin: 0;">
            👋 Hi! Ask me about products
        </div>
        ''', unsafe_allow_html=True)
    
    # Close chat messages and start input area
    st.markdown('''
        </div>
        <div class="chat-input-area">
    ''', unsafe_allow_html=True)
    
    # Chat input form at the bottom of container
    with st.form(key="chat_form", clear_on_submit=True):
        # Input row
        input_col, button_col = st.columns([5, 1])
        
        with input_col:
            user_input = st.text_input(
                "Message", 
                placeholder="Type your message...",
                key="message_input",
                label_visibility="collapsed"
            )
        
        with button_col:
            send_btn = st.form_submit_button(
                "▶",
                disabled=st.session_state.is_sending,
                use_container_width=True,
                help="Send message"
            )
    
    # Close input area and chat container
    st.markdown('''
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Handle message sending
    if send_btn and user_input.strip():
        st.session_state.is_sending = True
        
        try:
            response = requests.post(f"{API_BASE_URL}/chat", json={
                "query": user_input.strip(),
                "history": st.session_state.chat_history
            })
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.chat_history = data.get("history", [])
            else:
                st.error("Connection error")
                
        except Exception as e:
            st.error("Network error")
        
        st.session_state.is_sending = False
        st.rerun()
    
    # Auto-scroll to bottom of chat messages
    if st.session_state.chat_history:
        st.markdown('''
        <script>
        setTimeout(() => {
            const chatMessages = document.querySelector('.chat-messages');
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }, 100);
        </script>
        ''', unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Main content area
# Add sidebar toggle button
st.markdown('''
<button class="sidebar-toggle" onclick="
    const sidebar = window.parent.document.querySelector('[data-testid=stSidebar]');
    if(sidebar) {
        const event = new KeyboardEvent('keydown', {
            key: '[',
            ctrlKey: true,
            bubbles: true
        });
        window.parent.document.dispatchEvent(event);
    }
">☰ Chat</button>
''', unsafe_allow_html=True)

st.title("🛒 Shop Assistant")
st.markdown("---")

# Check API connection
connection_status = False
try:
    health_response = requests.get(f"{API_BASE_URL}/health", timeout=2)
    connection_status = health_response.status_code == 200
except:
    st.markdown('''
    <div class="status-message error-message">
        <h3>⚠️ Connection Error</h3>
        <p>Cannot connect to backend API</p>
    </div>
    ''', unsafe_allow_html=True)

if connection_status:
    # Load products
    if not st.session_state.products:
        try:
            response = requests.get(f"{API_BASE_URL}/products?page=1&page_size=100")
            if response.status_code == 200:
                st.session_state.products = response.json()
        except:
            pass
    
    if st.session_state.products:
        # Filters
        st.subheader("🔍 Filter Products")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            brands = ["All"] + sorted(set(p["ProductBrand"] for p in st.session_state.products if p["ProductBrand"]))
            selected_brand = st.selectbox("Brand", brands)
        
        with col2:
            genders = ["All"] + sorted(set(p["Gender"] for p in st.session_state.products if p["Gender"]))
            selected_gender = st.selectbox("Gender", genders)
        
        with col3:
            colors = ["All"] + sorted(set(p["PrimaryColor"] for p in st.session_state.products if p["PrimaryColor"]))
            selected_color = st.selectbox("Color", colors)
        
        # Apply filters
        filtered_products = st.session_state.products
        
        if selected_brand != "All":
            filtered_products = [p for p in filtered_products if p["ProductBrand"] == selected_brand]
        if selected_gender != "All":
            filtered_products = [p for p in filtered_products if p["Gender"] == selected_gender]
        if selected_color != "All":
            filtered_products = [p for p in filtered_products if p["PrimaryColor"] == selected_color]
        
        st.markdown("---")
        st.subheader(f"📦 Products ({len(filtered_products)} found)")
        
        # Display products
        if filtered_products:
            # Create rows of 3 products each
            for i in range(0, len(filtered_products), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(filtered_products):
                        product = filtered_products[i + j]
                        with col:
                            st.markdown(f'''
                            <div class="product-card">
                                <div>
                                    <div class="product-title">{product["ProductName"]}</div>
                                    <div class="product-brand">Brand: {product["ProductBrand"]}</div>
                                    <div class="product-tags">
                                        <span class="tag">{product["Gender"]}</span>
                                        <span class="tag">{product["PrimaryColor"]}</span>
                                    </div>
                                </div>
                                <div class="product-price">${product["Price"]:,.0f}</div>
                            </div>
                            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="status-message">
                <h3>🔍 No products found</h3>
                <p>Try adjusting your filters</p>
            </div>
            ''', unsafe_allow_html=True)
    
    else:
        st.markdown('''
        <div class="status-message loading-message">
            <h3>📦 Loading products...</h3>
        </div>
        ''', unsafe_allow_html=True)


