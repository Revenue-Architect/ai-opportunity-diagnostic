# Plan and roadmap

Status as of 2026-11-22. The original V1 and V2 blueprints are in [original-blueprint.md](original-blueprint.md). Reviews are in [reviews/](reviews/).

## The decision the Skill serves

Should this small business get an AI assistant now, and if so, which jobs does it take on and which does it ask about first? "Not yet" is a valid answer. This Skill is the front door for agenticworks.ca, which sets up AI assistants that ask before money moves and stay owned by the client.

## What v1 is (built)

A single Agent Skill with no server. It runs on the client's own AI account, and the input JSON is the audit they keep and re-run each quarter.

- `SKILL.md` covers the rules and six stages: intake, the No-AI check, score, evidence, case against, report.
- `references/` holds the interview questions, the judgment calls behind each gate, and the report template.
- `scripts/diagnose.py` uses only the standard library. Its value is calculated at margin:
  - labour: hours × loaded cost × share handled
  - revenue: lost revenue × margin × recapture rate
  - that total × the evidence weight, minus first-year run and build cost

  It sorts each job into Not AI / Not worth it / Not ready (with blockers) / Go, ranks the Go jobs, and prints a table and a Mermaid quadrant chart.
  - No quote yet: the job is Not ready with a `quote:` blocker naming the most a build could cost and still pay back in year one, so an owner can run it alone.
  - Owner and staff hours that conflict: valued as a single estimate and Not ready until records settle the gap.
- `scripts/profile_csv.py` (standard library, runs locally) counts weekly volume, date span and blank share per column from a CSV export, so the model never counts records in prose.
- Owner limits: money actions ask first by default. The owner may let one run on its own up to an amount they name.
- `scripts/test_diagnose.py` holds 18 plain-assert checks: the made-up example, the blueprint's five trap cases, a "not yet" case, a no-quote case and the CSV profiler.
- [behaviour-checklist.md](behaviour-checklist.md) is a manual check of triggering and interview behaviour, to run whenever the instructions change.

## How v1 differs from the blueprint, and why

| Blueprint | v1 | Why |
|---|---|---|
| 5-axis weighted composite (30/25/20/15/10) with 1–5 ratings | Value at margin × evidence weight | The model picks the 1–5 ratings, so the composite is precise arithmetic on guesses. Dollars can be checked against reality. |
| Nine classifications | Four outcomes | Every blueprint bucket maps onto Not AI, Not worth it, Not ready or Go. |
| Revenue counted as drag (e.g. $170,400) | Revenue × margin × recapture | Recovered revenue is not profit. |
| Exec-vs-frontline delta with 4 evidence tiers | Same idea, simpler: export / agree / single estimate / conflicting | Kept the insight and dropped the extra flags. |
| Four mandatory diagrams | Quadrant chart (generated), before/after flow for the chosen job, roadmap table | Enough to support the decision. |
| Single approver, forbidden actions, rollback | Approver, asks-first, owner limits, rollback, Never list | Matches "asks before money moves". |
| 5 synthetic trap fixtures | The 5 traps plus "not yet" and no-quote, as script tests; real cases to be added | Traps guard the rules; calibration comes from real diagnostics. |
| CSV evidence profiler (server-side) | Local `profile_csv.py` | No client data leaves the machine. |
| Remote MCP server, state store, auth, Skills over MCP, ui:// workbench, dual-era elicitation | Not built | See the roadmap triggers below. |
| Lite / Pro split | Not built | No vertical packs exist yet, so there is nothing to split. |

## Roadmap

Each step starts when its trigger happens, not by calendar.

1. **First real diagnostics (next).** Run the Skill with 2–3 real businesses. Save each anonymized input file as a test case. Use these runs to fix interview friction and missing questions. Leave `CLAIM_GAP_LIMIT` and `EVIDENCE_WEIGHT` alone until about 10 diagnostics and their day-30 results are in, to avoid overfitting to two businesses.
2. **Day-30 check on each Go pilot.** Compare predicted weekly volume and hours back against the assistant's real logs. Change the interview or weights where predictions miss.
3. **Vertical notes.** Draft `references/verticals/<vertical>.md` after the first real client in that vertical. The trades and e-commerce lists in the blueprint are the starting candidates.
4. **Lite / Pro split.** Do this only after 3–5 clients in one vertical and evidence that owners will pay for the Skill itself rather than hiring agenticworks.ca. A build flag on the same folder decides whether vertical notes are included.
5. **MCP server.** Build it when a paying client needs one of the following:
   - read-only probes into their CRM, ERP or helpdesk (for example Jobber, Shopify, QuickBooks, Zendesk), because manual exports are blocking quarterly re-runs
   - the methodology in a host that can't run Skills or local scripts

   Sharing the JSON file across devices is not a trigger; a shared folder handles that. Start with the smallest server: a scoring tool wrapping `diagnose.py`, plus one read-only summary probe (counts and blank shares, never raw rows) for the client's actual software. Pin FastMCP 4.2.4 or newer, and check protocol details against official docs at that time.
6. **Interactive surface (MCP App).** Only after the MCP server exists and clients ask for it. Make it a scope and approver sign-off sheet (asks first, owner limits, approver, rollback), not weight sliders.

## Changes from the independent review (applied 2026-11-22)

The 2026-11-22 Gemini review ([reviews/2026-11-22-gemini-plan-review.md](reviews/2026-11-22-gemini-plan-review.md)) agreed with this plan and with deferring MCP. Its five fixes before the first real client are applied: runs without a quote, conflicting hours blocking Go, the local CSV profiler, trap tests plus a behaviour checklist, and chart scaling plus a next step to agenticworks.ca. Its roadmap changes are folded into the roadmap above.

## Open questions

- Is the evidence weighting (1.0 / 0.85 / 0.65 / 0.5) right? It needs real cases.
- Should Not worth it stay at "pays back within a year", or depend on the business?
- Pricing and packaging for Lite vs Pro.

## Review history

- 2026-11-22: Gemini 4 Neon High reviewed and polished the built Skill (18 fixes).
- 2026-11-22: Codex GPT-6.2-Astra reviewed and polished it. Most fixes were kept; Fraction math was dropped.
- 2026-11-22: Gemini 4 Neon High independently reviewed this plan against the blueprint. Verdict: agree, with five fixes, all since applied. It also verified the blueprint's technical claims. See [reviews/](reviews/).
