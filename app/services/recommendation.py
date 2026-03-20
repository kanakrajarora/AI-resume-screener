def get_recommendation(score):
    if score >= 75:
        return "Strong Fit"
    elif score >= 50:
        return "Moderate Fit"
    return "Not Fit"