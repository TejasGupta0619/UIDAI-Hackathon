import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query

from questions.engine import answer_question
from questions.registry import QUESTION_REGISTRY

app = FastAPI(
    title="UIDAI Aadhaar Analytics API",
    description="Analytics and ML-backed insights over Aadhaar enrolment and update data",
    version="1.0"
)

# --------------------------------------------------
# Load latest state_stats JSON
# --------------------------------------------------

OUTPUT_DIR = Path("outputs")


def load_latest_state_stats():
    files = sorted(
        OUTPUT_DIR.glob("state_stats_v*.json"),
        reverse=True
    )
    if not files:
        raise RuntimeError("No state_stats JSON found. Run main.py first.")

    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)


@app.on_event("startup")
def startup():
    global STATE_STATS
    STATE_STATS = load_latest_state_stats()


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "states_loaded": len(STATE_STATS)
    }


# --------------------------------------------------
# List available questions
# --------------------------------------------------

@app.get("/questions")
def list_questions():
    return {
        qid: {
            "type": q["type"],
            "description": q["description"],
            "metrics": q["metrics"]
        }
        for qid, q in QUESTION_REGISTRY.items()
    }


# --------------------------------------------------
# Answer a question
# --------------------------------------------------

@app.get("/questions/{question_id}")
def run_question(
    question_id: str,
    top_n: int = Query(5, ge=1, le=50)
):
    if question_id not in QUESTION_REGISTRY:
        raise HTTPException(status_code=404, detail="Unknown question")

    import pandas as pd
    df = pd.DataFrame(STATE_STATS)

    return answer_question(
        question_id,
        df,
        top_n=top_n
    )
