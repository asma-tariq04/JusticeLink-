import streamlit as st
import json
import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def to_list(value):
    if isinstance(value, list):
        return value
    return [str(value)]


def generate_response(topic):

    prompt = f"""
    You are a legal rights educator for Pakistan. Write clear, polished, professional English
    that an ordinary student can understand. Avoid slang. If you must use a legal term,
    explain it in brackets. The topic may be written in English, Urdu or Roman Urdu.
    Understand the meaning.

    Topic: {topic}

    Respond in ONLY valid JSON, matching this exact shape with no extra text before or after:
    {{
        "overview": ["Paragraph 1", "Paragraph 2"],
        "your_rights_explained": ["Paragraph 1", "Paragraph 2", "Paragraph 3"],
        "more_information": ["Name 1 - what it covers", "Name 2 - what it covers"]
    }}

    What each part must contain:
    - overview: exactly 2 paragraphs. Paragraph 1 explains what the topic means, with a clear
      definition in simple words. Paragraph 2 explains how this topic is understood and handled
      in Pakistan: the main constitutional protections and laws in general terms, and the kind
      of real-life situations people face. Each paragraph 4 to 5 sentences.
    - your_rights_explained: 3 or 4 paragraphs written as flowing text, not bullet points.
      Together they must cover all the main rights a person has under this topic in Pakistan,
      and what the person can do if these rights are violated. Each paragraph 3 to 4 sentences.
    - more_information: 3 to 5 items. Each item is only the NAME of a reliable source the user
      can search for to learn more: an official body, a well-known law, or a published report
      or organization, followed by " - " and a few words on what it covers.

    Rules:
    - Do NOT write any links, URLs or website addresses.
    - Do NOT write section numbers or article numbers.
    - Mention a law by its full official name only if you are completely sure it exists.
      Never invent a law, report or organization. If you are not sure, speak generally
      or leave it out.
    - If laws differ by province, say so in general terms.
    - If the topic is unclear or not about legal rights, still return valid JSON, and say in
      the overview that the topic is unclear and a more specific legal topic is needed.
    - No markdown (no *, no #, no [ ]). Plain ASCII characters only: normal hyphen (-) and straight quotes.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            timeout=30.0
        )

        raw_content = response.choices[0].message.content
        clean_json_str = re.sub(r"```json|```", "", raw_content).strip()
        data = json.loads(clean_json_str)

    except Exception as e:
        data = {
            "overview": "Could not generate information right now.",
            "your_rights_explained": [f"Something went wrong: {e}. Please try again."],
            "more_information": []
        }

    return data

def run():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;700&display=swap');

    .knowrights-title {
        font-family: "sans-serif", sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: #000000;
        margin-top: -5.9rem;
        text-align: left;
        padding-bottom: 12px;
        border-bottom: 1.5px solid #9a9a9a;
        margin-bottom: 30px;
    }

    .search-subtitle {
        font-family: "Gilda Display", serif;
        font-size: 19px;
        font-weight: 400;
        color: #171717;
        margin-top: -5px;
        margin-bottom: 15px;
    }

    .stTextInput input {
        font-family: "Gilda Display", serif;
        font-size: 15px !important;
        color: #000000 !important;
        background-color: #E7E6E5 !important;
        border: none !important;
        border-radius: 18px !important;
        height: 58px !important;
        padding-left: 18px !important;
    }

    div[data-testid="stButton"] button {
        background-color: #E7E6E5 !important;
        border: none !important;
        font-family: "Syne", sans-serif !important;
        font-size: 15px !important;
        border-radius: 18px !important;
        height: 40px !important;
        width: 100% !important;
        color: #000000 !important;
    }

    div[data-testid="stButton"] button:hover {
        background-color: #DCDAD9 !important;
        color: #000000 !important;
        transform: translateY(-2px);
    }

    div[data-testid="stButton"] button [data-testid="stIconMaterial"] {
        font-size: 30px !important;
        color: #000000 !important;
    }

    .skin-textbox {
        background-color: #E2E1DF;
        border-radius: 20px;
        padding: 25px 30px;
        margin-top: 25px;
        width: 100%;
        max-height: 400px;
        overflow-y: auto;
        overflow-x: hidden;
        color: #1A1A1A;
        font-family: "Quicksand", sans-serif;
        font-size: 15px;
        font-weight: 500;
        line-height: 1.6;
        text-align: justify;
    }

    .skin-textbox-title {
        font-family: "Quicksand", sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #000000;
        margin-bottom: 12px;
    }
    </style>

    <div class="knowrights-title">
        Know Your Rights
    </div>
    <div class="search-subtitle">
        Understand your legal rights in simple language.
    </div>
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
     background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120' fill='none' stroke='%233A2E2B' stroke-width='0.8' stroke-linecap='round' stroke-linejoin='round'%3E%3C!-- Ambient Ray Background Lines --%3E%3Cpath d='M60 10 L60 2' stroke-dasharray='2 2' stroke-width='0.5'/%3E%3Cpath d='M25 25 L18 18' stroke-width='0.5'/%3E%3Cpath d='M95 25 L102 18' stroke-width='0.5'/%3E%3Cpath d='M10 60 L2 60' stroke-dasharray='2 2' stroke-width='0.5'/%3E%3C!-- Protective Legal Shield Border --%3E%3Cpath d='M60 110 C90 90, 105 65, 105 30 L60 12 L15 30 C15 65, 30 90, 60 110 Z' stroke-width='1.2'/%3E%3Cpath d='M60 103 C85 85, 98 62, 98 33 L60 17 L22 33 C22 62, 35 85, 60 103 Z' stroke-opacity='0.4'/%3E%3C!-- Open Guidance Book inside Shield --%3E%3Cpath d='M35 75 C45 70, 55 72, 60 76 C65 72, 75 70, 85 75 V45 C75 40, 65 42, 60 46 C55 42, 45 40, 35 45 Z' fill='%233A2E2B' fill-opacity='0.08' stroke-width='1'/%3E%3Cpath d='M60 46 V76' stroke-width='1'/%3E%3C!-- Small Scales Emblem Over Book --%3E%3Cpath d='M60 25 V42' stroke-width='1.2'/%3E%3Cpath d='M44 32 H76' stroke-width='1.2'/%3E%3Cpath d='M44 32 L38 44 H50 Z'/%3E%3Cpath d='M76 32 L70 44 H82 Z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.05;
    pointer-events: none;
    z-index: 0;
}
</style>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([9, 1], gap="small")

    with col1:
        category = st.text_input(
            "Search",
            placeholder="Search a legal topic...",
            label_visibility="collapsed",
            key="legal_search"
        )

    with col2:
        search_clicked = st.button(
            "",
            icon=":material/search:",
            key="search_btn",
            type="tertiary",
            use_container_width=True
        )

    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

    with btn_col1:
        btn_women = st.button("👩🏻 Women Rights", key="btn_women", use_container_width=True)

    with btn_col2:
        btn_employment = st.button(" 💼 Employment Rights", key="btn_emp", use_container_width=True)

    with btn_col3:
        btn_cyber = st.button("🛡️ Cybercrime", key="btn_cyber", use_container_width=True)

    with btn_col4:
        btn_consumer = st.button("🛒 Consumer Rights", key="btn_consumer", use_container_width=True)

    selected_topic = None

    if search_clicked and category:
        selected_topic = category
    elif btn_women:
        selected_topic = "Women Rights"
    elif btn_employment:
        selected_topic = "Employment Rights"
    elif btn_cyber:
        selected_topic = "Cybercrime"
    elif btn_consumer:
        selected_topic = "Consumer Rights"

    if selected_topic:
         with st.spinner("Searching and Generating your answer..."):
            result = generate_response(selected_topic)

         overview_html = "".join([f"<p>{p}</p>" for p in to_list(result.get("overview", []))])
         rights_html = "".join([f"<p>{p}</p>" for p in to_list(result.get("your_rights_explained", []))])
         more_html = "".join([f"<li>{m}</li>" for m in to_list(result.get("more_information", []))])

         html = '<div class="skin-textbox">'
         html += f'<div class="skin-textbox-title">{selected_topic}</div>'
         html += f'<div class="skin-textbox-title" style="font-size:17px;">Overview</div>{overview_html}'
         html += f'<div class="skin-textbox-title" style="font-size:17px;">Your Rights</div>{rights_html}'
         html += f'<div class="skin-textbox-title" style="font-size:17px;">Learn More</div>'
         html += f'<p>If you want to learn more, you can refer to the following:</p><ul>{more_html}</ul>'
         html += '<i style="font-size:13px;">This is general information, not official legal advice.</i>'
         html += '</div>'

         st.markdown(html, unsafe_allow_html=True)