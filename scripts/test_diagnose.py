"""Plain-assert checks for diagnose.py and profile_csv.py. Run: python scripts/test_diagnose.py

Uses the made-up example case and the trap cases from the original blueprint.
"""

import copy
import json
import os
import tempfile
from pathlib import Path

from diagnose import InputError, diagnose, to_markdown
from profile_csv import profile

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = json.loads((ROOT / "assets" / "example-case.json").read_text(encoding="utf-8"))
CLEAN = EXAMPLE["jobs"][0]  # after-hours inquiries: volume from an export, every gate clear
GATES = {"rule_covers_most": False, "data_ready": True, "on_own_is_reversible": True,
         "approver": "Owner", "rollback": "Turn it off", "build_cost": 500, "monthly_run_cost": 50}


def by_id(report):
    return {r["id"]: r for r in report["jobs"]}


def job(**changes):
    return dict(CLEAN, **changes)


def run(*jobs):
    return diagnose(dict(EXAMPLE, jobs=list(jobs)))


# --- Example case ---------------------------------------------------------------

def test_example_outcomes():
    jobs = by_id(diagnose(EXAMPLE))
    assert jobs["appointment_reminders"]["outcome"] == "Not AI"
    assert jobs["daily_numbers"]["outcome"] == "Not worth it"
    assert jobs["quote_drafting"]["outcome"] == "Not ready"
    assert jobs["quote_drafting"]["reason"].startswith("data:")
    assert jobs["after_hours_inquiries"]["outcome"] == "Go"
    assert jobs["invoice_chasing"]["outcome"] == "Not ready"
    assert jobs["invoice_chasing"]["reason"].startswith("hours:")


def test_example_values():
    jobs = by_id(diagnose(EXAMPLE))
    # Time: 40 x 6 min = 4 h/wk; 4 x 52 x 45 x 0.7 = 6552, volume from an export so counted at 1.0.
    # Revenue: 60000 x 0.4 x 0.3 = 7200, an estimate so counted at 0.65 = 4680.
    # 6552 + 4680 = 11232; minus 1800 run and 3000 build = 6432.
    a = jobs["after_hours_inquiries"]
    assert a["values"] == {"time": 6552, "revenue": 7200}
    assert (a["weights"], a["year_one_value"], a["net_first_year"]) == (
        {"time": 1.0, "revenue": 0.65}, 11232, 6432)
    # Owner and staff agree (no export): time at 0.85 = 5569.2; + 4680 - 4800 = 5449.
    estimate = run(job(evidence=None, hours_claims={"owner": 4, "staff": 4}))["jobs"][0]
    assert (estimate["evidence"], estimate["net_first_year"]) == ("owner_and_staff", 5449)
    # Owner says 3 h, staff say 6 h: conflicting, valued as a single estimate (0.65).
    # Time (20 x 10 / 60) x 52 x 45 x 0.8 = 6240; losses 4000 x 0.5 = 2000.
    # (6240 + 2000) x 0.65 = 5356; minus 600 run and 1000 build = 3756.
    i = jobs["invoice_chasing"]
    assert (i["evidence"], i["claim_gap"], i["year_one_value"], i["net_first_year"]) == (
        "conflicting", 0.5, 5356, 3756)


def test_ranking():
    assert diagnose(EXAMPLE)["recommended"] == ["after_hours_inquiries"]
    assert diagnose(EXAMPLE)["ai_tool"] == "ChatGPT"


def test_same_input_same_output():
    first = json.dumps(diagnose(EXAMPLE), sort_keys=True)
    assert all(json.dumps(diagnose(EXAMPLE), sort_keys=True) == first for _ in range(5))


# --- Trap cases from the original blueprint -------------------------------------

def test_trap_rules_job_is_not_ai():
    # Owner wants an AI to tag wholesale orders by SKU prefix and route them by province.
    report = run(job(id="sku_routing", name="Wholesale order routing", rule_covers_most=True,
                     rule_fix="Order-routing rule on SKU prefix and province in the store admin"))
    assert report["jobs"][0]["outcome"] == "Not AI" and report["recommended"] == []


def test_trap_poisoned_data_blocks_a_valuable_job():
    # Big claimed value, but the records behind it are half blank.
    report = run(job(id="quotes", name="Quote generation", weekly_volume=60, minutes_per_item=30,
                     data_ready=False, data_blocker="job type blank on 47% of past jobs"))
    j = report["jobs"][0]
    assert j["net_first_year"] > 20000 and j["outcome"] == "Not ready" and "47%" in j["reason"]


