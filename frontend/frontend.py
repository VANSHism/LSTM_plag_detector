import os
import streamlit as st
import requests

# API endpoint
def get_api_base_url():
    # Prefer Streamlit secrets, fallback to environment variable, then None
    try:
        secret_url = st.secrets.get("API_URL")
    except Exception:
        secret_url = None
    env_url = os.environ.get("API_URL")
    return secret_url or env_url

# Page config
st.set_page_config(
    page_title="LSTM Plagiarism Detection",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for styling
st.markdown(
    """
    <style>
        /* Main container styling */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 0;
        }
        
        /* Ensure main content area has proper background */
        .main .block-container {
            background: transparent;
        }
        
        /* Header styling */
        .main-header {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .main-header h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        /* Content container */
        .content-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin: 1rem 0;
        }
        
        /* Text area styling */
        .stTextArea textarea {
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            padding: 15px;
            font-size: 16px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s ease;
            background-color: #ffffff !important;
            color: #333333 !important;
        }
        
        .stTextArea textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background-color: #ffffff !important;
            color: #333333 !important;
        }
        
        .stTextArea textarea::placeholder {
            color: #999999 !important;
        }
        
        /* Label styling */
        .stTextArea label {
            font-weight: 600;
            font-size: 1.1rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 12px;
            padding: 12px 30px;
            border: none;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Clear button styling */
        button[kind="secondary"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
        }
        
        button[kind="secondary"]:hover {
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6) !important;
        }
        
        /* Result card styling */
        .result-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            color: #333333 !important;
        }
        
        .result-card * {
            color: #333333 !important;
        }
        
        /* Success message styling */
        .stSuccess {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.2rem;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        }
        
        /* Info message styling */
        .stInfo {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.2rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        /* Warning message styling */
        .stWarning {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        }
        
        /* Error message styling */
        .stError {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(235, 51, 73, 0.3);
        }
        
        /* Confidence score display */
        .confidence-display {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin-top: 1rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            color: #333333 !important;
        }
        
        .confidence-display p {
            color: #666666 !important;
        }
        
        .confidence-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: #667eea; /* Fallback for browsers that don't support background-clip */
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom spacing */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
        }
        
        /* Ensure all text is visible */
        .stTextInput input,
        .stTextInput input:focus {
            color: #333333 !important;
            background-color: #ffffff !important;
        }
        
        /* General text color fixes */
        .stMarkdown,
        .stMarkdown p 
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3 {
            color: #white !important;
        }
        
        /* Ensure content container text is visible */
        .content-container {
            color: #333333 !important;
        }
        
        .content-container * {
            color: inherit;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown(
    """
    <div class="main-header">
        <h1>🔍 LSTM Plagiarism Detection</h1>
        <p style="font-size: 1.2rem; color: #000000; margin-top: 0.5rem;">
            Advanced AI-powered tool to detect plagiarism using Deep Learning
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Ensure session state key exists
if "source_text" not in st.session_state:
    st.session_state["source_text"] = ""

if "plag_text" not in st.session_state:
    st.session_state["plag_text"] = ""

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

# Function to clear input
def clear_text():
    st.session_state["source_text"] = ""
    st.session_state["plag_text"] = ""
    st.session_state["last_result"] = None


def clear_all_and_rerun():
    clear_text()
    # Streamlit renamed experimental_rerun -> rerun; keep both for compatibility.
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()



# Input section with better layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📄 Source Text")
    st.markdown("*Enter the original reference text here*")
    source_text = st.text_area(
        "Source Text",
        height=150,
        key="source_text",
        placeholder="Paste the original text here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 🔎 Text to Check")
    st.markdown("*Enter the text you want to check for plagiarism*")
    plag_text = st.text_area(
        "Text to Check",
        height=150,
        key="plag_text",
        placeholder="Paste the text to check here...",
        label_visibility="collapsed"
    )

st.markdown("</div>", unsafe_allow_html=True)

# Button section
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

with col2:
    predict_button = st.button("🔍 Analyze & Predict", use_container_width=True)

with col3:
    st.button(
        "🔄 Clear All",
        use_container_width=True,
        type="secondary",
        on_click=clear_all_and_rerun,
    )

# Handle prediction
if predict_button:
    if not source_text.strip():
        st.warning("⚠️ **Please enter a source text before predicting.**")
    elif not plag_text.strip():
        st.warning("⚠️ **Please enter a text to be checked for plagiarism before predicting.**")
    else:
        input_data = {"source_text": source_text, "plag_text": plag_text}
        api_base = get_api_base_url()

        if not api_base:
            st.error("❌ **API_URL is not configured.** Set it in Streamlit secrets or environment.")
        else:
            with st.spinner("🔄 Analyzing texts with AI model..."):
                try:
                    response = requests.post(
                        f"{api_base.rstrip('/')}/predict",
                        json=input_data,
                        timeout=15
                    )
                    result = response.json()

                    if response.status_code == 200 and "predicted_category" in result:
                        prediction = result["predicted_category"]
                        confidence = result["confidence_score"]
                        st.session_state["last_result"] = {
                            "prediction": prediction,
                            "confidence": confidence
                        }
                    else:
                        st.error(f"❌ **API Error:** {response.status_code}")
                        st.json(result)

                except requests.exceptions.RequestException as e:
                    st.error("❌ **Could not connect to the FastAPI server.** Check API_URL and server status.")
                    st.exception(e)

# Display results
if st.session_state["last_result"]:
    result = st.session_state["last_result"]
    prediction = result["prediction"]
    confidence = result["confidence"]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Prediction result
    if prediction == 1:
        st.markdown("### 🚨 Result: **PLAGIARIZED**")
        st.success("⚠️ **Warning:** The text shows signs of plagiarism!")
    else:
        st.markdown("### ✅ Result: **NOT PLAGIARIZED**")
        st.info("✨ **Good news:** The text appears to be original!")
    
    # Confidence score with progress bar
    st.markdown("<br>", unsafe_allow_html=True)
    confidence_percent = round(confidence * 100, 2)
    
    st.markdown(f"### 📊 Similarity Score")
    st.markdown(
        f"""
        <div class="confidence-display">
            <div class="confidence-value">{confidence_percent}%</div>
            <p style="color: #666; margin-top: 0.5rem;">
                The content matches <strong>{confidence_percent}%</strong> with the source text
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Progress bar
    st.progress(confidence)
    
# NOTE: Don't emit a closing </div> unless you also emit the corresponding opening <div>.