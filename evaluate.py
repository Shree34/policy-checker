import json
from ai_agent import ask_insurance_question  # make sure this is your main function

def load_eval(file="eval_data.jsonl"):
    with open(file, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def exact_match(a, b, keys):
    return all(a.get(k) == b.get(k) for k in keys)

def main():
    data = load_eval()
    total = len(data)
    correct = 0
    for row in data:
        pred = ask_insurance_question(row["context"], row["question"])
        is_correct = exact_match(pred, row["expected"], ["decision"])  # you can also compare justification if needed
        print("✅" if is_correct else "❌", row["question"], "→", pred.get("decision"))
        if is_correct:
            correct += 1
    print(f"\n🧮 Accuracy: {correct}/{total} = {correct/total:.2%}")

if __name__ == "__main__":
    main()
