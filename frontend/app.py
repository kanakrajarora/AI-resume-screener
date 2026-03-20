import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/api/analyze"

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("AI Resume Screening System")

st.write("Upload a Job Description and multiple resumes to get AI-based ranking.")

# Upload JD
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

# Upload resumes
resume_files = st.file_uploader(
    "Upload Resumes (Multiple PDFs)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Analyze Candidates"):
    if not jd_file or not resume_files:
        st.warning("Please upload both JD and resumes.")
    else:
        with st.spinner("Analyzing resumes..."):
            files = {
                "jd": ("jd.pdf", jd_file.getvalue(), "application/pdf")
            }

            resume_data = [
                ("resumes", (file.name, file.getvalue(), "application/pdf"))
                for file in resume_files
            ]

            response = requests.post(API_URL, files=[*files.items(), *resume_data])

            if response.status_code == 200:
                data = response.json()
                results = data["results"]
                summary = data.get("summary", {})

                st.success("Analysis Complete!")

                # Top Candidate
                if summary:
                    st.header("Top Candidate")
                    st.success(f"{summary['top_candidate']} (Score: {summary['score']})")
                    st.write(summary["reason"])
                    st.markdown("---")

                for candidate in results:
                    with st.container():
                        st.subheader(f"{candidate['name']}")

                        col1, col2, col3 = st.columns(3)
                        col1.metric("Score", candidate["score"])
                        col2.metric("Recommendation", candidate["recommendation"])

                        st.write("**Strengths:**")
                        st.write(", ".join(candidate["strengths"]))

                        st.write("**Gaps:**")
                        st.write(", ".join(candidate["gaps"]))

                        st.markdown("---")
                
                # Convert results to DataFrame
                df = pd.DataFrame(results)

                # Optional: clean columns
                df = df[["name", "score", "recommendation", "strengths", "gaps"]]

                # Convert lists to readable strings
                df["strengths"] = df["strengths"].apply(lambda x: ", ".join(x))
                df["gaps"] = df["gaps"].apply(lambda x: ", ".join(x))

                # Download button
                st.download_button(
                    label="Download Results as CSV",
                    data=df.to_csv(index=False),
                    file_name="resume_screening_results.csv",
                    mime="text/csv"
                )

            else:
                st.error("Error processing request.")