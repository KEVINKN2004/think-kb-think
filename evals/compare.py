import json
from pathlib import Path

METRICS = [
    "hit_rate_at_5",
    "mrr",
    "fact_coverage",
    "citation_rate",
]

def compare():
    summaries = {}
    for path in sorted(Path("evals/results").glob("*.json")):
        data = json.loads(path.read_text(encoding = "utf-8"))
        summary = data.get("summary")
        if summary and "provider" in summary:
            summaries[path.stem] = summary

    if not summaries:
        raise SystemExit("No result files found in evals/results")

    names = sorted(summaries)

    print(f"{'metric':<20}" + "".join(f"{n:>14}" for n in names))
    print("-" * (20 + 14 * len(names)))

    for metric in METRICS:
        row = f"{metric:<20}"
        for n in names:
            value = summaries[n].get(metric)
            row += f"{value if value is not None else '-':>14}"
        print(row)

    # refusals shown as a fraction
    row = f"{'correct_refusals':<20}"
    for n in names:
        s = summaries[n]
        frac = str(s.get("correct_refusals")) + "/" + str(s.get("total_unanswerable"))
        row += f"{frac:>14}"
    print(row)

    row = f"{'false_refusals':<20}"
    for n in names:
        row += f"{summaries[n].get('false_refusals'):>14}"
    print(row)

    print()
    for n in names:
        s = summaries[n]
        print(f"{n}: threshold={s.get('threshold')}  model={s.get('model')}  cases={s.get('num_cases')}")

if __name__ == "__main__":
    compare()