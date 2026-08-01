from app.core.retrieval import RetrievedChunk

def hit_at_k(results: list[RetrievedChunk], expected_document: str) -> bool:
    return any(r.document_title == expected_document for r in results)

def reciprocal_rank(results: list[RetrievedChunk], expected_document: str) -> float:
    for position, result in enumerate(results, start=1):
        if result.document_title == expected_document:
            return 1.0 / position
    return 0.0

def fact_coverage(answer: str, required_facts: list[str]) -> float:
    if not required_facts:
        return 1.0
    lowered = answer.lower()
    found = sum(1 for fact in required_facts if fact.lower() in lowered)
    return found / len(required_facts)

def looks_like_refusal(answer: str) -> bool:
    markers = [        
        "don't have information",
        "do not contain",
        "don't contain",
        "no information",
        "not in the knowledge base",
        "cannot answer",
        "can't answer",
        "do not contain enough information",
        "not covered in the available context",
        "sources provided do not",
        ]
    lowered = answer.lower()
    return any(marker in lowered for marker in markers)

def citations_present(answer: str, num_sources: int) -> bool:
    """Did the answer cite at least one valid source number?"""
    if num_sources == 0:
        return True 
    return any(f"[{i}]" in answer for i in range(1, num_sources + 1))