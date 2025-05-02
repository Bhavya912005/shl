# SHL Assessment Recommendation Engine

This is a simple FastAPI-based recommendation system that suggests relevant SHL assessments based on a job description or natural language query.

---

## 🔧 Tech Stack
- **Python 3.8+**
- **FastAPI** – for building APIs
- **Sentence-Transformers** – for text embeddings (semantic matching)
- **scikit-learn** – for cosine similarity
- **pandas** – for loading and processing the catalog
- **uvicorn** – for running FastAPI server

---

## Folder Structure
shl_recommender/
├── app/
│ ├── main.py # FastAPI server (API endpoints)
│ └── recommender.py # Core logic to process and recommend
├── data/
│ └── shl_assessment_catalog.csv
├── requirements.txt
└── README.md

---

## How to Run the API Locally

### Step 1: Clone the repo or create a new folder

### Step 2: Create virtual environment

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
### Step 3: Install dependencies
pip install -r requirements.txt
### Step 4: Run the FastAPI server
uvicorn app.main:app --reload
### Step 5: Test API locally
Health check: http://127.0.0.1:8000/health

Swagger Docs: http://127.0.0.1:8000/docs


API Endpoints
GET /health
Check if the API is running

Response:

json
Copy
Edit
{ "status": "OK" }
POST /recommend
Takes a job description or natural language query and returns 1–10 relevant SHL assessments.

Input:

json
Copy
Edit
{
  "query": "I'm hiring for Python developers with strong analytical skills"
}
Output:

json
Copy
Edit
[
  {
    "name": "Core Java (Entry Level) (New)",
    "url": "https://...",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration_minutes": 30,
    "type": "Technical"
  },
  ...
]
📬 How It Works
Catalog is loaded from a CSV file (data/shl_assessment_catalog.csv)

Each entry is embedded using sentence-transformers

The user query is embedded and matched to catalog items via cosine similarity

Top matches are returned as JSON




