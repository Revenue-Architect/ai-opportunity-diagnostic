#!/usr/bin/env python3
"""Sort a business's jobs into Not AI / Not worth it / Not ready / Go and rank the Go jobs.

Usage:
    python scripts/diagnose.py <input.json>             # JSON result
    python scripts/diagnose.py <input.json> --markdown  # table, value breakdown, chart

Input format: assets/example-case.json. Standard library only.

Annual value = time back + revenue won or kept + money not lost, each weighted by
the evidence behind it, minus first-year build and running cost.
"""

import json
import re
import sys

WEEKS_PER_YEAR = 52

# Owner and staff hours claims further apart than this share of the larger claim
# count as conflicting.
CLAIM_GAP_LIMIT = 0.25

# How much of an estimate to trust, by the evidence behind it.
EVIDENCE_WEIGHT = {
    "export": 1.00,           # backed by real records
    "owner_and_staff": 0.85,  # owner and staff both gave hours and they agree
    "single_estimate": 0.65,  # one person's estimate
}

DRIVERS = ("time", "revenue", "losses")
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


def _choice(job, field, allowed):
    value = job.get(field)
    if value not in (None, allowed):
        raise InputError(f"job '{job['id']}': '{field}' must be \"{allowed}\" or left out")
    return value == allowed


def hours_check(job):
    """Compare owner and staff weekly-hours claims: agree, conflicting, or a single estimate."""
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

    unpriced = job.get("unpriced_drivers") or {}
    if not isinstance(unpriced, dict) or not set(unpriced) <= set(DRIVERS):
        raise InputError(f"job '{job['id']}': 'unpriced_drivers' keys must be among {', '.join(DRIVERS)}")

    level, claim_gap = hours_check(job)
    exported = _choice(job, "evidence", "export")
    money_records = _choice(job, "money_evidence", "records")
    money_weight = EVIDENCE_WEIGHT["export" if money_records else "single_estimate"]
    values, weights = {}, {}

    time_fields = ("weekly_volume", "minutes_per_item", "share_handled")
    if any(job.get(f) is not None for f in time_fields):
        rate = job.get("hourly_value", loaded_hourly_cost)
        if isinstance(rate, bool) or not isinstance(rate, (int, float)) or rate <= 0:
            raise InputError(f"job '{job['id']}': time is priced, so 'loaded_hourly_cost' "
                             "(or the job's 'hourly_value') must be a positive number")
        hours_per_week = _num(job, "weekly_volume") * _num(job, "minutes_per_item") / 60
        values["time"] = hours_per_week * WEEKS_PER_YEAR * rate * _num(job, "share_handled", 0, 1)
        if level == "conflicting":
            weights["time"] = EVIDENCE_WEIGHT["single_estimate"]
        else:
            weights["time"] = EVIDENCE_WEIGHT["export" if exported else level]
        result.update(hours_per_week=round(hours_per_week, 2), hourly_value=rate)
        if job.get("hourly_value_basis"):
            result["hourly_value_basis"] = job["hourly_value_basis"]

    if job.get("recovered_revenue_annual") is not None:
        values["revenue"] = (_num(job, "recovered_revenue_annual")
                             * _num(job, "gross_margin", 0, 1)
                             * _num(job, "recapture_rate", 0, 1))
        weights["revenue"] = money_weight

    if job.get("losses_avoided_annual") is not None:
        values["losses"] = _num(job, "losses_avoided_annual") * _num(job, "share_avoided", 0, 1)
        weights["losses"] = money_weight

    year_value = sum(values[d] * weights[d] for d in values)
    if "time" in values:
        evidence = "conflicting" if level == "conflicting" else ("export" if exported else level)
    else:
        evidence = "records" if money_records else "single_estimate"
    result.update(
        values={d: round(v) for d, v in values.items()},
        weights=weights,
        unpriced=unpriced,
        noted_benefits=job.get("noted_benefits") or [],
        evidence=evidence,
        claim_gap=claim_gap,
        year_one_value=round(year_value),
    )

    blockers = []
    if not values:
        blockers.append("value: no driver priced yet" + (f" ({'; '.join(unpriced.values())})" if unpriced else ""))
    elif job.get("build_cost") is not None and job.get("monthly_run_cost") is not None:
        build = _num(job, "build_cost")
        run_annual = _num(job, "monthly_run_cost") * 12
        net = year_value - run_annual - build
        result.update(build_cost=round(build), annual_run_cost=round(run_annual), net_first_year=round(net))
        if net <= 0:
            result.update(outcome=NOT_WORTH_IT, reason="does not pay back its build and run cost within a year")
            return result
    else:
        blockers.append("quote: pays back if total first-year cost (build plus a year of running) "
                        f"stays under ${round(year_value):,}")

    if level == "conflicting":
        claims = job["hours_claims"]
        blockers.append(f"hours: owner says {claims['owner']} a week, staff say {claims['staff']}; "
                        "reconcile what each is counting and confirm with a quick time check")
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
    return {"business": case.get("business"), "ai_tool": case.get("ai_tool"),
            "recommended": [r["id"] for r in go], "jobs": results}


