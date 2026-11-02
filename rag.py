import os
import json
import groq
from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))

def classify_case(description, docs_text="", evidence_text=""):
    system_prompt = """You are a legal intent classifier for Pakistan law. 
    Read the user's case description and available text. 
    Return a strict JSON object with two keys:
    1. "area": Choose strictly from one of these folders: [cyber, consumer, rent, police, banking, employment, harassment, family, property, utilities, general].
    2. "case_line": A clean, objective search query in English (20-30 words) summarizing the legal issue without names or CNICs.
    If unclear, default to area: "general".
    Return ONLY valid JSON."""
    
    user_content = f"Description: {description}\nDocs: {docs_text[:500]}\nEvidence: {evidence_text[:500]}"
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {"area": "general", "case_line": description[:300]}

def retrieve_chunks(area, case_line):
    chunks = []
    try:
        folder_path = os.path.join("database", area)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".txt"):
                    with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            chunks.append(content)
    except Exception:
        pass
    return chunks[:4]

def analyze_case(description, docs_text, evidence_text, law_chunks):
    laws_combined = "\n---\n".join(law_chunks) if law_chunks else "Rely on general legal principles and Pakistan law framework."
    
    system_prompt = """You are an expert legal triage and advisory AI for Pakistan.
    Analyze the case based on the provided user text, evidence, and legal context chunks.
    Use the provided legal context chunks as a supporting reference, but also apply your broader legal understanding and general intelligence regarding Pakistan law to give a complete and natural analysis, even if the case extends beyond the exact chunks.
    Rules:
    - Do not mention specific jail punishments or complex procedural article numbers in output.
    - Keep tone professional, advisory, and supportive.
    - Calculate score based on 6 criteria breakdown summing up to 100.
    Return a strict JSON object with these keys:
    - category (string): Main category title for UI.
    - authorities (list of strings): Relevant reporting bodies or forums.
    - missing_evidences (list of strings): What proof could strengthen the case.
    - suggestions (list of strings): Actionable next steps.
    - score_breakdown (dict): Points for 6 aspects (total 100).
    - score_reason (string): Short 2-3 lines explaining the score.
    Return ONLY valid JSON."""

    user_content = f"""
    User Description: {description}
    Extracted Documents: {docs_text}
    Extracted Evidence Text: {evidence_text}
    Relevant Law Chunks: {laws_combined}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {
            "category": "General Legal Advisory",
            "authorities": ["Local Police Station / Relevant Authority"],
            "missing_evidences": ["Detailed written timeline", "Receipts or screenshots if any"],
            "suggestions": ["Consult a legal professional for formal representation."],
            "score_breakdown": {"clarity": 10, "evidence": 10, "damages": 15, "liability": 20, "timeline": 10, "jurisdiction": 10},
            "score_reason": "Analysis generated via fallback safety protocol due to network processing."
        }