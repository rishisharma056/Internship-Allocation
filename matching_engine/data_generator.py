import random
import uuid
import pandas as pd

# ----- Configurable parameters -----
N_CANDIDATES = 50
N_INTERNSHIPS = 10
MAX_APPS_PER_CANDIDATE = 3

SKILLS = [
    "Python",
    "Java",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "Web Dev",
    "C++",
    "Cloud",
    "AI",
    "Networking",
]
SECTORS = ["IT", "Finance", "Healthcare", "Education", "Energy"]
DISTRICTS = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Chennai",
    "Kolkata",
    "Lucknow",
    "Patna",
    "Jaipur",
]
SOCIAL_CATS = ["General", "OBC", "SC", "ST"]


# ----- Generate candidates -----
def generate_candidates(n=N_CANDIDATES):
    rows = []
    for _ in range(n):
        cid = str(uuid.uuid4())[:8]
        rows.append(
            {
                "candidate_id": cid,
                "name": f"Candidate_{cid}",
                "age": random.randint(18, 25),
                "gender": random.choice(["Male", "Female"]),
                "social_category": random.choice(SOCIAL_CATS),
                "district": random.choice(DISTRICTS),
                "education_level": random.choice(["Bachelors", "Masters", "Diploma"]),
                "gpa": round(random.uniform(6.0, 9.9), 2),
                "skills": ",".join(random.sample(SKILLS, k=random.randint(2, 5))),
                "sector_interests": ",".join(
                    random.sample(SECTORS, k=random.randint(1, 2))
                ),
                "location_preferences": random.choice(DISTRICTS),
                "willing_to_relocate": random.choice([0, 1]),
                "past_participation": random.choice([0, 1]),
            }
        )
    return pd.DataFrame(rows)


# ----- Generate internships -----
def generate_internships(n=N_INTERNSHIPS):
    rows = []
    for i in range(n):
        iid = str(uuid.uuid4())[:8]
        rows.append(
            {
                "internship_id": iid,
                "organization_name": f"Org_{i}",
                "location": random.choice(DISTRICTS),
                "sector": random.choice(SECTORS),
                "required_skills": ",".join(
                    random.sample(SKILLS, k=random.randint(2, 4))
                ),
                "capacity": random.randint(3, 10),
            }
        )
    return pd.DataFrame(rows)


# ----- Generate applications -----
def generate_applications(candidates, internships):
    rows = []
    for _, c in candidates.iterrows():
        applied = random.sample(
            list(internships["internship_id"]),
            k=random.randint(1, MAX_APPS_PER_CANDIDATE),
        )
        rank = 1
        for iid in applied:
            rows.append(
                {
                    "application_id": str(uuid.uuid4())[:8],
                    "candidate_id": c["candidate_id"],
                    "internship_id": iid,
                    "preference_rank": rank,
                }
            )
            rank += 1
    return pd.DataFrame(rows)


if __name__ == "__main__":
    candidates = generate_candidates()
    internships = generate_internships()
    applications = generate_applications(candidates, internships)

    candidates.to_csv("candidates.csv", index=False)
    internships.to_csv("internships.csv", index=False)
    applications.to_csv("applications.csv", index=False)
    print("Generated candidates.csv, internships.csv, applications.csv")
