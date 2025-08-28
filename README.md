# AI-Based Smart Allocation Engine for PM Internship Scheme

Prototype system for Problem Statement **25033** (Ministry of Corporate Affairs).

## 🚀 Overview
This project builds an AI/ML-powered smart allocation engine to match students with internship opportunities. The system accounts for:
- Skills, qualifications, and preferences
- Sector and location alignment
- Industry capacity constraints
- Affirmative action quotas (districts, social categories, etc.)
- Fairness & explainability

The prototype includes:
- **Matching Engine (Python)** — ML model + optimization solver
- **Backend API (FastAPI)** — to expose matching service
- **Frontend (React + Vite + Tailwind)** — demo interface for uploading data and viewing allocations
- **Synthetic Data Generator** — to simulate candidates, internships, and applications

---

## 📂 Project Structure
```
pm_internship_allocation/
├── data/               # datasets (CSV)
├── matching_engine/    # ML + solver logic
├── api/                # FastAPI backend
├── frontend/           # React + Vite frontend
├── notebooks/          # Jupyter experiments
├── docs/               # project documentation
├── tests/              # unit tests
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # optional combined setup
├── Dockerfile          # backend container
└── README.md           # this file
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/pm_internship_allocation.git
cd pm_internship_allocation
```

### 2. Backend (Python + FastAPI)
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Run the API:
```bash
uvicorn api.main:app --reload
```
API will be live at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 3. Frontend (React + Vite + Tailwind)
```bash
cd frontend
npm install
npm run dev
```
Frontend will be live at: [http://localhost:5173](http://localhost:5173)

### 4. Generate Synthetic Data
```bash
python matching_engine/data_generator.py
```
This will create `candidates.csv`, `internships.csv`, and `applications.csv` inside the `data/` folder.

---

## 🧩 Roadmap
- [x] Synthetic data generator
- [ ] Baseline matching engine (rule-based + OR-Tools solver)
- [ ] ML-based scoring model
- [ ] Backend API endpoints
- [ ] Frontend demo (upload, match, reports)
- [ ] Explainability (SHAP values)
- [ ] Fairness audits

---

## 🛠 Tech Stack
- **Backend:** Python, FastAPI, OR-Tools, scikit-learn
- **Frontend:** React, Vite, TailwindCSS
- **Data/ML:** pandas, numpy, xgboost/lightgbm
- **Infra:** Docker, GitHub Actions (planned)

---

## 🤝 Contribution
1. Fork the repo
2. Create a branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push branch: `git push origin feature-name`
5. Open a Pull Request

---

## 📜 License
MIT License — free to use and modify.

