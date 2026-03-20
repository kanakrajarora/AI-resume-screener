import google.generativeai as genai
from app.config import GEMINI_API_KEY, MODEL_NAME
from app.utils.helpers import safe_json_loads

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def call_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text


def extract_jd_info(text):
    prompt = f"""
    Extract structured data from this job description.

    Return ONLY valid JSON:
    {{
        "skills": [],
        "experience": "",
        "education": ""
    }}

    JD:
    {text}
    """

    output = call_gemini(prompt)
    return safe_json_loads(output)


def analyze_resume(jd, resume_text):
    prompt = f"""
You are a senior technical recruiter and resume analyst.

Your task is to:
1. Extract structured candidate information
2. Evaluate candidate-job fit
3. Provide concise hiring insights

Think step-by-step internally, but output only final JSON.

---

### Tasks:

#### 1. Extract Resume Information:
- Identify key technical and relevant skills
- Normalize skill names (e.g., "Python programming" → "Python")
- Summarize experience (roles, years, domain)
- Extract highest or most relevant education

#### 2. Evaluate Fit Against Job Description:
- Compare skills, experience, and domain alignment
- Identify strong matches
- Identify missing or weak areas

---

### Output Format (STRICT JSON ONLY):

{{
    "skills": ["list of normalized relevant skills"],
    "experience": "concise summary of experience",
    "education": "highest or relevant education",

    "strengths": [
        "specific strength 1",
        "specific strength 2",
        "specific strength 3"
    ],

    "gaps": [
        "specific gap 1",
        "specific gap 2",
        "specific gap 3"
    ]
}}

---

### Rules:
- Return ONLY valid JSON (no explanation, no markdown, no ```).
- Do NOT hallucinate information not present in resume.
- Keep strengths/gaps concise (max 10–12 words each).
- If any field is missing, return empty string or empty list.
- Base evaluation strictly on given data.

---

### Job Description:
{jd}

---

### Resume:
{resume_text}
"""

    output = call_gemini(prompt)
    return safe_json_loads(output)