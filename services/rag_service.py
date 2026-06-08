from re import findall
from db.database import document_store




def simple_embed(text: str) -> dict[str, float]:
    """Lightweight TF-style embedding using word frequency (no external model needed)."""
    words = findall(r'\w+', text.lower())
    freq: dict[str, int] = dict()
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    total = sum(freq.values()) or 1
    return {w: c / total for w, c in freq.items()}


def cosine_sim(a: dict, b: dict) -> float:
    keys = set(a) & set(b)
    if not keys:
        return 0.0
    dot = sum(a[k] * b[k] for k in keys)
    mag_a = sum(v ** 2 for v in a.values()) ** 0.5
    mag_b = sum(v ** 2 for v in b.values()) ** 0.5
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0


def retrieve_context(session_id: str, query: str, top_k: int = 4) -> str:
    if session_id not in document_store:
        return ""
    q_vec = simple_embed(query)
    chunks_data = document_store[session_id]["chunks"]
    scored = [(cosine_sim(q_vec, c["vec"]), c["text"]) for c in chunks_data]
    scored.sort(reverse=True)
    return "\n\n".join(text for _, text in scored[:top_k])