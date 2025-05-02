import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.recommender import get_recommendations
from app.evaluator import mean_recall_and_map

# Benchmark queries and their expected relevant assessments (ground truth sets)
benchmark_queries = [
    "Looking for a technical test under 30 minutes",
    "I need to assess personality traits remotely",
    "Looking for a sales assessment with adaptive support"
]

ground_truth_sets = [
    {"Java 8 (New)", "HTML5 (New)"},
    {"Motivation Questionnaire MQM5"},
    {"Sales Representative Solution"}
]

# Run recommendations
all_predictions = []
for query in benchmark_queries:
    results = get_recommendations(query, top_k=5)
    predicted_names = [item["name"] for item in results]
    all_predictions.append(predicted_names)

# Evaluate
metrics = mean_recall_and_map(all_predictions, ground_truth_sets, k=3)
print("📊 Evaluation Results:")
print(metrics)
