from typing import List
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load and preprocess catalog
catalog_df = pd.read_csv("data/shl_assessment_catalog.csv")
catalog_df["duration_minutes"] = pd.to_numeric(catalog_df["duration_minutes"], errors="coerce")
catalog_df["type"] = catalog_df["type"].str.lower()
catalog_df["remote_support"] = catalog_df["remote_support"].str.lower()
catalog_df["adaptive_support"] = catalog_df["adaptive_support"].str.lower()

# Precompute text for embeddings
catalog_texts = (catalog_df["name"] + " " + catalog_df["type"]).fillna("").tolist()
catalog_embeddings = model.encode(catalog_texts, convert_to_tensor=True)

# ------------------ Helper Functions ------------------

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

# ------------------ Recommendation Logic ------------------

def get_recommendations(query: str, top_k: int = 10) -> List[dict]:
    # Step 1: Extract info from query
    max_duration = extract_duration(query)
    type_filters = extract_type_keywords(query)
    flags = extract_flags(query)

    # Step 2: Start with full catalog
    filtered_df = catalog_df.copy()

    # Step 3: Apply duration filter if mentioned
    if max_duration:
        filtered_df = filtered_df[filtered_df["duration_minutes"] <= max_duration]

    # Step 4: Apply test type filter — fuzzy match
    if type_filters:
        filtered_df = filtered_df[filtered_df["type"].apply(
            lambda t: any(req in t for req in type_filters)
        )]

    # Step 5: Apply remote/adaptive support if mentioned
    if flags["remote"]:
        filtered_df = filtered_df[filtered_df["remote_support"].str.lower() == "yes"]

    if flags["adaptive"]:
        filtered_df = filtered_df[filtered_df["adaptive_support"].str.lower() == "yes"]

    # Step 6: Fallback to full catalog if filtered out everything
    if filtered_df.empty:
        filtered_df = catalog_df.copy()

    # Step 7: Compute similarity on filtered items
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
