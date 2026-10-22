import streamlit as st
import time
import json
import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from pypdf import PdfReader
from docx import Document as DocxDocument
from fpdf import FPDF
import re
import base64

load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def create_case_folders(case_id):
    base = Path("History") / case_id
    (base / "evidence").mkdir(parents=True, exist_ok=True)
    (base / "analysis").mkdir(parents=True, exist_ok=True)
    (base / "generated").mkdir(parents=True, exist_ok=True)
    return base

def extract_text_from_docs(docs):
    combined_text = ""

    if not docs:
        return combined_text

    for file in docs:
        name = file.name.lower()

        if name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    combined_text += page_text + "\n"

        elif name.endswith(".docx"):
            doc = DocxDocument(file)
            for para in doc.paragraphs:
                combined_text += para.text + "\n"

        else:
            combined_text += f"[Could not read file: {file.name}]\n"

    return combined_text

def save_uploaded_files(base, docs, evidence):
    if docs:
        for file in docs:
            file_path = base / "evidence" / file.name
            with open(file_path, "wb") as f:
                f.write(file.getvalue())

    if evidence:
        for file in evidence:
            file_path = base / "evidence" / file.name
            with open(file_path, "wb") as f:
                f.write(file.getvalue())

def save_analysis(base, analysis_data, problem_text):
    record = {
        "problem": problem_text,
        "analysis": analysis_data
    }

    with open(base / "analysis" / "analysis.json", "w") as f:
        json.dump(record, f)

def clean(text):
    text = str(text)

    replacements = {
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


def add_heading(pdf, text):
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, clean(text), new_x="LMARGIN", new_y="NEXT")


def add_body(pdf, text):
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, clean(text), new_x="LMARGIN", new_y="NEXT")


def build_case_report_pdf(problem_text, result):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Case Analysis Report", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    add_heading(pdf, "Problem Description")
    add_body(pdf, problem_text)
    pdf.ln(4)

    add_heading(pdf, "Category")
    add_body(pdf, result.get("category", "N/A"))
    pdf.ln(4)

    add_heading(pdf, "Legal Readiness Score")
    add_body(pdf, f"{result.get('score', 'N/A')}% - {result.get('score_status', '')}")
    pdf.ln(4)

    add_heading(pdf, "Relevant Authorities")
    for item in result.get("authorities", []):
        add_body(pdf, f"- {item}")
    pdf.ln(4)

    add_heading(pdf, "Missing Evidences")
    for item in result.get("missing_evidences", []):
        add_body(pdf, f"- {item}")
    pdf.ln(4)

    add_heading(pdf, "Suggestions")
    for item in result.get("suggestions", []):
        add_body(pdf, f"- {item}")

    return bytes(pdf.output())

VISION_MODEL = "qwen/qwen3.8-27b"

def describe_evidence_images(evidence):
    if not evidence or client is None:
        return ""

    descriptions = []
    for file in evidence[:2]:
        try:
            b64 = base64.b64encode(file.getvalue()).decode("utf-8")
            mime = "image/png" if file.name.lower().endswith(".png") else "image/jpeg"

            response = client.chat.completions.create(
                model=VISION_MODEL,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text":
                            "This image is evidence in a legal case in Pakistan. "
                            "Write down every readable text, name, amount, date and "
                            "important detail you can see. Do not guess or invent anything. "
                            "Reply in plain English, maximum 120 words."},
                        {"type": "image_url",
                         "image_url": {"url": f"data:{mime};base64,{b64}"}}
                    ]
                }],
                temperature=0.1,
                max_completion_tokens=400,
                timeout=40.0
            )
            text = response.choices[0].message.content or ""
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

            if not text:
                print(f"VISION WARNING: empty answer for {file.name}")
                descriptions.append(f"[Could not read image: {file.name}]")
            else:
                descriptions.append(f"Image '{file.name}': {text}")

        except Exception as e:
            print(f"VISION ERROR for {file.name}: {e}")
            descriptions.append(f"[Could not read image: {file.name}]")

    return "\n".join(descriptions)

def calculate_readiness(checklist, has_images):
    image_words = ["screenshot", "photo", "picture", "image", "chat", "message"]

    provided_count = 0
    missing = []

    for entry in checklist:
        item = str(entry.get("item", "")).strip()
        provided = str(entry.get("provided", "")).lower() == "true"

        if has_images and any(word in item.lower() for word in image_words):
            provided = True

        if provided:
            provided_count += 1
        else:
            missing.append(item)

    score = round(100 * provided_count / len(checklist))
    return score, missing[:4]


