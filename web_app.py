import streamlit as st
from PIL import Image
import time
from morse import text_to_morse, morse_to_text
from steg import encode_image, decode_image
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Secret Messenger",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63);
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 8px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(106,17,203,0.4);
    }
    .stTabs [aria-selected="true"] {
        color: #6a11cb !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# App Header
st.title("🔐 Secret Messenger")
st.markdown("""
    <div style='background:rgba(255,255,255,0.1);padding:20px;border-radius:12px;margin-bottom:20px'>
    <h3 style='color:white;text-align:center'>Military-Grade Message Encryption</h3>
    </div>
""", unsafe_allow_html=True)

# Main Tabs
tab1, tab2 = st.tabs(["🔠 Morse Tools", "🖼️ Steganography"])

with tab1:
    # Morse Translator
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Morse Translator")
        direction = st.radio("Translation:", ["Text → Morse", "Morse → Text"], horizontal=True)
        text = st.text_area("Input:", height=150)
        
        if st.button("Translate", key="morse_translate"):
            with st.spinner("Processing..."):
                progress_bar = st.progress(0)
                for percent in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent + 1)
                
                try:
                    if direction == "Text → Morse":
                        result = text_to_morse(text)
                    else:
                        result = morse_to_text(text)
                    
                    with col2:
                        st.subheader("Result")
                        st.code(result, language="text")
                        
                        # Download button
                        st.download_button(
                            "Download Result",
                            data=result,
                            file_name="morse.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    # Steganography
    steg_tab1, steg_tab2 = st.tabs(["🔒 Encode", "🔓 Decode"])
    
    with steg_tab1:
        st.subheader("Encode Message")
        img = st.file_uploader("Upload image:", type=["png", "jpg", "jpeg"], key="encode_img")
        
        if img:
            st.image(img, caption="Uploaded Image", use_column_width=True)
            message = st.text_area("Secret message:", key="secret_msg")
            password = st.text_input("Password:", type="password", key="encode_pass")
            
            if st.button("Encode", key="encode_btn"):
                with st.spinner("Encoding..."):
                    progress_bar = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(percent + 1)
                    
                    try:
                        image = Image.open(img)
                        encoded = encode_image(image, message, password)
                        
                        # Display and download
                        st.success("Successfully encoded!")
                        st.image(encoded, caption="Encoded Image", use_column_width=True)
                        
                        buf = BytesIO()
                        encoded.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            "Download Encoded Image",
                            data=byte_im,
                            file_name="secret.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"Encoding failed: {str(e)}")
    
    with steg_tab2:
        st.subheader("Decode Message")
        secret_img = st.file_uploader("Upload image:", type=["png", "jpg", "jpeg"], key="decode_img")
        
        if secret_img:
            st.image(secret_img, caption="Encoded Image", use_column_width=True)
            password = st.text_input("Password:", type="password", key="decode_pass")
            
            if st.button("Decode", key="decode_btn"):
                with st.spinner("Decoding..."):
                    progress_bar = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(percent + 1)
                    
                    try:
                        image = Image.open(secret_img)
                        message = decode_image(image, password)
                        
                        st.success("Decoded message:")
                        st.text_area("Message:", value=message, height=100, key="decoded_msg")
                    except Exception as e:
                        st.error(f"Decoding failed: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("## 📊 App Info")
    st.markdown("""
    - **Morse Code Translator**
    - **Image Steganography**
    - Password Protected
    - Secure Encoding
    """)
    
    st.markdown("## 🛠️ Settings")
    if st.button("Clear Cache"):
        st.rerun()
        st.success("UI refreshed!")