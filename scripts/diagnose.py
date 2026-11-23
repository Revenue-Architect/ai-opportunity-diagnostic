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
# Conflicting owner and staff claims are valued as a single estimate and block Go
# until records settle the gap.
EVIDENCE_WEIGHT = {
    "export": 1.00,           # volume counted from real records
    "owner_and_staff": 0.85,  # both gave hours and they agree
    "single_estimate": 0.65,  # one person's estimate
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

    if not isinstance(job.get("rule_covers_most"), bool):
        raise InputError(f"job '{job['id']}': 'rule_covers_most' must be true or false")
    if job["rule_covers_most"]:
        if not job.get("rule_fix"):
            raise InputError(f"job '{job['id']}': 'rule_covers_most' is true, so name the fix in 'rule_fix'")
        result.update(outcome=NOT_AI, reason=job["rule_fix"])
        return result

    if (isinstance(loaded_hourly_cost, bool) or not isinstance(loaded_hourly_cost, (int, float))
            or loaded_hourly_cost <= 0):
        raise InputError("'loaded_hourly_cost' must be a positive number")
    hours_per_week = _num(job, "weekly_volume") * _num(job, "minutes_per_item") / 60
    share = _num(job, "share_handled", 0, 1)
    labour = hours_per_week * WEEKS_PER_YEAR * loaded_hourly_cost * share

    revenue = 0.0
    if job.get("recovered_revenue_annual"):
        revenue = (_num(job, "recovered_revenue_annual")
                   * _num(job, "gross_margin", 0, 1)
                   * _num(job, "recapture_rate", 0, 1))

    level, claim_gap = evidence_level(job)
    weight = EVIDENCE_WEIGHT["single_estimate" if level == "conflicting" else level]
    year_value = (labour + revenue) * weight

    result.update(
        hours_per_week=round(hours_per_week, 2),
        annual_labour_value=round(labour),
        annual_revenue_value=round(revenue),
        evidence=level,
        evidence_weight=weight,
        claim_gap=claim_gap,
        year_one_value=round(year_value),
    )

    blockers = []
    quoted = job.get("build_cost") is not None and job.get("monthly_run_cost") is not None
    if quoted:
        build = _num(job, "build_cost")
        run_annual = _num(job, "monthly_run_cost") * 12
        net = year_value - run_annual - build
        result.update(build_cost=round(build), annual_run_cost=round(run_annual), net_first_year=round(net))
        if net <= 0:
            result.update(outcome=NOT_WORTH_IT, reason="does not pay back its build and run cost within a year")
            return result
    else:
        blockers.append(f"quote: pays back if the build plus a year of running costs stays under ${round(year_value):,}")

    if level == "conflicting":
        claims = job["hours_claims"]
        blockers.append(f"hours: owner says {claims['owner']} a week, staff say {claims['staff']}; "
                        "settle it with real records")
    for field in ("data_ready", "on_own_is_reversible"):
        if field in job and not isinstance(job[field], bool):
            raise InputError(f"job '{job['id']}': '{field}' must be true or false")
    if not job.get("data_ready"):
        blockers.append(f"data: {job.get('data_blocker') or 'records not usable yet'}")
    if not job.get("on_own_is_reversible"):
        blockers.append("someone must approve a hard-to-undo step outside the owner's limits")
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
    jobs = case.get("jobs") or []
    if not jobs:
        raise InputError("'jobs' is empty")
    ids = [j.get("id") for j in jobs]
    if None in ids or len(set(ids)) != len(ids):
        raise InputError("every job needs a unique 'id'")
    for j in jobs:
        if not j.get("name"):
            raise InputError(f"job '{j['id']}': missing 'name'")

    results = [assess(j, cost) for j in jobs]
    go = sorted((r for r in results if r["outcome"] == GO), key=lambda r: -r["net_first_year"])
    for rank, r in enumerate(go, 1):
        r["rank"] = rank
    return {"business": case.get("business"), "recommended": [r["id"] for r in go], "jobs": results}


def _label(text):
    return " ".join(re.sub(r"[^\w -]+", " ", text).split())


def quadrant_chart(results):
    """Value per year against ease, for jobs that have a quote.

    Ease is the share of a year's value left after paying for the build, so it does not
    depend on the other jobs. Value is scaled to the most valuable charted job.
    """
    scored = [r for r in results if "build_cost" in r]
    if not scored:
        return ""
    top_value = max(max(r["year_one_value"] for r in scored), 1)
    lines = [
        "quadrantChart",
        "  title Value vs ease",
        "  x-axis Harder to build --> Easier to build",
        "  y-axis Less value --> More value",
        "  quadrant-1 Higher value and easier",
        "  quadrant-2 Higher value and harder",
        "  quadrant-3 Lower value and harder",
        "  quadrant-4 Lower value and easier",
    ]
    for r in scored:
        x = round(1 - min(r["build_cost"] / max(r["year_one_value"], 1), 1), 2)
        y = round(r["year_one_value"] / top_value, 2)
        x, y = min(max(x, 0.02), 0.98), min(max(y, 0.02), 0.98)
        label = _label(r["name"] + " - " + r["outcome"])
        lines.append(f'  "{label}": [{x}, {y}]')
    return "\n".join(lines)


def to_markdown(report):
    rows = ["| Rank | Job | Outcome | Value per year | Net first year | Evidence | Why |",
            "|---|---|---|---|---|---|---|"]
    for r in sorted(report["jobs"], key=lambda r: r.get("year_one_value", float("-inf")), reverse=True):
        value = f"${r['year_one_value']:,}" if "year_one_value" in r else "–"
        net = "–"
        if "net_first_year" in r:
            n = r["net_first_year"]
            net = f"{'-' if n < 0 else ''}${abs(n):,}"
        elif "year_one_value" in r:
            net = "needs quote"
        evidence = r.get("evidence", "–").replace("_", " ")
        cells = [r.get("rank", ""), r["name"], r["outcome"], value, net, evidence, r["reason"]]
        cells = [" ".join(str(cell).splitlines()).replace("|", r"\|") for cell in cells]
        rows.append("| " + " | ".join(cells) + " |")
    chart = quadrant_chart(report["jobs"])
    title = f"## {report['business']}\n\n" if report.get("business") else ""
    out = title + "\n".join(rows) + (f"\n\n```mermaid\n{chart}\n```\n" if chart else "\n")
    if any("year_one_value" in r and "net_first_year" not in r for r in report["jobs"]):
        out += "\nJobs without a quote are not charted.\n"
    return out


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
