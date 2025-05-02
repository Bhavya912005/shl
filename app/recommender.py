from typing import List
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


catalog_df = pd.read_csv("data/shl_assessment_catalog.csv")
catalog_df["duration_minutes"] = pd.to_numeric(catalog_df["duration_minutes"], errors="coerce")
catalog_df["type"] = catalog_df["type"].str.lower()
catalog_df["remote_support"] = catalog_df["remote_support"].str.lower()
catalog_df["adaptive_support"] = catalog_df["adaptive_support"].str.lower()


catalog_texts = (catalog_df["name"] + " " + catalog_df["type"]).fillna("").tolist()
catalog_embeddings = model.encode(catalog_texts, convert_to_tensor=True)



def extract_duration(query: str) -> int | None:
    match = re.search(r"(?:under|within|less than)?\s*(\d{1,3})\s*min", query.lower())
    return int(match.group(1)) if match else None

def extract_type_keywords(query: str) -> List[str]:
    known_types = ["technical", "cognitive", "personality", "sales", "communication", "marketing", "administration"]
    query_lower = query.lower()
    return [t for t in known_types if t in query_lower]

def extract_flags(query: str) -> dict:
    q = query.lower()
    return {
        "remote": "remote" in q,
        "adaptive": "adaptive" in q or "irt" in q
    }



def get_recommendations(query: str, top_k: int = 10) -> List[dict]:
    
    max_duration = extract_duration(query)
    type_filters = extract_type_keywords(query)
    flags = extract_flags(query)

    
    filtered_df = catalog_df.copy()

    
    if max_duration:
        filtered_df = filtered_df[filtered_df["duration_minutes"] <= max_duration]

    
    if type_filters:
        filtered_df = filtered_df[filtered_df["type"].apply(
            lambda t: any(req in t for req in type_filters)
        )]

    
    if flags["remote"]:
        filtered_df = filtered_df[filtered_df["remote_support"].str.lower() == "yes"]

    if flags["adaptive"]:
        filtered_df = filtered_df[filtered_df["adaptive_support"].str.lower() == "yes"]

    
    if filtered_df.empty:
        filtered_df = catalog_df.copy()

    
    filtered_texts = (filtered_df["name"] + " " + filtered_df["type"]).fillna("").tolist()
    filtered_embeddings = model.encode(filtered_texts, convert_to_tensor=True)
    query_embedding = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding, filtered_embeddings)[0]
    top_k_indices = similarities.argsort()[-top_k:][::-1]

    results = []
    for idx in top_k_indices:
        item = filtered_df.iloc[idx]
        results.append({
            "name": item["name"],
            "url": item["url"],
            "remote_support": item["remote_support"].capitalize(),
            "adaptive_support": item["adaptive_support"].capitalize(),
            "duration_minutes": int(item["duration_minutes"]),
            "type": item["type"].capitalize()
        })

    return results
