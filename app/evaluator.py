def recall_at_k(predicted: list, relevant: set, k: int) -> float:
    """
    Calculate Recall@K.
    """
    top_k = predicted[:k]
    hits = sum(1 for item in top_k if item in relevant)
    return hits / len(relevant) if relevant else 0.0

def average_precision_at_k(predicted: list, relevant: set, k: int) -> float:
    """
    Calculate Average Precision@K.
    """
    score = 0.0
    hits = 0
    for i, item in enumerate(predicted[:k], 1):
        if item in relevant:
            hits += 1
            score += hits / i
    return score / min(len(relevant), k) if relevant else 0.0

def mean_recall_and_map(predictions: list[list], relevant_sets: list[set], k: int = 3) -> dict:
    """
    Calculate Mean Recall@K and MAP@K across all queries.
    """
    recalls = []
    maps = []
    for pred, rel in zip(predictions, relevant_sets):
        recalls.append(recall_at_k(pred, rel, k))
        maps.append(average_precision_at_k(pred, rel, k))
    return {
        "Mean Recall@K": round(sum(recalls) / len(recalls), 4),
        "MAP@K": round(sum(maps) / len(maps), 4)
    }
