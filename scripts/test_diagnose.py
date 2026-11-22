"""Plain-assert checks for diagnose.py. Run: python scripts/test_diagnose.py

Uses the made-up example case. Add each real diagnostic as its own case here.
"""

import copy
import json
from pathlib import Path

from diagnose import InputError, diagnose, to_markdown

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = json.loads((ROOT / "assets" / "example-case.json").read_text(encoding="utf-8"))


def by_id(report):
    return {r["id"]: r for r in report["jobs"]}


def test_example_outcomes():
    jobs = by_id(diagnose(EXAMPLE))
    assert jobs["appointment_reminders"]["outcome"] == "Not AI"
    assert jobs["daily_numbers"]["outcome"] == "Not worth it"
    assert jobs["quote_drafting"]["outcome"] == "Not ready"
    assert jobs["quote_drafting"]["reason"].startswith("data:")
    assert jobs["after_hours_inquiries"]["outcome"] == "Go"
    assert jobs["invoice_chasing"]["outcome"] == "Go"


def test_example_values():
    jobs = by_id(diagnose(EXAMPLE))
    # 40 x 6 min = 4 h/wk; 4 x 52 x 45 x 0.7 = 6552 labour; 60000 x 0.4 x 0.3 = 7200 revenue;
    # export weight 1.0; minus 1800 run and 3000 build.
    a = jobs["after_hours_inquiries"]
    assert (a["annual_labour_value"], a["annual_revenue_value"], a["net_first_year"]) == (6552, 7200, 8952)
    # Owner says 3 h, staff says 6 h: gap 0.5 is conflicting, weight 0.5.
    # (20 x 10 / 60) x 52 x 45 x 0.8 = 6240; x 0.5 - 600 - 1000 = 1520.
    i = jobs["invoice_chasing"]
    assert (i["evidence"], i["claim_gap"], i["net_first_year"]) == ("conflicting", 0.5, 1520)


def test_ranking():
    report = diagnose(EXAMPLE)
    assert report["recommended"] == ["after_hours_inquiries", "invoice_chasing"]


def test_same_input_same_output():
    first = json.dumps(diagnose(EXAMPLE), sort_keys=True)
    assert all(json.dumps(diagnose(EXAMPLE), sort_keys=True) == first for _ in range(5))


def test_missing_approver_blocks_go():
    case = copy.deepcopy(EXAMPLE)
    case["jobs"][0]["approver"] = ""
    job = by_id(diagnose(case))["after_hours_inquiries"]
    assert job["outcome"] == "Not ready" and "approver" in job["reason"]


def test_bad_input_is_reported():
    case = copy.deepcopy(EXAMPLE)
    del case["jobs"][0]["weekly_volume"]
    try:
        diagnose(case)
    except InputError as e:
        assert "weekly_volume" in str(e)
    else:
        raise AssertionError("missing field was not reported")


def test_markdown_has_chart():
    md = to_markdown(diagnose(EXAMPLE))
    assert "quadrantChart" in md and "Appointment reminders" in md


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} checks passed")
