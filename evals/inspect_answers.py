import json
from pathlib import Path

data = json.loads(Path("evals/results/local.json").read_text(encoding = "utf-8"))
for c in data["cases"]:
    if c["expected_document"] is None and not c.get("refused"):
        print(f"Q: {c['question']}")
        print(f"   sim: {c['top_similarity']}  retrieved: {c['retrieved'][:2]}")
        print(f"   A: {c['answer'][:300]}")
        print()