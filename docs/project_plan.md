# Project Plan — AI-Based Smart Allocation Engine for PM Internship Scheme (Problem ID: 25033)

> **Objective:** Build a prototype system that intelligently matches internship applicants to opportunities while respecting skills, preferences, capacity, affirmative action constraints, and fairness requirements.

---

## 1. Executive summary
A hybrid allocation system combining: (A) a machine-learned ranking model (supervised ranker) that predicts fit scores between candidate and internship, and (B) a constrained optimization layer (assignment solver) that produces final allocations subject to capacity, affirmative action, geographic/sector quotas, and previous participation rules.

The prototype deliverables:
- A working matching engine (Python) that takes candidate and internship records and returns an assignment plan.
- A lightweight front-end demonstrating the flow (React/Tailwind) — candidate profile input, bulk upload, match suggestions, manual override, and final allocation report.

---

## 2. Scope & assumptions
- **Scope:** Software prototype (no hardware). Focus on algorithm correctness, explainability, and a minimal workable UI. No production-level scaling is required for the prototype, but architecture will be designed to scale.
- **Assumptions:** A structured dataset is available (or can be synthetically generated) including candidate demographics, skills, preferences, location, qualification, prior participation flags, and internship capacities & attributes.

---

## 3. Data model (suggested fields)

### Candidate table (`candidates`)
- `candidate_id` (string)
- `name` (string)
- `age` (int)
- `gender` (enum)
- `social_category` (enum: General/OBC/SC/ST/etc.)
- `district` (string) — used to detect rural/aspirational
- `education_level` (string)
- `gpa` (float)
- `skills` (array of strings) — canonical skill tags
- `sector_interests` (array of strings)
- `location_preferences` (array of strings / radius)
- `willing_to_relocate` (bool)
- `available_dates` (date range)
- `past_participation` (bool)
- `disability_flag` (bool)
- `application_score` (float) — optional pre-score from screening

### Internship table (`internships`)
- `internship_id`
- `organization_name`
- `location` (district, city, state)
- `sector` (string)
- `required_skills` (array)
- `capacity` (int)
- `start_date`, `end_date`
- `stipend` (float)
- `affirmative_quota_profile` (optional object) — e.g., reserving seats for district/category/etc.

### Applications table (`applications`)
- `application_id`
- `candidate_id`
- `internship_id`
- `preference_rank` (int)
- `status` (submitted/withdrawn)
- `submission_time`

---

## 4. Matching approach (high-level)
1. **Feature engineering:** Build candidate–internship pair features (skill overlap, distance, preference match, qualification match, historical equity signals).
2. **Train a ranking/regression model** (XGBoost / LightGBM / CatBoost) to predict a *fit score* — trained on historical placements (if available) or simulated labels for prototype.
3. **Fairness & rule enforcement:** Encode quotas and constraints (e.g., district quotas, reserved categories, one-placement-per-candidate, capacity limits) as hard constraints.
4. **Assignment optimization:** Use an integer programming or min-cost flow solver (OR-Tools, `mip`, `PuLP`, or CVXPY) that maximizes total fit score subject to constraints. Optionally apply proportional fairness or lexicographic objectives for affirmative groups.
5. **Explainability:** For each assigned pair, show contributing features (skill overlap, distance penalty, model SHAP values) so administrators can understand decisions.

---

## 5. Constraints & fairness requirements
- **Capacity constraints** — no internship exceeds its capacity.
- **One placement per candidate** (or configurable: up to N slots).
- **Affirmative action quotas** — district-based, social-category-based, women/disabled quotas. These can be hard quotas or soft with penalties.
- **Prior participation rules** — avoid repeat winners or allow according to policy.
- **Geographic/relocation considerations** — respect candidate location preferences if possible.

Implementation choices:
- Hard quotas: modeled in the assignment solver as explicit constraints.
- Soft quotas: add penalty terms to objective when violating preferred distribution.

---

## 6. Training data & synthetic data generator
If historical labelled matches are unavailable, generate synthetic data:
- Create distributions for candidate skills, districts, and preferences.
- Simulate organizations with required skills and capacities.
- Assign ground-truth placements using a deterministic rule-based matching with noise to produce labels for supervised learning.

Include a `data_generator.py` script in the prototype to create `N` candidates and `M` internships and produce `applications.csv` and `ground_truth.csv` for model training.

---

