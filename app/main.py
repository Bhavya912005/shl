from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .recommender import get_recommendations

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class Query(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/recommend")
def recommend(query: Query):
    try:
        results = get_recommendations(query.query)
        if not results:
            return {"message": "No assessments matched your query filters."}
        return results
    except Exception as e:
        return {"error": str(e)}
