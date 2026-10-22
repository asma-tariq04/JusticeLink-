import streamlit as st
import os
from pathlib import Path
from fpdf import FPDF
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def file_time(folder):
    return (folder / "analysis" / "analysis.json").stat().st_mtime


def load_latest_case():
    history_folder = Path("History")

    if not history_folder.exists():
        return None

    folders = []
    for folder in history_folder.iterdir():
        if (folder / "analysis" / "analysis.json").exists():
            folders.append(folder)

    folders.sort(key=file_time, reverse=True)

    for folder in folders:
        try:
            with open(folder / "analysis" / "analysis.json", "r") as f:
                record = json.load(f)
        except Exception:
            continue

        result = record.get("analysis", {})
        if result.get("category") == "Unable to analyze":
            continue

        return {
            "problem": record.get("problem", ""),
            "result": result,
            "base": str(folder)
        }

    return None
def clean(text):
    text = str(text)

    replacements = {
        "Rs.": "Rs. ",
        "RS.": "Rs. ",
        "rs.": "Rs. ",
        "PKR": "PKR ",
        "â€": "",
        "\u2011": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.encode("latin-1", "replace").decode("latin-1")


def generate_letter_text(selected_document, document_type, case):
    result = case["result"]
    authorities = result.get("authorities", [])
    main_authority = authorities[0] if authorities else "the concerned authority"

    prompt = f"""
    You are an expert Pakistani legal editor drafting a highly professional, grammatically error-free document.

    Document Request:
    - Selected Category: {selected_document} (e.g. Email, Formal Application, or Complaint)
    - Chosen Style: {document_type}

    Case Details:
    - User's Problem Description: {case["problem"]}
    - Category: {result.get("category", "")}
    - Recipient/Authority to address: {main_authority}

    FORMATTING RULES BY DOCUMENT CATEGORY:

    IF Document Category is "Email":
    - Format strictly as a professional email.
    - Top lines must be:
      To: [Recipient Email / {main_authority}]
      Subject: [Clear, concise subject line summarizing the issue]
    - Opening: Dear [Name/Title],
    - Body: 2 or 3  short paragraphs (Issue summary & precise resolution requested).
    - Closing: "Best regards," followed by [Your Full Name], [Your Contact Information].

    IF Document Category is "Formal Application" OR "Complaint":
    - Format as a standard Pakistani formal letter/application.
    - Top line: Date: [Date]
    - Addressing block: 
      To,
      {main_authority},
      [City/Location]
    - Subject line: Subject: [Formal application/complaint title]
    - Opening: Respected Sir/Madam,
    - Body: 2 to 3 paragraphs detailing facts, impact/loss, and explicit action requested.
    - Closing: "Yours faithfully," or "Yours sincerely," followed by:
      [Your Full Name]
      [Your CNIC Number]
      [Your Address]
      [Your Phone Number]

    CRITICAL QUALITY & LANGUAGE RULES:
    1. Perfect English Grammar: Ensure clean syntax, correct tenses, and formal terminology.
    2. Currency Format: Always format currency strictly as "PKR 1,500" or "Rs. 1,500". NEVER write "rs?", "rs.", or unformatted numbers.
    3. ASCII Standard: Use standard ASCII characters only. Do not use special symbols, smart quotes, bullets (*, #), or markdown bolding.
    4. Facts & Placeholders: Stick strictly to provided facts. Use square brackets like [City Name] for missing information.
    5. No Citations: Do not cite legal acts, section numbers, or external URLs.
    6. Length: Keep under 230 words to fit easily on a single page.
    7. Output: Output ONLY the letter text without commentary or conversational preambles.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            timeout=30.0
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", e)
        return None


def build_letter_pdf(letter_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, clean(letter_text), new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())

@st.dialog("Download your Document")
def show_download_dialog(selected_document, pdf_bytes):
    st.markdown(
        "<p style='font-family:\"Gilda Display\", serif; font-size:15px;'>"
        "Click here on the pdf icon to download your document</p>",
        unsafe_allow_html=True
    )


    st.markdown("""
    <style>
    div[data-testid="stDownloadButton"] button {
        background-color: #E7E6E5 !important;
        border: none !important;
        border-radius: 15px !important;
        width: 140px !important;
        height: 110px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        font-family: "Gilda Display", serif !important;
        color: #171717 !important;
        padding: 0 !important;
    }
    div[data-testid="stDownloadButton"] button [data-testid="stIconMaterial"] {
        font-size: 40px !important;
        color: #E63946 !important;
    }

    
    </style>
""", unsafe_allow_html=True)

    left, center, right = st.columns([1, 1, 1])
    with center:
        st.download_button(
            label="Download",
            data=pdf_bytes,
            file_name=f"{selected_document}.pdf",
            mime="application/pdf",
            icon=":material/picture_as_pdf:"
        )

def run():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

    .complaint-title {
        font-family: "SyI", sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: #000000;
        margin-top: -5.9rem;
        text-align: left;
        padding-bottom: 12px;
        border-bottom: 1.5px solid #9a9a9a;
        margin-bottom: 15px;
    }

    .complaint-subtitle {
        font-family: "Gilda Display", serif;
        font-size: 18px;
        font-weight: 400;
        color: #171717;
        margin-bottom: 18px;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #E7E6E5 !important;
        border: none !important;
        border-radius: 15px !important;
        min-height: 45px;
    }

    .stSelectbox div[data-baseweb="select"] div {
        color: #171717;
        font-family: "Gilda Display", serif;
        font-size: 15px;
    }

    div[data-testid="stButton"] button {
        background-color: #E7E6E5 !important;
        border: none !important;
        font-family: "Gilda Display", serif !important;
        font-size: 19px !important;
        border-radius: 15px !important;
        min-height: 63px !important;
        width: 100% !important;
        color: #222222 !important;
    }

    div[data-testid="stButton"] button:hover {
        background-color: #DCDAD9 !important;
        color: #000000 !important;
        transform: translateY(-2px);
    }

    div[data-testid="stButton"] button [data-testid="stIconMaterial"] {
        font-size: 28px !important;
        color: #222222 !important;
    }

    .icon {
        font-family: 'Material Symbols Outlined';
        font-size: 24px;
    }

    </style>

    <div class="complaint-title">
        Complaint Generator
    </div>

    <div class="complaint-subtitle">
        Generate professional legal documents based on your case.
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

    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120' fill='none' stroke='%233A2E2B' stroke-width='0.8' stroke-linecap='round' stroke-linejoin='round'%3E%3C!-- Subtle Document Border Frame --%3E%3Cpath d='M30 110 H110 V30' stroke-width='0.5' stroke-dasharray='3 3'/%3E%3Crect x='102' y='102' width='8' height='8' fill='none' stroke='%233A2E2B' stroke-width='0.6'/%3E%3C!-- Main Scroll Document --%3E%3Cpath d='M35 20 C25 20, 20 25, 20 30 C20 35, 25 35, 30 35 H90 C95 35, 100 30, 100 25 C100 20, 95 20, 90 20 Z' stroke-width='1.2' fill='%233A2E2B' fill-opacity='0.05'/%3E%3Cpath d='M30 35 V90 C30 98, 40 98, 45 90 V35' stroke-width='1'/%3E%3Cpath d='M90 35 V85 C90 92, 80 95, 75 90' stroke-width='1'/%3E%3C!-- Text Lines on Scroll --%3E%3Cline x1='48' y1='48' x2='80' y2='48' stroke-width='1'/%3E%3Cline x1='48' y1='56' x2='82' y2='56' stroke-width='1'/%3E%3Cline x1='48' y1='64' x2='78' y2='64' stroke-width='1'/%3E%3Cline x1='48' y1='72' x2='70' y2='72' stroke-width='1'/%3E%3C!-- Feather Quill Pen --%3E%3Cpath d='M95 40 C85 55, 68 75, 52 92 L48 95 L52 88 C68 72, 85 52, 98 32 Z' fill='%233A2E2B' fill-opacity='0.1' stroke-width='1'/%3E%3Cpath d='M95 40 C88 50, 75 65, 62 80' stroke-width='0.6'/%3E%3C!-- Official Wax Seal Emblem --%3E%3Ccircle cx='40' cy='85' r='10' fill='%233A2E2B' fill-opacity='0.15' stroke-width='1.2'/%3E%3Ccircle cx='40' cy='85' r='7' stroke-dasharray='1.5 1.5' stroke-width='0.8'/%3E%3Cpath d='M37 85 L40 82 L43 85 L40 88 Z' fill='%233A2E2B'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.05;
    pointer-events: none;
    z-index: 0;
}
</style>
""", unsafe_allow_html=True)

    document_type = st.selectbox(
        "Select Document Type",
        [
            "Select the type of document you want to generate",
            "Generate Formal Application",
            "General Email",
            "General Complaint",
        ],
        label_visibility="collapsed"
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        generate_email = st.button(
            "Generate Email",
            key="generate_email",
            use_container_width=True,
            icon=":material/mail:"
        )

    with col3:
        generate_complaint = st.button(
            "Generate Complaint",
            key="generate_complaint",
            use_container_width=True,
            icon=":material/report:"
        )

    st.write("")

    left, center, right = st.columns([1, 1, 1])

    with center:
        generate_application = st.button(
            "Generate Formal Application",
            key="generate_application",
            use_container_width=True,
            icon=":material/description:"
        )

    selected_document = None

    if generate_email:
        selected_document = "Email"
    elif generate_complaint:
        selected_document = "Complaint"
    elif generate_application:
        selected_document = "Formal Application"

    if selected_document:

        case = load_latest_case()

        if document_type == "Select the type of document you want to generate":
            st.warning("Please select a document type first.")

        elif case is None:
            st.warning("Please analyze a case in CaseHub first, then come back here.")

        else:
            with st.spinner("Generating..."):
                letter_text = generate_letter_text(selected_document, document_type, case)

            if letter_text is None:
                st.error("Could not generate the document right now. Please try again.")
            else:
                pdf_bytes = build_letter_pdf(letter_text)

                file_name = selected_document.replace(" ", "_") + ".pdf"
                with open(Path(case["base"]) / "generated" / file_name, "wb") as f:
                    f.write(pdf_bytes)

                show_download_dialog(selected_document, pdf_bytes)
if __name__ == "__main__":
    run()