## 7. Technical stack & libraries
- Backend: Python 3.10+
  - Data: pandas, numpy
  - ML: scikit-learn, xgboost/catboost/lightgbm
  - Solver: OR-Tools (CP-SAT), PuLP, or `mip`
  - API: FastAPI (or Flask)
- Frontend: React + Tailwind (or simple static HTML with Bootstrap for quicker prototype)
- DB (prototype): SQLite or in-memory structures; final: PostgreSQL
- Dev & infra: Docker, GitHub repo, CI (optional)

---

## 8. API endpoints (prototype)
- `POST /upload_candidates` — CSV bulk upload
- `POST /upload_internships` — CSV bulk upload
- `POST /match/run` — trigger matching process (returns assignment summary and top-k suggestions)
- `GET /match/{batch_id}/report` — download allocation report
- `POST /match/{batch_id}/override` — admin manual override of assignment
- `GET /explain/{candidate_id}/{internship_id}` — show explanation/feature contribution

---

## 9. Frontend prototype pages
- **Dashboard** — summary stats, unassigned counts, quota fulfillment
- **Upload** — candidate & internship CSV upload
- **Candidate profile** — view profile and suggested matches
- **Allocation UI** — view solver output, accept & finalize, manual overrides
- **Reports** — export assigned list, fairness audits

---

## 10. Evaluation metrics
- **Placement accuracy** — if ground truth exists: precision@k, recall@k, NDCG
- **Utilization** — fraction of internship capacity filled
- **Fairness metrics:** representation parity (difference vs target quotas), demographic parity, and constraint violations count
- **Distance / preference satisfaction** — percentage of candidates assigned to top-3 preferences

---

## 11. Milestones & timeline (prototype)
1. *M1 (Days 0–3):* Finalize data schema + build synthetic data generator.
2. *M2 (Days 4–8):* Feature engineering + train baseline scorer (rule-based & tree-based).
3. *M3 (Days 9–12):* Implement assignment solver integrating fit scores and constraints.
4. *M4 (Days 13–16):* Build minimal FastAPI backend & endpoints.
5. *M5 (Days 17–21):* Frontend prototype (React) + integration, plus explainability UI.
6. *M6 (Days 22–25):* Testing, fairness audit, documentation, final demo.

---

## 12. Example algorithms / code sketches
- **Pairwise feature ideas:** skill_jaccard, skill_missing_count, distance_km, preference_rank_penalty, gpa_gap, stipend_preference_score, prior_participation_penalty

- **Score formula (baseline):**
```
fit_score = w1*skill_jaccard - w2*distance_km + w3*(1/preference_rank) + w4*gpa_norm - w5*prior_participation_flag
```

- **Assignment (CP-SAT) objective:** maximize sum(fit_score * x[c,i]) subject to constraints, where x[c,i] in {0,1}.

---

## 13. Explainability & audit
- Use SHAP on the trained tree-model to get feature contributions per candidate–internship pair.
- Generate audit reports showing how quotas were met, who was bumped by constraints, and top contributing features to each match.

---

## 14. Deliverables (prototype)
- `matching_engine/` — Python package with data generator, feature engineering, model training, solver integration.
- `api/` — FastAPI prototype exposing endpoints.
- `frontend/` — React app demonstrating upload → match → report flow.
- `docs/` — README, architecture diagram, evaluation report.

---

## 15. Next steps (implementation plan)
1. Implement the synthetic data generator and upload sample dataset (M1).
2. Build baseline scoring function and simple rule-based matcher to validate pipeline (M2).
3. Implement CP-SAT assignment using OR-Tools and test constraints (M3).
4. Add ML scorer and integrate with solver, plus explainability (M2–M4).

---

### Appendix A — Sample DB schema (SQL)
```sql
CREATE TABLE candidates (
  candidate_id TEXT PRIMARY KEY,
  name TEXT,
  district TEXT,
  social_category TEXT,
  gpa REAL,
  skills TEXT, -- JSON array
  sector_interests TEXT,
  location_pref TEXT,
  past_participation INTEGER
);

CREATE TABLE internships (
  internship_id TEXT PRIMARY KEY,
  org_name TEXT,
  location TEXT,
  sector TEXT,
  required_skills TEXT, -- JSON array
  capacity INTEGER,
  affirmative_profile TEXT -- JSON
);
```


---

*Document created for collaborative development. Use this as the project single source-of-truth for the prototype implementation and UI sketches.*

