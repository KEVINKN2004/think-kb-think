import json
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings
from app.core.embeddings import get_provider
from app.core.generation import generate_answer
from app.core.retrieval import retrieve
from app.db.session import SessionLocal
from evals.dataset import CASES
from evals.metrics import (
    citations_present,
    fact_coverage,
    hit_at_k,
    looks_like_refusal,
    reciprocal_rank,
)

TOP_K = 5

def run(skip_generation: bool = False):
    provider = get_provider()
    db = SessionLocal()
    rows = []

    try:
        for case in CASES:
            results = retrieve(
                db, case.question, provider,
                top_k = TOP_K,
                min_similarity = settings.min_similarity_threshold,
            )

            row = {
                "question": case.question,
                "expected_document": case.expected_document,
                "retrieved": [r.document_title for r in results],
                "top_similarity": round(results[0].similarity, 3) if results else None,
            }

            if case.expected_document:
                row["hit"] = hit_at_k(results, case.expected_document)
                row["rr"] = round(reciprocal_rank(results, case.expected_document), 3)

            if not skip_generation:
                generated = generate_answer(case.question, results)
                row["answer"] = generated.answer
                row["refused"] = looks_like_refusal(generated.answer)
                row["refusal_correct"] = row["refused"] != case.should_answer
                row["cited"] = citations_present(generated.answer, len(generated.sources))
                if case.should_answer:
                    row["fact_coverage"] = round(
                        fact_coverage(generated.answer, case.required_facts), 3
                    )

            rows.append(row)
            if case.expected_document:
                verdict = "PASS" if row["hit"] else "MISS"
            else:
                verdict = f"UNANS sim = {row['top_similarity']}"
            print(f"{verdict}  {case.question[:60]}")

    finally:
        db.close()

    summary = summarize(rows, provider.name)
    write_report(rows, summary, provider.name)
    print_summary(summary)
    return summary

def summarize(rows: list[dict], provider_name: str) -> dict:
    answerable = [r for r in rows if r["expected_document"]]
    unanswerable = [r for r in rows if not r["expected_document"]]

    def mean(values):
        values = [v for v in values if v is not None]
        return round(sum(values) / len(values), 3) if values else None

    return {
        "provider": provider_name,
        "model": settings.generation_model,
        "threshold": settings.min_similarity_threshold,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "num_cases": len(rows),
        "hit_rate_at_5": mean([r.get("hit") and 1.0 or 0.0 for r in answerable]),
        "mrr": mean([r.get("rr") for r in answerable]),
        "fact_coverage": mean([r.get("fact_coverage") for r in answerable]),
        "citation_rate": mean([1.0 if r.get("cited") else 0.0 for r in answerable]),
        "correct_refusals": sum(1 for r in unanswerable if r.get("refused")),
        "total_unanswerable": len(unanswerable),
        "false_refusals": sum(1 for r in answerable if r.get("refused")),
    }

def write_report(rows, summary, provider_name):
    out = Path(f"evals/results/{provider_name}.json")
    out.parent.mkdir(parents=True, exist_ok = True)
    out.write_text(json.dumps({"summary": summary, "cases": rows}, indent=2), encoding = "utf-8")
    print(f"\nWrote {out}")

def print_summary(s: dict):
    print(f"\n--- {s['provider']} ---")
    print(f"Hit rate @5:      {s['hit_rate_at_5']}")
    print(f"MRR:              {s['mrr']}")
    print(f"Fact coverage:    {s['fact_coverage']}")
    print(f"Citation rate:    {s['citation_rate']}")
    print(f"Correct refusals: {s['correct_refusals']}/{s['total_unanswerable']}")
    print(f"False refusals:   {s['false_refusals']}")

if __name__ == "__main__":
    import sys
    run(skip_generation = "--skip-generation" in sys.argv)