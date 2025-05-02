

# 🔍 SHL Assessment Recommendation System

This project implements a semantic search–based recommendation engine that suggests the most relevant SHL assessments given a job description or natural language query. Built using FastAPI, sentence-transformers, and Streamlit, it enables hiring managers to efficiently identify suitable assessments from SHL’s product catalog.

---

## 🛠️ Tech Stack

* 🐍 Python 3.11
* ⚙️ FastAPI – for API development
* 🤖 Sentence Transformers (MiniLM-L6-v2) – for semantic similarity
* 📊 Scikit-learn – for cosine similarity
* 🧮 Pandas – for data processing
* 🌐 Streamlit – for frontend UI
* 🚀 Render – for backend deployment

---

## 📁 Dataset

The SHL product catalog is stored in a structured CSV file with the following columns:

* `name`: Assessment name
* `url`: SHL product page
* `duration_minutes`: Duration in minutes
* `type`: Test type (Technical, Cognitive, Personality, etc.)
* `remote_support`: Yes/No
* `adaptive_support`: Yes/No

Example:

| name         | type      | duration\_minutes | remote\_support | adaptive\_support |
| ------------ | --------- | ----------------- | --------------- | ----------------- |
| Java 8 (New) | Technical | 40                | Yes             | Yes               |

---

## 📐 System Architecture

```text
[ Query Input ]
       ↓
[ Extract filters ]
       ↓
[ Filter catalog (duration, type, remote/adaptive) ]
       ↓
[ Compute embeddings ]
       ↓
[ Rank with cosine similarity ]
       ↓
[ Return top 1–10 recommendations ]
```

---

## 🚀 Deployment

✅ Hosted API on Render:

* Base URL: [https://oa-recommendation.onrender.com](https://oa-recommendation.onrender.com)
* Swagger UI: [https://oa-recommendation.onrender.com/docs](https://oa-recommendation.onrender.com/docs)
* Health check: [https://oa-recommendation.onrender.com/health](https://oa-recommendation.onrender.com/health)

Run locally:


uvicorn app.main:app --reload


Example request:


POST /recommend
{
  "query": "Looking for a cognitive and personality test within 40 minutes that supports remote testing"
}


---

## 💻 Streamlit UI

Run locally:


streamlit run streamlit_app.py


Deployed via Streamlit Cloud :
[https://bhavya912005-shl-streamlit-app-yrguko.streamlit.app/](https://bhavya912005-shl-streamlit-app-yrguko.streamlit.app/)

---

## 🧪 Evaluation

Implemented metrics:

* 📌 Mean Recall\@3
* 📌 MAP\@3 (Mean Average Precision)

Code: `app/evaluator.py`
Evaluation script: `test/test_metrics.py`

Example scores (3 queries):


{
  "Mean Recall@3": 0.67,
  "MAP@3": 0.61
}


---

## 🧠 Example Output


[
  {
    "name": "HTML5 (New)",
    "type": "Technical",
    "duration_minutes": 35,
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "url": "https://www.shl.com/solutions/products/product-catalog/view/html5-new/"
  },
  ...
]


---

## 📂 Project Structure

```text
shl-recommender/
├── app/
│   ├── main.py           # FastAPI endpoints
│   ├── recommender.py    # Recommendation logic
│   └── evaluator.py      # Evaluation metrics
├── test/
│   └── test_metrics.py   # MAP@K, Recall@K testing
├── data/
│   └── shl_assessment_catalog.csv
├── streamlit_app.py      # Streamlit UI
├── requirements.txt
└── README.md
```

---

## 📈 Optimizations

* 🔍 Duration, type, and feature filtering before ranking
* 🧠 Substring matching for test types (e.g. "cognitive" matches "cognitive reasoning")
* 🛡️ Filter fallback if result set is empty
* ✅ CORS and error handling for stability

---








