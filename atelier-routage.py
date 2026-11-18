#!/usr/bin/env python3
"""TD 2 and TD 3: read the decisions of a routing rule, then adapt it to your own.

Adapted by sub-group 1 to its TD 2 routing rule (td2/C-routing/routing-rule.md). No API call, no key.

Resources are the five TD 1 models and the paid route of gpt-oss-120b. A resource is eligible for a
question family only if its model was correct on every TD 1 cell of that family
(model-question-comparison-en.csv). The paid cost is the portfolio price of 2026-09-29 applied to the
median TD 1 tokens of gpt-oss-120b. Quota availability is supplied as a scenario, not measured.
"""
import argparse
import csv
import json
from pathlib import Path

TD1_TABLE = Path(__file__).with_name("model-question-comparison-en.csv")

FAMILIES = {
    "F1": ["C01", "C04", "C05", "C06", "C07", "C20"],
    "F3": ["C03", "C12", "C13", "C14"],
    "F2": ["C02", "C08", "C09", "C11", "C15", "C16", "C17", "C19"],
    "F2b": ["C10", "C18"],
}

PREFERENCE = [
    "groq:openai/gpt-oss-20b",
    "openrouter:cohere/north-mini-code:free",
    "openrouter:dots-studio/dots-3-note-preview:free",
    "groq:openai/gpt-oss-120b",
    "groq:qwen/qwen3.8-27b",
]

RESOURCES = [
    {"id": "groq:openai/gpt-oss-20b", "model": "groq:openai/gpt-oss-20b", "access": "free",
     "available": True, "cash": 0.0, "allocation": 0.0, "reset_minutes": None},
    {"id": "openrouter:cohere/north-mini-code:free", "model": "openrouter:cohere/north-mini-code:free", "access": "free",
     "available": True, "cash": 0.0, "allocation": 0.0, "reset_minutes": None},
    {"id": "openrouter:dots-studio/dots-3-note-preview:free", "model": "openrouter:dots-studio/dots-3-note-preview:free", "access": "free",
     "available": True, "cash": 0.0, "allocation": 0.0, "reset_minutes": None},
    {"id": "groq:openai/gpt-oss-120b", "model": "groq:openai/gpt-oss-120b", "access": "free",
     "available": True, "cash": 0.0, "allocation": 0.0, "reset_minutes": None},
    {"id": "groq:qwen/qwen3.8-27b", "model": "groq:qwen/qwen3.8-27b", "access": "free",
     "available": True, "cash": 0.0, "allocation": 0.0, "reset_minutes": None},
    {"id": "openrouter:openai/gpt-oss-120b (paid)", "model": "groq:openai/gpt-oss-120b", "access": "tokens",
     "available": True, "cash": 0.00021, "allocation": 0.00021, "reset_minutes": None},
]


def td1_rates():
    with TD1_TABLE.open(encoding="utf-8", newline="") as f:
        status = {(r["model_id"], r["case_id"]): r["status"] for r in csv.DictReader(f)}
    rates = {}
    for family, cells in FAMILIES.items():
        for model in PREFERENCE:
            failed = [c for c in cells if status[(model, c)] != "correct"]
            rates[(family, model)] = (len(cells) - len(failed), len(cells), failed)
    return rates


def checks_for(use, family):
    if use == "payout":
        return "reference query check and human review"
    if use == "customer":
        return "3-of-5 quorum, abstention sent to human review" if family in ("F2", "F2b") else "2-of-3 quorum"
    return "none"


def evidence(rates, family, resource):
    ok, total, _ = rates[(family, resource["model"])]
    return f"{resource['model']} correct {ok}/{total} on {family} in TD 1 ({', '.join(FAMILIES[family])})"


