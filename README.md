# AI Resume Screening System

## Overview
This project is an AI-powered resume screening system designed to automate candidate evaluation against a given job description. It processes multiple resumes, extracts relevant information, computes match scores, and provides explainable insights such as strengths, gaps, and hiring recommendations.

The system acts as a lightweight Applicant Tracking System (ATS) to improve hiring efficiency and decision-making.

---

## Problem Statement
Recruiters often receive a large number of resumes for a single role, making manual screening time-consuming and inconsistent.

This system addresses the problem by:
- Automatically analyzing resumes
- Comparing them with job requirements
- Generating structured, explainable outputs

---

## Features
- Upload job description and multiple resumes (PDF)
- AI-based extraction of skills, experience, and education
- Match score generation (0–100)
- Candidate ranking
- Strengths and gaps identification
- Recommendation:
  - Strong Fit
  - Moderate Fit
  - Not Fit
- Top candidate summary
- Download results as CSV
- Interactive dashboard (Streamlit)

---

## System Architecture

### Input
- Job Description (PDF)
- Multiple resumes (PDF)

### Processing Pipeline
1. Text extraction from PDFs
2. LLM-based structuring using Gemini
3. Scoring using hybrid evaluation
4. Insights generation
5. Ranked output with recommendations

---

## Scoring Methodology

The system uses a weighted scoring model:

- Skill Match (30%)
- Semantic Similarity (30%)
- Experience (20%)
- Education (10%)
- Skill Richness (10%)
- Penalty for missing critical skills

Semantic similarity is computed using Sentence Transformers (MiniLM) and cosine similarity.

---

## Tech Stack

### Backend
- FastAPI
- Python

### AI / ML
- Google Gemini API
- Sentence Transformers (MiniLM)
- Scikit-learn

### Frontend
- Streamlit

### Data Processing
- pdfplumber

---

## Project Structure

```

ai-resume-screening/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── config.py
│
├── frontend/
│   └── app.py
│
├── data/
├── requirements.txt
└── README.md

```

---

## How to Run

### 1. Install dependencies
```

pip install -r requirements.txt

```

### 2. Set environment variables
Create a `.env` file:
```

GEMINI_API_KEY=your_api_key

```

### 3. Run backend
```

uvicorn app.main:app --reload

```

### 4. Run frontend
```

streamlit run frontend/app.py

```

---

## Usage
1. Upload job description
2. Upload resumes
3. Click "Analyze Candidates"
4. View results and rankings
5. Download results as CSV

---

## Design Decisions
- Combined LLM tasks to reduce API calls
- Used structured extraction for consistency
- Integrated semantic similarity for contextual matching
- Implemented penalty-based scoring for differentiation
- Designed stateless system for simplicity

---

## Limitations
- Depends on LLM output quality
- No persistent storage (MVP)
- Limited handling of very large files

---

## Future Improvements
- Add database integration
- Improve experience parsing
- Add ATS workflow features
- Deploy on cloud
- Enhance scoring with domain-specific tuning

---

## Conclusion
This project demonstrates a practical AI solution for resume screening by combining LLMs, embeddings, and rule-based scoring into a usable and explainable system.
