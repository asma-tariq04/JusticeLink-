import streamlit as st
import CaseHub
import Complaint_Generator
import History
import Know_Your_Rights
from responsive import apply_responsive

# Page Configuration 
st.set_page_config(
    page_title="JusticeLink",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About":"Developed by Asma Tariq"},
    
    
)

apply_responsive()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Gilda+Display&display=swap');

html body .custom-card,
html body .suggestion-box,
html body .case-card,
html body .skin-textbox {
    background-color: #EFECE7 !important;
    border: 1px solid #3A2E2B !important;
    border-left: 5px solid #3A2E2B !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.07) !important;
}

html body div[data-testid="stButton"] button {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.10) !important;
    transition: all 0.2s ease !important;
}

html body div[data-testid="stButton"] button:hover {
    background: #3A2E2B !important;
    border-color: #3A2E2B!important;
    color: #ffffff !important;
}



</style>
""", unsafe_allow_html=True)

# --- SCREEN 1: Home ---
if "current_screen" not in st.session_state:
    st.session_state["current_screen"]= "home"


# sidebar navigation
st.sidebar.markdown("""
<div class="sidebar-title">
   <span class="icon">⚖️</span> 
   <span>JusticeLink</span>
    
</div>
<div class="sidebar-subtitle">
    Legal Empowerment Platform
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.sidebar-title {
    display: flex;
    align-items: center;
    margin-top: -3.5rem;
    transform: translateY(-5px);
    margin-bottom: 0.1rem;
    font-family: "Cormorant Garamond", serif;
    font-size: 34px;
    font-weight: 500;
    color: #171717;
    gap:8px;
    line-height: 2;
    pointer-events: none;
}

.sidebar-subtitle {
    font-family: "Century Gothic", sans-serif;
    font-size: 18px;
    font-weight: 400;
    transform: translateY(-5px);
    color: #222222;
    margin-bottom: 3.2rem !important;
}
[data-testid="stSidebar"] {
   background-color:#EBEAE8;
}
.sidebar-title .icon {
    font-size: 29px;          
    filter: grayscale(100%) brightness(0.1);
    line-height: 1.5;            
}

.sidebar-title span:last-child {
    font-size: 24px;
}

</style>
""", unsafe_allow_html=True)

if st.sidebar.button(
    "CaseHub",
    icon=":material/description:",
    type="tertiary",
    width="stretch",
):
    st.session_state["current_screen"] = "CaseHub"

st.sidebar.caption("Analyze your case and organize evidence.")

if st.sidebar.button(
    "Know Your Rights",
    icon=":material/balance:",
    type="tertiary",
    width="stretch",
):
    st.session_state["current_screen"] = "Know_Your_Rights"

st.sidebar.caption("Explore legal information and guidance.")

if st.sidebar.button(
    "Complaint Generator",
    icon=":material/contract:",
    type="tertiary",
    width="stretch",
):
    st.session_state["current_screen"] = "Complaint_Generator"

st.sidebar.caption("Create formal complaints and applications.")


if st.sidebar.button(
    "History",
    icon=":material/folder_open:",
    type="tertiary",
    width="stretch",
):
    st.session_state["current_screen"] = "History"

st.sidebar.caption("Access your saved cases.")
if st.sidebar.button(
    "↩",
    key="back_to_home_btn",
    type="tertiary",
):
    st.session_state["current_screen"] = "home"
    st.rerun()

# BUTTON CSS

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0px !important;
}
    /* Button spacing */
    [data-testid="stSidebar"] .stButton {
        margin: 0 !important;
        padding: 0 !important;
        margin-top: 8px !important;
    }

    /* Button itself */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        align-items:left;
        width: 100% !important;
        min-height:38px !important;
        display:flex;
        padding: 0px 20px 0px 25px !important;

        justify-content: flex-start !important;
        text-align: left !important;
    }

    /* Button text */
    [data-testid="stSidebar"] .stButton > button p {
        font-family: "Cormorant Garamond", serif !important;
        font-size: 21px !important;
        font-weight: 500 !important;
        color: #171717 !important;
        margin: 0 !important;
        line-height: 1.1 !important;
    }

    /* Material icons */
    [data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"] {
        font-size: 25px !important;
        color: #333333 !important;
        margin-right: 9px !important;
    }

    /* Hover */
    [data-testid="stSidebar"] .stButton > button:hover {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover p {
        color: #000000 !important;
    }

    /* Captions */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        margin-left: 26px !important;
        margin-top: 1px !important;
        margin-bottom: 6px !important;
        padding: 0 !important;
        
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        font-family: "Century Gothic", sans-serif !important;
        font-size: 15px !important;
        font-weight: 400 !important;

        color: #000000 !important;

        line-height: 1.5 !important;
        margin: 0 !important;

        max-width: 250px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- SCREEN 1: Home ---

if st.session_state["current_screen"] == "home":
    st.markdown(
        """
        <style>
        .stApp {
            background: transparent !important;
        }

        /* Desktop View (Standard Landscape 16:9 Image) */
        @media (min-width: 769px) {
            [data-testid="stMain"] {
                background-image: url("https://github.com/asma-tariq04/JusticeLink-/blob/f9ed191c58e7827db6c60900ac7ba038187c9037/ChatGPT%20Image%20Aug%2030,%202026,%2008_02_21%20PM.png?raw=true") !important;
                background-size: cover !important;
                background-repeat: no-repeat !important;
                background-position: center center !important;
                min-height: 100vh;
            }
        }

        @media (max-width: 768px) {
            [data-testid="stMain"] {
                
                background-image: url("https://github.com/asma-tariq04/JusticeLink-/blob/main/Gemini_Generated_Image_8at7df8at7df8at7%20(1).jpg?raw=true") !important;
                background-size: cover !important;
                background-repeat: no-repeat !important;
                background-position: center center !important;
                min-height: 100vh;
            }
            
            [data-testid="stMainBlockContainer"] {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 2rem !important;
            }
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stSidebar"] {
            z-index: 1000;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --- SCREEN 2: CASE HUB ---
elif st.session_state["current_screen"] == "CaseHub":
    CaseHub.run()  

# --- SCREEN 3: KNOW YOUR RIGHTS ---
elif st.session_state["current_screen"] == "Know_Your_Rights":
    Know_Your_Rights.run()  

# --- SCREEN 4: COMPLAINT GENERATOR ---
elif st.session_state["current_screen"] == "Complaint_Generator":
    Complaint_Generator.run()  

# --- SCREEN 5: HISTORY ---
elif st.session_state["current_screen"] == "History":
    History.run() 


# Run Cmd 
# python -m streamlit run home.py