def analyze_case(problem, docs, evidence):
    docs_text = extract_text_from_docs(docs)
    evidence_text = describe_evidence_images(evidence)
    doc_names = [f.name for f in docs] if docs else []
    image_names = [f.name for f in evidence] if evidence else []

    prompt = f"""
    You are a legal case analyzer for Pakistan. A user describes a legal problem below.
    The problem may be written in English, Urdu or Roman Urdu. Understand the meaning.

    User's problem: {problem}

    Uploaded documents: {doc_names if doc_names else "none"}
    Text extracted from the documents: {docs_text[:1500] if docs_text else "none"}
    Uploaded evidence images (you cannot see inside them, the file names are only a hint): {image_names if image_names else "none"}
    Details read from evidence images: {evidence_text[:1500]}

    Respond in English, in ONLY valid JSON, matching this exact shape with no extra text before or after:
    {{
        "category": "short case category",
        "authorities": ["authority 1", "authority 2", "authority 3"],
        "evidence_checklist": [
            {{"item": "short evidence name", "provided": true}},
            {{"item": "short evidence name", "provided": false}}
        ],
        "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
    }}

    Rules:
    - evidence_checklist: exactly 6 items. These are the evidence items normally needed for this
      kind of case in Pakistan. Each item is 2 to 4 words only.
    - Set "provided" to true only if the problem text, the document text, or an uploaded file name
      clearly shows that the user already has that item. Otherwise set it to false.
    - missing_evidences: do not list anything that already appears in the  documents or evidence images above.
    - Be honest. Do not mark an item as provided just to be encouraging.
    - authorities: maximum 3 items, official names only, no explanation.
    - suggestions: maximum 4 items, each one clear sentence under 25 words.
    - Do NOT include any links, URLs, or website addresses.
    - Do NOT use markdown formatting (no *, no [ ], no **).
    - Use plain ASCII characters only: normal hyphen (-) and straight quotes.
    - Never invent law names or section numbers. Stay general if unsure.
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

        checklist = data.get("evidence_checklist", [])
        if len(checklist) == 0:
            raise ValueError("AI did not return an evidence checklist")

        score, missing = calculate_readiness(checklist, len(image_names) > 0)

        data["score"] = score
        data["missing_evidences"] = missing

        if score >= 90:
            data["score_status"] = "Excellent Preparation"
        elif score >= 70:
            data["score_status"] = "Good Preparation"
        elif score >= 40:
            data["score_status"] = "Moderate Preparation"
        else:
            data["score_status"] = "Weak Preparation"

    except Exception as e:
        data = {
            "category": "Unable to analyze",
            "authorities": [],
            "score": 0,
            "score_status": "Analysis failed",
            "missing_evidences": [],
            "suggestions": [f"Something went wrong: {e}. Please try again."]
        }

    return data

def build_gauge_html(score):
    try:
        score = max(0, min(100, float(score)))
    except (TypeError, ValueError):
        score = 0

    shown = int(round(score))
    arc_length = 3.14159265 * 80
    filled = arc_length * score / 100

    html = '<div style="width:100%; max-width:260px; margin:0 auto;">'
    html += '<svg viewBox="0 0 200 112" width="100%" xmlns="http://www.w3.org/2000/svg">'
    html += '<path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#DDD8D2" stroke-width="20"/>'
    html += f'<path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#8f3511" stroke-width="20" stroke-dasharray="{filled:.2f} {arc_length:.2f}"/>'
    html += f'<text x="100" y="94" text-anchor="middle" font-size="34" fill="#000000" style="font-family: Cormorant Garamond, serif;">{shown}%</text>'
    html += '</svg>'
    html += '</div>'
    return html

def render_case_result(result):

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

 
    .result-container {
        font-family: 'Cormorant Garamond', serif;
        color: #000000;
        margin-top:3px;
    }

    .section-title {
        font-family: 'Cormorant Garamond', serif;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 15px;
        margin-top: -2rem;
    }

    .icon {
        font-family: 'Material Symbols Outlined';
        font-size: 24px;

    }

    .custom-card {
        font-family: 'Cormorant Garamond', serif;
        background-color: #E2E1DF;
        border-radius: 18px;
        padding: 15px 20px;
        font-size: 18px;
        margin-bottom: 15px;
        
    }

    .score-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 14px;
        color: #000000;
        margin-top: 4px;
    }

    .status-text {
        font-family: 'Cormorant Garamond', serif;
        text-align: center;
        font-size: 20px;
        margin-top: 15px;
        font-weight: 500;
    }

    .suggestion-box {
        font-family: 'Cormorant Garamond', serif;
        background-color: #E2E1DF;
        border-radius: 20px;
        padding: 25px 35px;
        margin-top: 2.5px;
        margin-bottom: 13px;
    }

    .suggestion-box ul {
        margin: 0;
        padding-left: 20px;
    }

    .suggestion-box li {
        font-family: 'Cormorant Garamond', serif;
        font-size: 20px;
        margin-bottom: 6px;
        color: #000000;
    }

    [data-testid="stPlotlyChart"] {
        border-radius: 18px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
            <div class="section-title">
                <span class="icon">account_balance</span>
                <span>Authority Finder</span>
            </div>
            <p style="font-size: 18px; margin-bottom: 5px;">Case Category:</p>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="custom-card">{result["category"]}</div>', unsafe_allow_html=True)

        st.markdown('<p style="font-size: 18px; margin-top: 20px; margin-bottom: 5px;">Tailored Suggestions:</p>', unsafe_allow_html=True)

        auth_html = "<br>".join([f"{i+1}. {auth}" for i, auth in enumerate(result["authorities"])])
        st.markdown(f'<div class="custom-card">{auth_html}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="section-title">
                <span class="icon">bar_chart</span>
                <span>Legal Readiness Score</span>
            </div>
        """, unsafe_allow_html=True)

        score_col1, score_col2 = st.columns([1.2, 1])

        with score_col1:
            st.markdown(build_gauge_html(result["score"]), unsafe_allow_html=True)

            st.markdown(f'<p class="score-text" style="text-align:center;">{result["score_status"]}</p>', unsafe_allow_html=True)

        with score_col2:
            st.markdown('<p style="font-size: 18px; width:100%; margin-bottom: 8px;">Missing Evidences:</p>', unsafe_allow_html=True)
            missing_html = "".join([f"<li>{item}</li>" for item in result["missing_evidences"]])
            st.markdown(f'<div class="custom-card"><ul>{missing_html}</ul></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("""
        <div class="section-title">
            <span class="icon">chat_bubble_outline</span>
            <span>Suggestions</span>
        </div>
    """, unsafe_allow_html=True)

    sug_html = "".join([f"<li>{sug}</li>" for sug in result["suggestions"]])
    st.markdown(f'<div class="suggestion-box"><ul>{sug_html}</ul></div>', unsafe_allow_html=True)

def run():
    
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&display=swap');

.casehub-title {
    font-family: "Neue Machina", sans-serif;
    font-size: 42px;
    font-weight: 800;
    color: #000000;
    margin-top: -7.9rem;
    text-align: left;
    margin-bottom: 0.1rem;
    padding-bottom: 12px;
    border-bottom: 1.5px solid #9a9a9a;
    margin-bottom: 30px;


}
</style>

<div class="casehub-title">CaseHub</div>
""", unsafe_allow_html=True)
    
    st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    position: relative;
}

