import streamlit as st
import json
import io
import zipfile
from pathlib import Path
from datetime import datetime

MAX_CASES_SHOWN = 2


def get_timestamp(case):
    return case["timestamp"]


def load_cases():
    cases = []
    history_folder = Path("History")

    if not history_folder.exists():
        return cases

    for folder in history_folder.iterdir():
        if not folder.is_dir():
            continue

        analysis_file = folder / "analysis" / "analysis.json"
        if not analysis_file.exists():
            continue

        try:
            with open(analysis_file, "r") as f:
                record = json.load(f)
        except Exception:
            continue

        analysis = record.get("analysis", {})
        if analysis.get("category") == "Unable to analyze":
            continue

        try:
            timestamp = int(folder.name.split("_")[-1])
            date_text = datetime.fromtimestamp(timestamp).strftime("%d %B %Y")
        except ValueError:
            timestamp = 0
            date_text = "Unknown date"

        authorities = analysis.get("authorities", [])

        cases.append({
            "folder": folder,
            "title": analysis.get("category", "Case"),
            "date": date_text,
            "timestamp": timestamp,
            "authority": authorities[0] if authorities else "Not specified",
            "score": analysis.get("score", 0),
            "status": analysis.get("score_status", ""),
            "problem": record.get("problem", "")
        })

    cases.sort(key=get_timestamp, reverse=True)
    return cases


def make_zip_bytes(folder):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in folder.rglob("*"):
            if file_path.is_file() and file_path.suffix != ".json":
                zf.write(file_path, file_path.relative_to(folder))
    return buffer.getvalue()


def case_matches(case, query):
    text = (case["title"] + " " + case["problem"] + " " + case["authority"]).lower()

    for word in query.lower().split():
        if word not in text:
            return False

    return True


