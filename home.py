import CaseHub
import Complaint_Generator
import History
import Know_Your_Rights
import signup
import streamlit as st
from my_auth import is_logged_in, sidebar_profile
from responsive import apply_responsive

st.set_page_config(
    page_title="JusticeLink",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Developed by Asma Tariq"},
)

if not is_logged_in():
  st.markdown(
      """
        <style>
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        [data-testid="stToolbarActions"] { display: none !important; }
[data-testid="stMainMenu"] { display: none !important; }
[data-testid="stAppDeployButton"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
footer { visibility: hidden !important; }
        </style>
        """,
      unsafe_allow_html=True,
  )

if "current_screen" not in st.session_state:
  st.session_state["current_screen"] = "home"

apply_responsive()

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

if is_logged_in():
  st.sidebar.markdown(
      """
    <div class="sidebar-title">
       <span class="icon">⚖️</span> 
       <span>JusticeLink</span>
    </div>
    <div class="sidebar-subtitle">
        Legal Empowerment Platform
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.sidebar.markdown(
      """
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
    """,
      unsafe_allow_html=True,
  )

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

  sidebar_profile()

  st.markdown(
      """
    <style>
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0px !important;
    }
    [data-testid="stSidebar"] .stButton {
        margin: 0 !important;
        padding: 0 !important;
        margin-top: 8px !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        align-items:left;
        width: 100% !important;
        min-height:39px !important;
        display:flex;
        padding: 0px 20px 0px 25px !important;
        justify-content: flex-start !important;
        text-align: left !important;
    }
    [data-testid="stSidebar"] .stButton > button p {
        font-family: "Cormorant Garamond", serif !important;
        font-size: 22px !important;
        font-weight: 500 !important;
        color: #171717 !important;
        margin: 0 !important;
        line-height: 1.1 !important;
    }
    [data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"] {
        font-size: 25px !important;
        color: #333333 !important;
        margin-right: 9px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover p {
        color: #000000 !important;
    }
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
      unsafe_allow_html=True,
  )

if st.session_state["current_screen"] not in ("home", "auth") and not is_logged_in():
  st.session_state["current_screen"] = "auth"

if st.session_state["current_screen"] == "home":
  if not is_logged_in():
    _, col_btn = st.columns([8.5, 1.5])
    with col_btn:
      if st.button("Log In", key="top_login_btn"):
        st.session_state["current_screen"] = "auth"
        st.rerun()

    st.markdown(
        """
        <style>
        html body .st-key-top_login_btn {
            position: fixed;
            top: 0.7rem;
            right: 8rem;
            width: auto !important;
            z-index: 1000000;
        }
        html body .st-key-top_login_btn button {
            background: #EDEBE8 !important;
            border: 1px solid #a8a29b !important;
            border-radius: 20px !important;
            height: 38px !important;
            min-height: 38px !important;
            width: auto !important;
            padding: 0 24px !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.10) !important;
        }
        html body .st-key-top_login_btn button p {
            color: #000000 !important;
            font-family: "Syne", sans-serif !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            margin: 0 !important;
        }
        html body .st-key-top_login_btn button:hover {
            background: #3A2E2B !important;
            border-color: #3A2E2B !important;
        }
        html body .st-key-top_login_btn button:hover p {
            color: #ffffff !important;
        }
        @media (max-width: 768px) {
            html body .st-key-top_login_btn {
                top: 0.5rem;
                right: 4.5rem;
            }
            html body .st-key-top_login_btn button {
                height: 34px !important;
                min-height: 34px !important;
                padding: 0 16px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

  st.markdown(
      """
        <style>
        .stApp {
            background: transparent !important;
        }
        @media (min-width: 769px) {
            [data-testid="stMain"] {
                background-image: url("https://github.com/asma-tariq04/JusticeLink-/blob/main/home.png?raw=true") !important;
                background-size: cover !important;
                background-repeat: no-repeat !important;
                background-position: center center !important;
                min-height: 100vh;
            }
        }
        @media (max-width: 768px) {
            [data-testid="stMain"] {
                background-image: url("https://github.com/asma-tariq04/JusticeLink-/blob/main/mobile_app.jpg?raw=true") !important;
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

elif st.session_state["current_screen"] == "CaseHub":
  CaseHub.run()

elif st.session_state["current_screen"] == "Know_Your_Rights":
  Know_Your_Rights.run()

elif st.session_state["current_screen"] == "Complaint_Generator":
  Complaint_Generator.run()

elif st.session_state["current_screen"] == "History":
  History.run()

elif st.session_state["current_screen"] == "auth":
  signup.run()
