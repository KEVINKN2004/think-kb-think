import json

data = json.load(open("evals/results/local.json"))
for c in data["cases"]:
    if c["expected_document"] is None and not c.get("refused"):
        print(f"Q: {c['question']}")
        print(f"   sim: {c['top_similarity']}  retrieved: {c['retrieved'][:2]}")
        print(f"   A: {c['answer'][:300]}")
        print()