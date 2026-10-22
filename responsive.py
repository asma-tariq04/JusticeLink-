import streamlit as st


def apply_responsive():
    st.markdown(
        """
<style>

@media (max-width: 768px) {
   
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
    }

  
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) > div[data-testid="stColumn"] {
        width: auto !important;
        min-width: unset !important;
        flex: unset !important;
    }

    
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) > div[data-testid="stColumn"]:last-child {
        margin-left: auto !important;
    }

    html body div[data-testid="stCheckbox"] {
        display: flex !important;
        justify-content: flex-end !important;
    }

    html body div[data-testid="stCheckbox"] label {
        white-space: nowrap !important;
    }
    [data-testid="stAppViewContainer"]::after {
        position: fixed !important;
        bottom: 12% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 280px !important;
        height: 280px !important;
        opacity: 0.06 !important;
        z-index: 0 !important;
    }
    }
    
@media (min-width: 769px) {
 
    [data-testid="stAppViewContainer"]::after {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        left: auto !important;
        transform: none !important;
        width: 380px !important;
        height: 380px !important;
        opacity: 0.07 !important;
        z-index: 0 !important;
    }
}
 
@media (max-width: 768px) {
 
    [data-testid="stAppViewContainer"]::after {
        position: fixed !important;
        bottom: 12% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 280px !important;
        height: 280px !important;
        opacity: 0.06 !important;
        z-index: 0 !important;
    }
 
    html body [data-testid="stMainBlockContainer"],
    html body .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
 
    [data-testid="stVerticalBlock"] {
        gap: 0.7rem !important;
    }
 
    [data-testid="stSidebar"] {
        width: 74vw !important;
    }
 
    html body .sidebar-subtitle {
        font-size: 16px !important;
        margin-bottom: 2rem !important;
    }
 
    html body [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        max-width: none !important;
        font-size: 14px !important;
    }
 
    html body .casehub-title,
    html body .knowrights-title,
    html body .complaint-title,
    html body .history-title {
        font-size: 28px !important;
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        padding-bottom: 8px !important;
    }
 
    html body .search-subtitle,
    html body .complaint-subtitle,
    html body .history-subtitle {
        font-size: 16px !important;
    }
 
    html body .description,
    html body .upload {
        font-size: 17px !important;
        margin-top:1rem;
    }
 
    html body [data-testid="stFileUploaderDropzoneInstructions"] small {
        font-size: 14px !important;
    }
 
    html body div[style*="height: 140px"] {
        height: 0 !important;
    }
 
    html body .section-title {
        font-size: 20px !important;
        margin-top: 0 !important;
    }
 
    html body .custom-card {
        font-size: 16px !important;
        padding: 12px 14px !important;
    }
 
    html body .suggestion-box {
        padding: 16px 18px !important;
    }
 
    html body .suggestion-box li {
        font-size: 17px !important;
    }
 
    html body .status-text {
        font-size: 18px !important;
    }
 
    html body .stTextInput input {
        height: 48px !important;
        font-size: 14px !important;
    }
 
    html body .skin-textbox {
        padding: 18px 16px !important;
        text-align: left !important;
        max-height: 60vh !important;
    }
 
    html body .skin-textbox-title {
        font-size: 18px !important;
    }
 
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) {
        flex-wrap: nowrap !important;
    }
 
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) > div[data-testid="stColumn"] {
        min-width: 0 !important;
    }
 
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) > div[data-testid="stColumn"]:first-child {
        flex: 1 1 0 !important;
        width: auto !important;
    }
 
    html body div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) > div[data-testid="stColumn"]:last-child {
        flex: 0 0 56px !important;
        width: 56px !important;
    }
 
    html body .case-card {
        padding: 14px 16px !important;
    }
 
    html body .case-title {
        font-size: 16px !important;
    }
 
    html body .case-line {
        font-size: 13px !important;
    }
    
    html body div[data-testid="stDialog"] h2 {
        font-size: 22px !important;
    }
 
    html body div[data-testid="stDialog"] p {
        font-size: 14px !important;
    }
}
 
@media (max-width: 480px) {
 
    html body .casehub-title,
    html body .knowrights-title,
    html body .complaint-title,
    html body .history-title {
        font-size: 24px !important;
    }
 
    html body .custom-card {
        font-size: 15px !important;
    }
 
    html body .suggestion-box li {
        font-size: 16px !important;
    }
    
}

 
</style>
""",
        unsafe_allow_html=True,
    )
 