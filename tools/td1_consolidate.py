"""TD 1 consolidation: merge the operators' raw traces, build the comparison CSV and its pivot.

Usage (from the repository root, after the model batches):
    python3 tools/td1_consolidate.py

Reads   traces-A.csv ... traces-E.csv (any traces-*.csv except traces-td1.csv / traces-demo.csv)
        state-*.jsonl (the --state files of each operator)
Writes  traces-td1.csv              every attempt of every operator, one header, + column source_file
        traces-td1.jsonl            the state files concatenated, + field source_file
        model-question-comparison-en.csv   one final row per model x question (last attempt)
        results/pivot-td1.md        models x questions view of the comparison CSV, for the plenary
        results/families-td1.md     correct / evaluated per model and question family, for the summary

Raw files are only read, never modified. Missing cells of the 5 x 20 batch are written as
`not_executed` with a TODO reason. Explanations of non-correct cells are pre-filled with the
evidence (verdict_detail, error, HTTP status) and a TODO for the cause, which a member must write
after reading the SQL: the cause is a human reading of the trace, not something this script guesses.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"traces-td1.csv", "traces-demo.csv"}
STATUS_SHORT = {"correct": "OK", "incorrect": "WRONG", "sql_invalid": "SQL-INV", "sql_rejected": "SQL-REJ",
                "access_error": "ACCESS", "not_executed": "NOT-RUN", "": "NO-REF"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def merge_traces():
    rows, header = [], None
    for path in sorted(ROOT.glob("traces-*.csv")):
        if path.name in SKIP:
            continue
        part = read_csv(path)
        if part and header is None:
            header = list(part[0].keys())
        for r in part:
            r["source_file"] = path.name
        rows += part
        print(f"  {path.name}: {len(part)} attempt(s)")
    if not rows:
        raise SystemExit("no traces-*.csv found: run the model batches first")
    with open(ROOT / "traces-td1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header + ["source_file"])
        w.writeheader()
        w.writerows(rows)

    jsonl = 0
    with open(ROOT / "traces-td1.jsonl", "w", encoding="utf-8") as out:
        for path in sorted(ROOT.glob("state-*.jsonl")):
            for line in open(path, encoding="utf-8"):
                if line.strip():
                    rec = json.loads(line)
                    rec["source_file"] = path.name
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    jsonl += 1
    print(f"traces-td1.csv: {len(rows)} attempt(s); traces-td1.jsonl: {jsonl} line(s)")
    return rows


def attempt_key(r):
    try:
        n = int(r.get("attempts") or 0)
    except ValueError:
        n = 0
    return (n, r.get("date_utc", ""))


def build_comparison(rows):
    config = json.load(open(ROOT / "modeles-autorises.json", encoding="utf-8"))
    models = [f"{m['gate']}:{m['identifiant_exact']}" for m in config["modeles"] if not m.get("optionnel")]
    questions = json.load(open(ROOT / "questions-td1.json", encoding="utf-8"))["questions"]
    refs = {r["case_id"]: r["revenue_cents"] for r in read_csv(ROOT / "reference-td1.csv")}

    last = {}
    for r in rows:
        if r.get("nature") == "simulation":
            continue
        model = f"{r['provider']}:{r['model_requested']}"
        if model not in models:
            models.append(model)            # documented replacement model
        key = (model, r["case_id"])
        if key not in last or attempt_key(r) >= attempt_key(last[key]):
            last[key] = r

    out = []
    for model in models:
        for q in questions:
            r = last.get((model, q["id"]))
            if r is None:
                out.append(dict(case_id=q["id"], model_id=model, trace_file="", cell_id=f"{model}:{q['id']}",
                                nature="", status="not_executed", value_cents="",
                                reference_cents=refs.get(q["id"], ""),
                                explanation="TODO reason: cell not run (quota, time, access?)"))
                continue
            status = r.get("verdict", "")
            evidence = "; ".join(x for x in [r.get("verdict_detail"), r.get("error"),
                                             f"HTTP {r['http_status']}" if r.get("http_status") not in ("", "200") else ""] if x)
            expl = f"last attempt {r.get('attempts')}"
            if status != "correct":
                expl = f"TODO cause read from the SQL/error; evidence: {evidence or 'see sql'}; {expl}"
            out.append(dict(case_id=q["id"], model_id=model, trace_file=r["source_file"], cell_id=r["cell_id"],
                            nature=r.get("nature", ""), status=status, value_cents=r.get("value", ""),
                            reference_cents=r.get("reference", "") or refs.get(q["id"], ""), explanation=expl))

    path = ROOT / "model-question-comparison-en.csv"
    if path.exists() and any("TODO" not in row.get("explanation", "") and row.get("explanation")
                             for row in read_csv(path) if row.get("status") != "correct"):
        path = ROOT / "results" / "model-question-comparison-en.generated.csv"
        print(f"explanations already written in model-question-comparison-en.csv: new version saved to {path.name}")
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"{path.relative_to(ROOT)}: {len(out)} row(s)")
    return out, models, questions


def write_views(out, models, questions):
    (ROOT / "results").mkdir(exist_ok=True)
    cell = {(r["model_id"], r["case_id"]): r for r in out}
    ids = [q["id"] for q in questions]
    lines = ["# TD 1 — models x questions (pivot of model-question-comparison-en.csv)", "",
             "Generated by `tools/td1_consolidate.py`. " + ", ".join(f"`{v}` = {k or 'no reference'}" for k, v in STATUS_SHORT.items()), "",
             "| model | " + " | ".join(ids) + " | correct |", "|---|" + "---|" * (len(ids) + 1)]
    for m in models:
        st = [cell[(m, i)]["status"] for i in ids]
        lines.append(f"| {m} | " + " | ".join(STATUS_SHORT.get(s, s) for s in st) + f" | {st.count('correct')}/{len(ids)} |")
    (ROOT / "results" / "pivot-td1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fam = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))   # model -> family -> [correct, evaluated, access/not run]
    for q in questions:
        parts = [p.strip() for p in q["type"].split("+")]
        families = ["combined"] + parts if len(parts) > 1 else parts
        for m in models:
            r = cell[(m, q["id"])]
            for f in families:
                key = "age" if f.startswith("age") else ("product" if f.startswith("product") else f)
                c = fam[m][key]
                if r["status"] in ("access_error", "not_executed"):
                    c[2] += 1
                else:
                    c[1] += 1
                    c[0] += r["status"] == "correct"
    lines = ["# TD 1 — results by question family (for five-model-summary-en.csv)", "",
             "correct/evaluated, then access failures or unfinished cells. Combined questions also count in each of their families (overlap).", "",
             "| model | period | age | product | combined |", "|---|---|---|---|---|"]
    for m in models:
        lines.append(f"| {m} | " + " | ".join(f"{fam[m][k][0]}/{fam[m][k][1]} (+{fam[m][k][2]} not evaluated)"
                                             for k in ("period", "age", "product", "combined")) + " |")
    (ROOT / "results" / "families-td1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print((ROOT / "results" / "pivot-td1.md").read_text())


if __name__ == "__main__":
    rows = merge_traces()
    write_views(*build_comparison(rows))
