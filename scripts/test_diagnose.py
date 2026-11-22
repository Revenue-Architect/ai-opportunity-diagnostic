"""Plain-assert checks for diagnose.py. Run: python scripts/test_diagnose.py

Uses the made-up example case.
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
    estimated = dict(EXAMPLE["jobs"][0], evidence=None, hours_claims={"owner": 4, "staff": 4})
    estimate = diagnose(dict(EXAMPLE, jobs=[estimated]))["jobs"][0]
    assert (estimate["evidence"], estimate["net_first_year"]) == ("owner_and_staff", 6889)
    # Owner says 3 h, staff says 6 h: gap 0.5 is conflicting, weight 0.5.
    # (20 x 10 / 60) x 52 x 45 x 0.8 = 6240; x 0.5 - 600 - 1000 = 1520.
    i = jobs["invoice_chasing"]
    assert (i["evidence"], i["claim_gap"], i["net_first_year"]) == ("conflicting", 0.5, 1520)


def test_ranking():
    report = diagnose(EXAMPLE)
    assert report["recommended"] == ["after_hours_inquiries", "invoice_chasing"]


def test_no_ai_needs_no_hourly_rate():
    job = next(j for j in EXAMPLE["jobs"] if j["rule_covers_most"])
    assert diagnose({"jobs": [job]})["jobs"][0]["outcome"] == "Not AI"


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


def test_incomplete_or_quoted_gate_answers():
    for field in ("rule_covers_most", "data_ready", "on_own_is_reversible"):
        job = dict(EXAMPLE["jobs"][0])
        if field == "rule_covers_most":
            del job[field]
        else:
            job[field] = "false"
        try:
            diagnose(dict(EXAMPLE, jobs=[job]))
        except InputError as e:
            assert field in str(e)
        else:
            raise AssertionError(f"accepted incomplete or quoted {field}")


def test_markdown_has_chart():
    case = copy.deepcopy(EXAMPLE)
    case["jobs"][0]["name"] = "Title checks (new): A | B"
    case["jobs"][1]["build_cost"] = 1000  # Blocked quote drafting is worth more than invoice chasing.
    md = to_markdown(diagnose(case))
    table, chart = md.split("quadrantChart")
    assert r"Title checks (new): A \| B" in table
    assert '"Title checks new A B - Go": [' in chart
    assert "Appointment reminders" in table and "Appointment reminders" not in chart
    assert table.index("Quote drafting") < table.index("Overdue invoice chasing")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} checks passed")
