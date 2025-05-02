import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load catalog
catalog_df = pd.read_csv('data/shl_assessment_catalog.csv')

# Precompute catalog text embeddings
catalog_texts = catalog_df['name'] + ' ' + catalog_df['type']
catalog_embeddings = model.encode(catalog_texts.tolist(), convert_to_tensor=True)

# Core recommendation logic
def get_recommendations(query, top_k=10):
    query_embedding = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding, catalog_embeddings)[0]
    top_k_indices = similarities.argsort()[-top_k:][::-1]

    results = []
    for idx in top_k_indices:
        item = catalog_df.iloc[idx]
        results.append({
            "name": item["name"],
            "url": item["url"],
            "remote_support": item["remote_support"],
            "adaptive_support": item["adaptive_support"],
            "duration_minutes": int(item["duration_minutes"]),
            "type": item["type"]
        })

    return results

# Evaluation: Recall@K
def recall_at_k(recommended, relevant, k=3):
    recommended_at_k = recommended[:k]
    hits = len([item for item in recommended_at_k if item in relevant])
    return hits / len(relevant) if relevant else 0.0

# Evaluation: MAP@K
def average_precision_at_k(recommended, relevant, k=3):
    score = 0.0
    hits = 0
    for i in range(min(k, len(recommended))):
        if recommended[i] in relevant:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(relevant), k) if relevant else 0.0

# Evaluate a single query
def evaluate_query(query, relevant_assessment_names, k=3):
    results = get_recommendations(query, top_k=k)
    recommended_names = [item['name'] for item in results]

    recall = recall_at_k(recommended_names, relevant_assessment_names, k)
    map_k = average_precision_at_k(recommended_names, relevant_assessment_names, k)

    return {
        f"Recall@{k}": round(recall, 3),
        f"MAP@{k}": round(map_k, 3),
        "Recommended": recommended_names
    }

# Quick test
if __name__ == "__main__":
    query = "Looking for a Java developer with strong problem-solving and communication"
    relevant = ["Java 8 (New)", "Core Java (Entry Level) (New)"]
    
    print("\n🔎 Recommendations:")
    for rec in get_recommendations(query, top_k=5):
        print(f"- {rec['name']} ({rec['type']}) — {rec['duration_minutes']} mins")

    print("\n📊 Evaluation:")
    print(evaluate_query(query, relevant, k=3))
