import pandas as pd


def load_data():
    candidates = pd.read_csv("../data/candidates.csv")
    internships = pd.read_csv("../data/internships.csv")
    return candidates, internships


def baseline_matcher(candidate_id: int, candidates, internships):
    # Simple baseline: match by sector & location
    candidate = candidates[candidates["candidate_id"] == candidate_id].iloc[0]
    matches = internships[
        (internships["sector"] == candidate["sector_interest"])
        & (internships["location"] == candidate["location_preference"])
    ]
    return matches.to_dict(orient="records")
