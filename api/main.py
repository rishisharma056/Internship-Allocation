from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Internship Matching API")

# Load data
candidates_df = pd.read_csv("../data/candidates.csv")
internships_df = pd.read_csv("../data/internships.csv")


@app.get("/")
def root():
    return {"message": "Internship Matching API running 🚀"}


@app.get("/candidates")
def get_candidates():
    return candidates_df.to_dict(orient="records")


@app.get("/internships")
def get_internships():
    return internships_df.to_dict(orient="records")


@app.get("/match/{candidate_id}")
def match_candidate(candidate_id: int, top_n: int = 5):
    # Get candidate
    candidate = candidates_df[candidates_df["id"] == candidate_id].iloc[0]

    # Simple scoring: match sector and location
    internships_df["score"] = 0
    internships_df.loc[
        internships_df["sector"] == candidate["preferred_sector"], "score"
    ] += 1
    internships_df.loc[
        internships_df["location"] == candidate["preferred_location"], "score"
    ] += 1

    # Get top N matches
    matches = internships_df.sort_values("score", ascending=False).head(top_n)

    return {
        "candidate_id": candidate_id,
        "matches": matches[["id", "title", "sector", "location", "company"]].to_dict(
            orient="records"
        ),
    }


# To run the app, use the command:
# uvicorn api.main:app --reload
# Make sure to run this command from the root directory of the project.
# The --reload flag is useful during development as it auto-restarts the server on code changes.
# The API will be accessible at http://127.0.0.1:8000