[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    bottom: 15px;
    right: 15px;
    width: 380px;
    height: 380px;

    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120' fill='none' stroke='%233A2E2B' stroke-width='0.8' stroke-linecap='round' stroke-linejoin='round'%3E%3C!-- Subtle Background Geometric Accents --%3E%3Cpath d='M20 110 L110 20' stroke-dasharray='2 2' stroke-width='0.4'/%3E%3Cpath d='M40 110 L110 40' stroke-width='0.5'/%3E%3C!-- Desk Line --%3E%3Cpath d='M15 95 H110' stroke-width='1.2'/%3E%3C!-- Desk Lamp on Right Side --%3E%3Cpath d='M100 95 V45 C100 30, 85 25, 75 25' stroke-width='1.2'/%3E%3Cpath d='M78 22 L65 32 L80 38 Z' fill='%233A2E2B' fill-opacity='0.15' stroke-width='1'/%3E%3C!-- Light Rays from Lamp onto Books --%3E%3Cline x1='70' y1='34' x2='45' y2='65' stroke-dasharray='1.5 1.5' stroke-width='0.5'/%3E%3Cline x1='76' y1='36' x2='65' y2='65' stroke-dasharray='1.5 1.5' stroke-width='0.5'/%3E%3C!-- Stacked Legal Books directly under light --%3E%3Crect x='35' y='68' width='45' height='7' rx='1' fill='%233A2E2B' fill-opacity='0.05'/%3E%3Crect x='32' y='75' width='50' height='8' rx='1'/%3E%3Crect x='28' y='83' width='56' height='12' rx='1' fill='%233A2E2B' fill-opacity='0.08'/%3E%3C!-- Gavel & Sound Block on Left --%3E%3Cellipse cx='92' cy='93' rx='7' ry='2' fill='%233A2E2B' fill-opacity='0.2'/%3E%3Crect x='85' y='86' width='8' height='5' rx='1' transform='rotate(-20 85 86)' stroke-width='1'/%3E%3Cpath d='M88 86 L80 75' stroke-width='1.2'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right bottom;
    background-size: contain;
    opacity: 0.06;
    pointer-events: none;
    z-index: 999; 
}
</style>
""", unsafe_allow_html=True)
    page = st.empty()

    if "case_result" in st.session_state:
        with page.container():
          render_case_result(st.session_state["case_result"])

        if st.button("New Case"):
            del st.session_state["case_result"]
            st.rerun()
        return

    with page.container():
        st.markdown("""
        <div class="description">
       <span class="icon">edit_document</span>
       <span>Describe Your Problem</span>

       </div>
       """, unsafe_allow_html=True)

        st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gilda+Display&display=swap');

    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');

   .description {
     display: flex;
     align-items: left;
     transform: translateY(-5px);
     font-family: "Gilda Display", serif;
     font-size: 20px;
     font-weight: 400;
     color: #171717;
     gap:10px;
     margin-top:-1.9rem;
}

.description .icon {
    font-family: 'Material Symbols Outlined';
    font-size: 20px;
    color: #555555;
}
.stTextArea textarea {
    font-family: "Gilda Display", serif;
    font-size: 13px;
    font-weight: 200;
    font-decoration:bold;
    color: #000000;  !important;
    opacity: 1;
    background-color: #F0EFED;
    border-radius: 10px;
    border: 1px solid #808080;
}
  .upload{
      display: flex;
      align-items: left;
      margin-top:1.1rem;
      margin-bottom:1rem;
      transform: translateY(-5px);
      font-family: "Gilda Display", serif;
      font-size: 20px;
      font-weight: 400;
      color: #171717;
      gap:10px;
 }

 .upload .icon {
    font-family: 'Material Symbols Outlined';
    font-size: 20px;
    color: #555555;
    font-weight: normal;
}
[data-testid="stFileUploader"]{
font-family: "Gilda Display", serif;
color: #171717;
}
[data-testid="stFileUploaderDropzone"] {
    background-color: #F0EFED;
    border-radius: 10px;
    border: 1px solid #808080;
    }
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #000000 !important;
    font-size: 20px;
     opacity: 1;
    font-family: "Gilda Display", serif;
}

/* Analyze Case / Primary Button */
.stButton button {
    background: #594239;
    color: #FFFFFF !important;
    border: 1px solid #252525;
    border-radius: 11px;
    width: 189px !important;
    font-family: "Gilda Display", serif;
    font-size: 19px;
    font-weight: 400;
    padding: 10px 24px;

    box-shadow:
        0 2px 4px rgba(0, 0, 0, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);

    transition: all 0.25s ease;
}

/* Hover */
.stButton button:hover {
    background: linear-gradient(135deg, #505050, #3E3E3E);
    color: #FFFFFF;
    border-color: #505050;

    transform: translateY(-2px);

    box-shadow:
        0 7px 16px rgba(0, 0, 0, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.10);
}

.stButton button:active {
    transform: translateY(0px);

    box-shadow:
        0 2px 5px rgba(0, 0, 0, 0.12);
}

</style>
""", unsafe_allow_html=True)

        problem = st.text_area("Problem", placeholder="Type your problem briefly here.",label_visibility="collapsed")

        st.markdown("""
                <div class="upload">
               <span class="icon">cloud_upload</span>
               <span>Upload Details</span>

               </div>
               """, unsafe_allow_html=True)
        col1, col2,col3 = st.columns([2,2,1])
        with col1:
            docs = st.file_uploader("Upload Documents", type=["pdf", "doc", "docx"],accept_multiple_files=True)
        with col2:
            evidence = st.file_uploader("Upload Evidence", type=["png", "jpg", "jpeg"],accept_multiple_files=True)
        with col3:
            st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)
            analyze = st.button("Analyze Case")
    if analyze:
        
        if not problem or not problem.strip():
            st.warning("Please first describe the problem!")
            st.stop()
            
        if not docs and not evidence:
            st.warning("Please upload evidence or document details!")
            st.stop()
        page.empty()

        spinner_placeholder = st.empty()
        spinner_placeholder.markdown("""
        <div class="analyzing-container">
            <div class="loader"></div>
            <span>Analyzing....</span>
        </div>

        <style>
        .analyzing-container {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Gilda Display', serif;
            font-size: 26px;
            color: #171717;
            font-weight: 500;
        }

        .loader {
            width: 20px;
            height: 20px;
            border: 3px solid #d9d9d9;
            border-top: 3px solid #171717;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        </style>
        """, unsafe_allow_html=True)

        try:
            result = analyze_case(problem, docs, evidence)

            case_id = f"Case_{int(time.time())}"
            base = create_case_folders(case_id)
            save_uploaded_files(base, docs, evidence)
            save_analysis(base, result, problem)

            try:
                report_pdf_bytes = build_case_report_pdf(problem, result)
                with open(base / "generated" / "case_report.pdf", "wb") as f:
                    f.write(report_pdf_bytes)
            except Exception as pdf_e:
                print(f"PDF Error: {pdf_e}")

            spinner_placeholder.empty()
            st.session_state["case_result"] = result
            st.rerun()

        except Exception as e:
            spinner_placeholder.empty()
            st.error(f"Something went wrong: {e}")