@st.dialog(" ")
def show_download_confirm(case):
    st.markdown(
        "<h2 style='font-family:\"Gilda Display\", serif; font-weight:700; margin-bottom:10px;'>"
        "Do you want to download the report?</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-family:\"Gilda Display\", serif; font-size:16px; color:#555555;'>"
        "Note: click download button to download your full case report and documents</p>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <style>
    div[data-testid="stDownloadButton"] button {
        background-color: #E7E6E5 !important;
        border: none !important;
        border-radius: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 100px !important;
        width: 130px !important;
        padding: 0 !important;
        font-family: "Gilda Display", serif !important;
        color: #171717 !important;
    }
    div[data-testid="stDownloadButton"] button [data-testid="stIconMaterial"] {
        font-size: 36px !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    zip_bytes = make_zip_bytes(case["folder"])

    left, center, right = st.columns([1, 1, 1])
    with center:
        st.download_button(
            label="Download",
            data=zip_bytes,
            file_name=f"{case['folder'].name}.zip",
            mime="application/zip",
            icon=":material/folder_open:",
            key=f"download_{case['folder'].name}"
        )


def run():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

    div[data-testid="stButton"] button {
        background-color: #E7E6E5 !important;
        border: none !important;
        border-radius: 15px !important;
        height: 40px !important;
        width: 100% !important;
    }

    div[data-testid="stButton"] button [data-testid="stIconMaterial"] {
        font-size: 24px !important;
        color: #000000 !important;
    }

    div[data-testid="stDialog"] div[data-testid="stButton"] button {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        height: 100px !important;
        width: 130px !important;
        margin: 10px auto 0 auto !important;
        padding: 0 !important;
    }

    div[data-testid="stDialog"] div[data-testid="stButton"] button [data-testid="stIconMaterial"] {
        font-size: 36px !important;
    }

    .history-title {
        font-family: "Nueue Machina", sans-serif;
        font-size: 39px;
        font-weight: 850;
        color: #000000;
        margin-top: -6.2rem;
        text-align: left;
        padding-bottom: 12px;
        border-bottom: 1.5px solid #9a9a9a;
        margin-bottom: 15px;
    }

    .history-subtitle {
        font-family: "Gilda Display", serif;
        font-size: 18px;
        color: #171717;
        margin-bottom: 18px;
    }

    .stTextInput input {
        background-color: #E7E6E5 !important;
        border: none !important;
        border-radius: 15px !important;
        font-family: "Gilda Display", serif;
        font-size: 15px;
        min-height: 45px;
    }

    .section-label {
        font-family: "Gilda Display", serif;
        font-size: 17px;
        color: #171717;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .case-card {
        background-color: #E7E6E5;
        border-radius: 15px;
        padding: 18px 20px;
        font-family: "Gilda Display", serif;
        color: #171717;
        margin-bottom: 15px;
    }

    .case-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .case-line {
        font-size: 14px;
        margin-bottom: 4px;
        color: #333333;
    }
    </style>

    <div class="history-title">History</div>
    <div class="history-subtitle">Review your previously analyzed cases.</div>
    """, unsafe_allow_html=True)

    
    st.markdown("""
<style>
[data-testid="stMain"]::after {
    content: "";
    position: fixed;
    bottom: 25px;
    right: 30px;
    width: 250px;
    height: 250px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120' fill='none' stroke='%233A2E2B' stroke-width='0.8' stroke-linecap='round' stroke-linejoin='round'%3E%3C!-- Timeline Dots Accent --%3E%3Cline x1='25' y1='25' x2='25' y2='100' stroke-dasharray='2 3' stroke-width='0.6'/%3E%3Ccircle cx='25' cy='35' r='2' fill='%233A2E2B'/%3E%3Ccircle cx='25' cy='65' r='2' fill='%233A2E2B'/%3E%3Ccircle cx='25' cy='95' r='2' fill='%233A2E2B'/%3E%3C!-- Back Folder --%3E%3Cpath d='M45 40 H80 A2 2 0 0 1 82 42 V85 A2 2 0 0 1 80 87 H45 A2 2 0 0 1 43 85 V42 A2 2 0 0 1 45 40 Z' fill='%233A2E2B' fill-opacity='0.04' stroke-width='1'/%3E%3C!-- Main Front Folder --%3E%3Cpath d='M35 50 H55 L62 57 H95 A2 2 0 0 1 97 59 V98 A2 2 0 0 1 95 100 H35 A2 2 0 0 1 33 98 V52 A2 2 0 0 1 35 50 Z' fill='%233A2E2B' fill-opacity='0.08' stroke-width='1.2'/%3E%3C!-- Document Lines inside Folder --%3E%3Cline x1='42' y1='68' x2='75' y2='68' stroke-width='1'/%3E%3Cline x1='42' y1='76' x2='85' y2='76' stroke-width='1'/%3E%3Cline x1='42' y1='84' x2='68' y2='84' stroke-width='1'/%3E%3C!-- History Clock Emblem --%3E%3Ccircle cx='85' cy='45' r='12' fill='%23FBF9F6' stroke-width='1.2'/%3E%3Cpolyline points='85 38 85 45 90 48' stroke-width='1.2'/%3E%3Cpath d='M75 42 A12 12 0 1 1 80 55' stroke-dasharray='2 2' stroke-width='0.8'/%3E%3C/svg%3E");
    
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.05;
    pointer-events: none;
    z-index: 0;}



div[data-testid="stCheckbox"] label p {
    font-family: "Gilda Display", serif !important;
    font-size: 13px !important;
    color: #171717 !important;
}

div[data-testid="stColumn"]:has(div[data-testid="stCheckbox"]) {
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
}

div[data-testid="stCheckbox"] {
    display: flex !important;
    justify-content: flex-end !important;
    width: 100% !important;
}

div[data-testid="stCheckbox"] label {
    display: flex !important;
    flex-direction: row-reverse !important; 
    gap: 8px !important;
    white-space: nowrap !important;
}
div[data-testid="stCheckbox"] label > div:first-child {
    transform: scale(0.65) !important; 
    transform-origin: right center !important;
}

</style>
""", unsafe_allow_html=True)

    search_col, icon_col = st.columns([9.2, 0.8], gap="small")
    with search_col:
        search_query = st.text_input(
            "Search",
            placeholder="Search Previous Cases",
            label_visibility="collapsed",
            key="history_search"
        )
    with icon_col:
        st.button(
            "",
            icon=":material/search:",
            key="history_search_btn",
            type="tertiary",
            use_container_width=True
        )


    all_cases = load_cases()

    
    show_all = st.session_state.get("toggle_all_cases", False)

    if search_query:
        filtered_cases = [c for c in all_cases if case_matches(c, search_query)]
    elif show_all:
        filtered_cases = all_cases
    else:
        filtered_cases = all_cases[:MAX_CASES_SHOWN]

    st.write("")

    if len(filtered_cases) == 0:
        st.markdown("""
            <div style="text-align:center; margin-top:40px; font-family:'Gilda Display', serif; color:#555555;">
                📁 No Previous Cases<br>
                <span style="font-size:14px;">Your analyzed cases will appear here.</span>
            </div>
        """, unsafe_allow_html=True)
        return

    label = "Your Case" if search_query else "Previous Cases"
    
   
    header_col1, header_col2 = st.columns([8.5, 1.5])
    with header_col1:
        st.markdown(f'<div class="section-label">📁 {label}</div>', unsafe_allow_html=True)
    with header_col2:
        if not search_query and len(all_cases) > MAX_CASES_SHOWN:
            st.toggle("Show All", key="toggle_all_cases")

    cols = st.columns(2)

    for index, case in enumerate(filtered_cases):
        with cols[index % 2]:
            st.markdown(f"""
                <div class="case-card">
                    <div class="case-title">📌 {case['title']}</div>
                    <div class="case-line">Date: {case['date']}</div>
                    <div class="case-line">Legal Readiness: {case['score']}%</div>
                    <div class="case-line">Authority: {case['authority']}</div>
                    <div class="case-line">Status: {case['status']}</div>
                </div>
            """, unsafe_allow_html=True)

            view_clicked = st.button("View Report", key=f"view_{index}", use_container_width=True)
            if view_clicked:
                show_download_confirm(case)