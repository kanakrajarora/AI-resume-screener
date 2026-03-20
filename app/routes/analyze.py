from fastapi import APIRouter, UploadFile, File
from typing import List

from app.services import parser, llm_service, scoring, recommendation

router = APIRouter()


@router.post("/analyze")
async def analyze_resumes(
    jd: UploadFile = File(...),
    resumes: List[UploadFile] = File(...)
):
    # Extract JD text
    jd_text = await parser.extract_text(jd)
    jd_text = jd_text[:2000]

    # Extract JD structured data
    try:
        jd_data = llm_service.extract_jd_info(jd_text)
    except Exception as e:
        print("JD extraction failed:", e)
        jd_data = {}

    results = []

    for resume in resumes:
        try:
            #Extract resume text
            resume_text = await parser.extract_text(resume)
            resume_text = resume_text[:3000]

            analysis = llm_service.analyze_resume(jd_text, resume_text)

        except Exception as e:
            print("Resume processing failed:", e)

            # fallback to avoid crash
            analysis = {
                "skills": [],
                "experience": "",
                "education": "",
                "strengths": ["Processing failed"],
                "gaps": ["System error"]
            }

        #Split structured output
        resume_data = {
            "skills": analysis.get("skills", []),
            "experience": analysis.get("experience", ""),
            "education": analysis.get("education", "")
        }

        insights = {
            "strengths": analysis.get("strengths", []),
            "gaps": analysis.get("gaps", [])
        }

        #Use JD data in scoring
        score = scoring.compute_score(jd_data, resume_data)

        #Recommendation
        rec = recommendation.get_recommendation(score)

        results.append({
            "name": resume.filename,
            "score": score,
            "strengths": insights["strengths"],
            "gaps": insights["gaps"],
            "recommendation": rec
        })

    # Sort by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    if results:
        top_candidate = results[0]

        summary = {
            "top_candidate": top_candidate["name"],
            "score": top_candidate["score"],
            "reason": "Best alignment with required skills, experience, and job requirements"
        }
    else:
        summary = {}

    # output structured response
    return {
        "results": results,
        "summary": summary
    }