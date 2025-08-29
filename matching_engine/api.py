from fastapi import FastAPI, HTTPException
from baseline_matcher import load_data, baseline_matcher

app = FastAPI()

# Load data once
candidates, internships = load_data()


@app.get("/match/{candidate_id}")
def match_candidate(candidate_id: int):
    try:
        matches = baseline_matcher(candidate_id, candidates, internships)
        if not matches:
            raise HTTPException(status_code=404, detail="No matches found")
        return {"candidate_id": candidate_id, "matches": matches}
    except IndexError:
        raise HTTPException(status_code=404, detail="Candidate not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
