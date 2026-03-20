from fastapi import FastAPI
from app.routes import analyze

app = FastAPI(
    title="AI Resume Screening API",
    version="1.0.0"
)

app.include_router(analyze.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}