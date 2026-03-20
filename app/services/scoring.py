from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(text1, text2):
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    return cosine_similarity(emb1, emb2)[0][0]


def compute_score(jd_data, resume_data):
    jd_skills = set(jd_data.get("skills", []))
    resume_skills = set(resume_data.get("skills", []))

    # Skill overlap (30%)
    if jd_skills:
        overlap = len(jd_skills & resume_skills) / len(jd_skills)
    else:
        overlap = 0
    skill_score = overlap * 30

    # Semantic similarity (30%)
    jd_text = " ".join(jd_skills)
    resume_text = " ".join(resume_skills)

    sim = compute_similarity(jd_text, resume_text)
    semantic_score = sim * 30

    # Experience scoring (20%)
    exp_text = resume_data.get("experience", "").lower()

    if "year" in exp_text:
        exp_score = 20
    elif "intern" in exp_text:
        exp_score = 15
    else:
        exp_score = 8

    # Education (10%)
    edu_score = 10 if resume_data.get("education") else 5

    # Skill richness (10%)
    richness = min(len(resume_skills), 20) / 20
    richness_score = richness * 10

    # Missing critical skills penalty
    missing_skills = jd_skills - resume_skills
    penalty = min(len(missing_skills), 5) * 2  # max -10

    total = skill_score + semantic_score + exp_score + edu_score + richness_score - penalty

    return int(max(0, min(total, 100)))