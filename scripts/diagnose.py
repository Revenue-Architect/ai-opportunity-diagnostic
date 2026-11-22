#!/usr/bin/env python3
"""Sort a business's jobs into Not AI / Not worth it / Not ready / Go and rank the Go jobs.

Usage:
    python scripts/diagnose.py <input.json>             # JSON result
    python scripts/diagnose.py <input.json> --markdown  # table + Mermaid quadrant chart

Input format: assets/example-case.json. Standard library only.
"""

import json
import re
import sys

WEEKS_PER_YEAR = 52

# Owner and staff hours claims further apart than this share of the larger claim
# count as conflicting.
CLAIM_GAP_LIMIT = 0.25

# How much of the claimed value to trust, by the strongest evidence behind it.
EVIDENCE_WEIGHT = {
    "export": 1.00,           # volume counted from 30 days of real records
    "owner_and_staff": 0.85,  # both gave hours and they agree
    "single_estimate": 0.65,  # one person's estimate
    "conflicting": 0.50,      # owner and staff disagree and no export settles it
}

NOT_AI, NOT_WORTH_IT, NOT_READY, GO = "Not AI", "Not worth it", "Not ready", "Go"


class InputError(ValueError):
    pass


def _num(job, field, lo=0.0, hi=None):
    value = job.get(field)
    if value is None:
        raise InputError(f"job '{job.get('id', '?')}': missing '{field}'")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise InputError(f"job '{job.get('id', '?')}': '{field}' must be a number, got {value!r}")
    if value < lo or (hi is not None and value > hi):
        bound = f"between {lo} and {hi}" if hi is not None else f"at least {lo}"
        raise InputError(f"job '{job.get('id', '?')}': '{field}' must be {bound}, got {value}")
    return float(value)


def evidence_level(job):
    if job.get("evidence") == "export":
        return "export", None
    if job.get("evidence") not in (None, "export"):
        raise InputError(f"job '{job.get('id', '?')}': 'evidence' must be \"export\" or left out")
    claims = job.get("hours_claims") or {}
    owner, staff = claims.get("owner"), claims.get("staff")
    if owner is not None and staff is not None:
        larger = max(owner, staff)
        gap = abs(owner - staff) / larger if larger else 0.0
        return ("conflicting" if gap > CLAIM_GAP_LIMIT else "owner_and_staff"), round(gap, 3)
    return "single_estimate", None


def assess(job, loaded_hourly_cost):
    result = {"id": job["id"], "name": job["name"]}

    if job.get("rule_covers_most"):
        if not job.get("rule_fix"):
            raise InputError(f"job '{job['id']}': 'rule_covers_most' is true, so name the fix in 'rule_fix'")
        result.update(outcome=NOT_AI, reason=job["rule_fix"])
        return result

    hours_per_week = _num(job, "weekly_volume") * _num(job, "minutes_per_item") / 60
    share = _num(job, "share_handled", 0, 1)
    labour = hours_per_week * WEEKS_PER_YEAR * loaded_hourly_cost * share

    revenue = 0.0
    if job.get("recovered_revenue_annual"):
        revenue = (_num(job, "recovered_revenue_annual")
                   * _num(job, "gross_margin", 0, 1)
                   * _num(job, "recapture_rate", 0, 1))

    level, claim_gap = evidence_level(job)
    weight = EVIDENCE_WEIGHT[level]
    run_annual = _num(job, "monthly_run_cost") * 12
    build = _num(job, "build_cost")
    net = (labour + revenue) * weight - run_annual - build

    result.update(
        hours_per_week=round(hours_per_week, 2),
        annual_labour_value=round(labour),
        annual_revenue_value=round(revenue),
        evidence=level,
        evidence_weight=weight,
        claim_gap=claim_gap,
        build_cost=round(build),
        annual_run_cost=round(run_annual),
        net_first_year=round(net),
    )

    if result["net_first_year"] <= 0:
        result.update(outcome=NOT_WORTH_IT, reason="does not pay back its build and run cost within a year")
        return result

    blockers = []
    if not job.get("data_ready"):
        blockers.append(f"data: {job.get('data_blocker') or 'records not usable yet'}")
    if not job.get("on_own_is_reversible"):
        blockers.append("reversibility: move every hard-to-undo action into asks_first")
    if not job.get("approver"):
        blockers.append("no named approver")
    if not job.get("rollback"):
        blockers.append("no same-day rollback")
    if blockers:
        result.update(outcome=NOT_READY, reason="; ".join(blockers))
        return result

    result.update(outcome=GO, reason="clears every gate")
    return result