def test_trap_owner_staff_gap_loses_to_the_verified_job():
    # CEO claims 35 h/wk on returns; the ops lead says 6. Freight reconciliation has records.
    returns = job(id="returns", name="Returns triage", evidence=None, weekly_volume=150,
                  minutes_per_item=14, hours_claims={"owner": 35, "staff": 6})
    freight = job(id="freight", name="Freight bill reconciliation", weekly_volume=112,
                  minutes_per_item=15, recovered_revenue_annual=None)
    report = run(returns, freight)
    jobs = by_id(report)
    assert jobs["returns"]["evidence"] == "conflicting" and jobs["returns"]["claim_gap"] == 0.829
    assert jobs["returns"]["outcome"] == "Not ready"
    assert report["recommended"] == ["freight"]


def test_trap_autonomous_refunds_are_not_ready():
    # Ops head wants refunds up to $2,500 issued with no review, no approver and no rollback.
    j = run(job(id="refunds", name="Refunds", on_own_is_reversible=False, approver=None,
                rollback=None))["jobs"][0]
    assert j["outcome"] == "Not ready"
    assert all(word in j["reason"] for word in ("hard-to-undo", "approver", "rollback"))


def test_trap_clean_job_is_a_go():
    report = run(CLEAN)
    assert report["recommended"] == ["after_hours_inquiries"]
    assert report["jobs"][0]["evidence"] == "export"


def test_not_yet_when_nothing_clears():
    report = run(job(id="a", rule_covers_most=True, rule_fix="Booking tool reminder"),
                 job(id="b", build_cost=50000),
                 job(id="c", data_ready=False))
    assert report["recommended"] == []
    assert [j["outcome"] for j in report["jobs"]] == ["Not AI", "Not worth it", "Not ready"]


def test_no_quote_reports_the_most_a_build_can_cost():
    j = run(job(build_cost=None, monthly_run_cost=None))["jobs"][0]
    assert j["outcome"] == "Not ready" and "net_first_year" not in j
    assert "total first-year cost" in j["reason"] and "$11,232" in j["reason"]
    assert "needs quote" in to_markdown(run(job(build_cost=None, monthly_run_cost=None)))


# --- Value model ----------------------------------------------------------------

def test_export_proves_volume_only():
    # The export lifts time to full weight; money estimates stay at 0.65 unless backed by records.
    assert run(CLEAN)["jobs"][0]["weights"] == {"time": 1.0, "revenue": 0.65}
    with_records = run(job(money_evidence="records"))["jobs"][0]
    assert (with_records["weights"]["revenue"], with_records["year_one_value"]) == (1.0, 13752)


def test_export_does_not_settle_conflicting_hours():
    j = run(job(hours_claims={"owner": 35, "staff": 6}))["jobs"][0]
    assert j["evidence"] == "conflicting" and j["weights"]["time"] == 0.65
    assert j["outcome"] == "Not ready" and "reconcile what each is counting" in j["reason"]


def test_owner_hourly_value_overrides_staff_rate():
    j = run(job(hourly_value=90, hourly_value_basis="net margin per billable hour"))["jobs"][0]
    assert j["values"]["time"] == 13104  # 4 h/wk x 52 x 90 x 0.7
    assert "net margin per billable hour" in to_markdown(run(job(hourly_value=90,
                                                                 hourly_value_basis="net margin per billable hour")))


def test_revenue_only_job_needs_no_time_fields_or_hourly_cost():
    hangups = dict(GATES, id="hangups", name="Callers who hang up",
                   recovered_revenue_annual=20000, gross_margin=0.5, recapture_rate=0.2)
    j = diagnose({"jobs": [hangups]})["jobs"][0]
    # 20000 x 0.5 x 0.2 = 2000 at 0.65 = 1300; minus 600 run and 500 build = 200.
    assert (j["values"], j["net_first_year"], j["outcome"]) == ({"revenue": 2000}, 200, "Go")


def test_losses_only_job():
    refunds = dict(GATES, id="refunds", name="Wrong-size refunds",
                   losses_avoided_annual=4000, share_avoided=0.5)
    estimate = diagnose({"jobs": [refunds]})["jobs"][0]
    records = diagnose({"jobs": [dict(refunds, money_evidence="records")]})["jobs"][0]
    assert (estimate["values"], estimate["year_one_value"], records["year_one_value"]) == (
        {"losses": 2000}, 1300, 2000)


