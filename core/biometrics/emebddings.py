import numpy as np


def verify_embedding_match(embeddingA, embeddingB, threshold=0.85):
    assert len(embeddingA) == len(embeddingB)

    dist = np.linalg.norm(np.array(embeddingA) - np.array(embeddingB))

    results = {
        "metric": "euclidean",
        "distance": dist,
        "threshold": threshold
    }

    # check if match occurs
    if dist > threshold:
        results["match"] = False
    else:
        results["match"] = True

    return results