def diagnose(case):
    cost = case.get("loaded_hourly_cost")
    if not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost <= 0:
        raise InputError("'loaded_hourly_cost' must be a positive number")
    jobs = case.get("jobs") or []
    if not jobs:
        raise InputError("'jobs' is empty")
    ids = [j.get("id") for j in jobs]
    if None in ids or len(set(ids)) != len(ids):
        raise InputError("every job needs a unique 'id'")
    for j in jobs:
        if not j.get("name"):
            raise InputError(f"job '{j['id']}': missing 'name'")

    results = [assess(j, float(cost)) for j in jobs]
    go = sorted((r for r in results if r["outcome"] == GO), key=lambda r: -r["net_first_year"])
    for rank, r in enumerate(go, 1):
        r["rank"] = rank
    return {"business": case.get("business"), "recommended": [r["id"] for r in go], "jobs": results}


def _label(text):
    return re.sub(r"[^A-Za-z0-9 \-]", "", text).strip() or "job"


def quadrant_chart(results):
    """Value (net first year) against ease (lower build cost). Not AI jobs are left out."""
    scored = [r for r in results if r["outcome"] != NOT_AI]
    if not scored:
        return ""
    top_value = max(max(r["net_first_year"] for r in scored), 1)
    top_build = max(max(r["build_cost"] for r in scored), 1)
    lines = [
        "quadrantChart",
        "  title Value vs ease",
        "  x-axis Harder to build --> Easier to build",
        "  y-axis Less value --> More value",
        "  quadrant-1 Do first",
        "  quadrant-2 Plan for",
        "  quadrant-3 Skip",
        "  quadrant-4 Small wins",
    ]
    for r in scored:
        x = round(1 - r["build_cost"] / top_build, 2)
        y = round(max(r["net_first_year"], 0) / top_value, 2)
        x, y = min(max(x, 0.02), 0.98), min(max(y, 0.02), 0.98)
        lines.append(f"  {_label(r['name'] + ' - ' + r['outcome'])}: [{x}, {y}]")
    return "\n".join(lines)


def to_markdown(report):
    rows = ["| Rank | Job | Outcome | Net first year | Evidence | Why |", "|---|---|---|---|---|---|"]
    order = {GO: 0, NOT_READY: 1, NOT_WORTH_IT: 2, NOT_AI: 3}
    for r in sorted(report["jobs"], key=lambda r: (order[r["outcome"]], r.get("rank", 0))):
        net = "–"
        if "net_first_year" in r:
            n = r["net_first_year"]
            net = f"{'-' if n < 0 else ''}${abs(n):,}"
        rows.append(f"| {r.get('rank', '')} | {r['name']} | {r['outcome']} | {net} | "
                    f"{r.get('evidence', '–')} | {r['reason']} |")
    chart = quadrant_chart(report["jobs"])
    title = f"## {report['business']}\n\n" if report.get("business") else ""
    return title + "\n".join(rows) + (f"\n\n```mermaid\n{chart}\n```\n" if chart else "\n")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(argv) >= 2 else 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            report = diagnose(json.load(f))
    except (OSError, json.JSONDecodeError, InputError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(to_markdown(report) if "--markdown" in argv else json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