def test_unpriced_and_noted_are_shown_not_added():
    j = job(recovered_revenue_annual=None, unpriced_drivers={"revenue": "owner couldn't estimate"},
            noted_benefits=["Evenings back"])
    report = run(j)
    assert report["jobs"][0]["year_one_value"] == 6552
    md = to_markdown(report)
    assert "Revenue won or kept: not priced (owner couldn't estimate)" in md
    assert "Also: Evenings back (not priced)" in md


def test_nothing_priced_is_not_ready():
    bare = dict(GATES, id="bare", name="Something vague",
                unpriced_drivers={"revenue": "owner couldn't estimate"})
    j = diagnose({"jobs": [bare]})["jobs"][0]
    assert j["outcome"] == "Not ready" and j["reason"].startswith("value: no driver priced yet")


def test_value_breakdown_wording():
    md = to_markdown(run(CLEAN))
    assert "Time back: $6,552 a year (4.0 h/week at $45/h), counted at 100%" in md
    assert "Revenue won or kept: $7,200 a year, counted at 65%" in md


# --- Input checks and output ----------------------------------------------------

def test_no_ai_needs_no_hourly_rate():
    rule_job = next(j for j in EXAMPLE["jobs"] if j["rule_covers_most"])
    assert diagnose({"jobs": [rule_job]})["jobs"][0]["outcome"] == "Not AI"
    assert diagnose({"jobs": [rule_job]})["ai_tool"] is None


def test_missing_approver_blocks_go():
    j = run(job(approver=""))["jobs"][0]
    assert j["outcome"] == "Not ready" and "approver" in j["reason"]


def test_bad_input_is_reported():
    case = copy.deepcopy(EXAMPLE)
    del case["jobs"][0]["weekly_volume"]
    try:
        diagnose(case)
    except InputError as e:
        assert "weekly_volume" in str(e)
    else:
        raise AssertionError("missing field was not reported")


def test_incomplete_or_quoted_gate_answers():
    for field in ("rule_covers_most", "data_ready", "on_own_is_reversible"):
        bad = dict(CLEAN)
        if field == "rule_covers_most":
            del bad[field]
        else:
            bad[field] = "false"
        try:
            run(bad)
        except InputError as e:
            assert field in str(e)
        else:
            raise AssertionError(f"accepted incomplete or quoted {field}")


def test_markdown_table_and_chart():
    case = copy.deepcopy(EXAMPLE)
    case["jobs"][0]["name"] = "Title checks (new): A | B"
    md = to_markdown(diagnose(case))
    table, chart = md.split("quadrantChart")
    assert r"Title checks (new): A \| B" in table
    assert '"Title checks new A B - Go": [' in chart
    assert "Appointment reminders" in table and "Appointment reminders" not in chart
    assert table.index("| Quote drafting") < table.index("| Overdue invoice chasing")


def test_chart_needs_two_quoted_jobs():
    assert "quadrantChart" not in to_markdown(run(CLEAN))
    assert "quadrantChart" in to_markdown(run(CLEAN, job(id="b")))


def test_chart_position_does_not_depend_on_other_jobs():
    point = '"After-hours inquiries - Go": [0.96, 0.98]'
    assert point in to_markdown(run(job(build_cost=500), job(id="mid", build_cost=1000)))
    assert point in to_markdown(run(job(build_cost=500), job(id="big", build_cost=9000)))


# --- CSV profiler ---------------------------------------------------------------

def test_profile_csv_counts_volume_and_blanks():
    lines = ["date,type,job_type"]
    for day in range(1, 31):
        lines.append(f"2026-10-{day:02d},Quote,{'' if day % 2 else 'repair'}")
    lines.append("10/15/2026,Invoice,repair")
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        quotes = profile(path, "date", ("type", "Quote"))
        everything = profile(path, "date")
    finally:
        os.remove(path)
    assert (quotes["rows"], quotes["days_covered"], quotes["weekly_volume"]) == (30, 30, 7.0)
    assert quotes["blank_share"]["job_type"] == 0.5
    assert everything["rows"] == 31 and everything["unreadable_dates"] == 0


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} checks passed")