def choose(request, resources):
    """Same priority order as the supplied rule: included capacity, then deferral, then paid route, then abstention.

    Eligibility: the model was correct on every TD 1 cell of the family. Among eligible free routes, the
    order of PREFERENCE keeps gpt-oss-120b for the age families, where it is the only model at 100 %.
    """
    family = request["family"]
    if family not in FAMILIES:
        return {"action": "abstain", "resource": None, "cash": 0, "checks": None,
                "reason": f"family {family} has no TD 1 cell: no evidence for any model"}
    rates = td1_rates()
    eligible = [r for r in resources if rates[(family, r["model"])][0] == rates[(family, r["model"])][1]]
    eligible.sort(key=lambda r: (r["cash"], PREFERENCE.index(r["model"])))
    checks = checks_for(request["use"], family)

    included = [r for r in eligible if r["available"] and r["cash"] == 0]
    if included:
        chosen = included[0]
        reason = evidence(rates, family, chosen)
        if chosen is not eligible[0]:
            reason = f"preferred {eligible[0]['id']} unavailable; next eligible route: " + reason
        return {"action": "run", "resource": chosen["id"], "cash": 0, "checks": checks, "reason": reason}
    waiting = [r for r in eligible if not r["available"] and r["cash"] == 0
               and r["reset_minutes"] is not None
               and 0 < r["reset_minutes"] <= request["deadline_minutes"]]
    if waiting and request["can_wait"]:
        chosen = min(waiting, key=lambda r: r["reset_minutes"])
        return {"action": "defer", "resource": chosen["id"], "cash": 0, "checks": checks,
                "reason": "free quota exhausted, refill before the deadline; recheck availability at wake-up; "
                          + evidence(rates, family, chosen),
                "wake_in_minutes": chosen["reset_minutes"]}
    paid = [r for r in eligible if r["available"] and 0 < r["cash"] <= request["budget"]]
    if paid:
        chosen = paid[0]
        return {"action": "run", "resource": chosen["id"], "cash": chosen["cash"], "checks": checks,
                "reason": "no free eligible route in time; paid route of the same model within the budget; "
                          + evidence(rates, family, chosen)}
    if not eligible:
        reason = f"no model correct on every TD 1 cell of {family} ({', '.join(FAMILIES[family])})"
    else:
        rejected = []
        for r in eligible:
            if r["cash"] > 0:
                why = f"costs {r['cash']} USD, over the budget of {request['budget']}" if r["available"] else "unavailable"
            elif r["reset_minutes"] is None:
                why = "unavailable, no announced refill"
            elif r["reset_minutes"] > request["deadline_minutes"]:
                why = f"unavailable, refill in {r['reset_minutes']} min, after the {request['deadline_minutes']}-min deadline"
            else:
                why = f"unavailable, refill in {r['reset_minutes']} min, and the request cannot wait"
            rejected.append(f"{r['id']} {why}")
        models = sorted({r["model"] for r in eligible}, key=PREFERENCE.index)
        reason = (f"no eligible route for {family} within deadline and budget: " + "; ".join(rejected) + "; "
                  + "; ".join(evidence(rates, family, {"model": m}) for m in models))
    return {"action": "abstain", "resource": None, "cash": 0, "checks": checks, "reason": reason}


def scenarios():
    base = {"family": "F1", "use": "dashboard", "can_wait": True, "deadline_minutes": 120, "budget": 0.001}
    groq_120b_exhausted = [dict(r, available=False, reset_minutes=60) if r["id"] == "groq:openai/gpt-oss-120b" else dict(r)
                           for r in RESOURCES]
    groq_20b_down = [dict(r, available=False) if r["id"] == "groq:openai/gpt-oss-20b" else dict(r) for r in RESOURCES]
    return [
        ("F1 dashboard", base, RESOURCES),
        ("F1 preferred route unavailable", base, groq_20b_down),
        ("F3 customer figure", {**base, "family": "F3", "use": "customer"}, RESOURCES),
        ("F2 customer figure", {**base, "family": "F2", "use": "customer"}, RESOURCES),
        ("F2 deferrable, free quota exhausted", {**base, "family": "F2"}, groq_120b_exhausted),
        ("F2 urgent, free quota exhausted", {**base, "family": "F2", "use": "customer", "can_wait": False,
                                             "deadline_minutes": 5}, groq_120b_exhausted),
        ("F2 urgent, no budget", {**base, "family": "F2", "use": "customer", "can_wait": False,
                                  "deadline_minutes": 5, "budget": 0}, groq_120b_exhausted),
        ("F2 amount paid out", {**base, "family": "F2", "use": "payout"}, RESOURCES),
        ("F2b customer figure", {**base, "family": "F2b", "use": "customer"}, RESOURCES),
        ("unknown family", {**base, "family": "F4"}, RESOURCES),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", help="show only the named scenario")
    args = parser.parse_args()
    found = False
    for name, request, resources in scenarios():
        if args.scenario and name != args.scenario:
            continue
        found = True
        print(json.dumps({"scenario": name, "nature": "simulation", "request": request,
                          "result": choose(request, resources)}))
    if not found:
        parser.error("unknown scenario")


if __name__ == "__main__":
    main()