def _label(text):
    return " ".join(re.sub(r"[^\w -]+", " ", text).split())


def _money(n):
    return f"{'-' if n < 0 else ''}${abs(n):,}"


def quadrant_chart(results):
    """Value per year against build cost relative to value, for jobs that have a quote.

    The x position is the share of a year's value left after paying for the build, so it
    does not depend on the other jobs. Value is scaled to the most valuable charted job.
    Drawn only when at least two jobs can be compared.
    """
    scored = [r for r in results if "build_cost" in r]
    if len(scored) < 2:
        return ""
    top_value = max(max(r["year_one_value"] for r in scored), 1)
    lines = [
        "quadrantChart",
        "  title Value vs build cost",
        "  x-axis Higher build cost vs value --> Lower build cost vs value",
        "  y-axis Less value --> More value",
        "  quadrant-1 More value, cheaper to build",
        "  quadrant-2 More value, costlier to build",
        "  quadrant-3 Less value, costlier to build",
        "  quadrant-4 Less value, cheaper to build",
    ]
    for r in scored:
        x = round(1 - min(r["build_cost"] / max(r["year_one_value"], 1), 1), 2)
        y = round(r["year_one_value"] / top_value, 2)
        x, y = min(max(x, 0.02), 0.98), min(max(y, 0.02), 0.98)
        label = _label(r["name"] + " - " + r["outcome"])
        lines.append(f'  "{label}": [{x}, {y}]')
    return "\n".join(lines)


def value_breakdown(r):
    lines = [f"**{r['name']}**"]
    names = {"time": "Time back", "revenue": "Revenue won or kept", "losses": "Money not lost"}
    for d in DRIVERS:
        if d in r["values"]:
            basis = ""
            if d == "time":
                basis = f" ({r['hours_per_week']} h/week at ${r['hourly_value']:,}/h"
                basis += f", {r['hourly_value_basis']})" if r.get("hourly_value_basis") else ")"
            lines.append(f"- {names[d]}: {_money(r['values'][d])} a year{basis}, "
                         f"counted at {r['weights'][d]:.0%} for the evidence behind it")
        elif d in r["unpriced"]:
            lines.append(f"- {names[d]}: not priced ({r['unpriced'][d]})")
    for benefit in r["noted_benefits"]:
        lines.append(f"- Also: {benefit} (not priced)")
    return "\n".join(lines)


def to_markdown(report):
    rows = ["| Rank | Job | Outcome | Value per year | Net first year | Evidence | Why |",
            "|---|---|---|---|---|---|---|"]
    ordered = sorted(report["jobs"], key=lambda r: r.get("year_one_value", float("-inf")), reverse=True)
    for r in ordered:
        value = _money(r["year_one_value"]) if "year_one_value" in r else "–"
        net = "–"
        if "net_first_year" in r:
            net = _money(r["net_first_year"])
        elif "year_one_value" in r:
            net = "needs quote"
        evidence = r.get("evidence", "–").replace("_", " ")
        cells = [r.get("rank", ""), r["name"], r["outcome"], value, net, evidence, r["reason"]]
        cells = [" ".join(str(cell).splitlines()).replace("|", r"\|") for cell in cells]
        rows.append("| " + " | ".join(cells) + " |")
    title = f"## {report['business']}\n\n" if report.get("business") else ""
    out = title + "\n".join(rows) + "\n"
    breakdowns = [value_breakdown(r) for r in ordered if "values" in r]
    if breakdowns:
        out += "\n### Where the value comes from\n\n" + "\n\n".join(breakdowns) + "\n"
    chart = quadrant_chart(report["jobs"])
    if chart:
        out += f"\n```mermaid\n{chart}\n```\n"
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
