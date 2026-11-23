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
- Owner limits: money actions ask first by default. The owner may let one run on its own up to an amount they name.
- `scripts/test_diagnose.py` holds plain-assert checks on a made-up example business.

## How v1 differs from the blueprint, and why

| Blueprint | v1 | Why |
|---|---|---|
| 5-axis weighted composite (30/25/20/15/10) with 1–5 ratings | Value at margin × evidence weight | The model picks the 1–5 ratings, so the composite is precise arithmetic on guesses. Dollars can be checked against reality. |
| Nine classifications | Four outcomes | Every blueprint bucket maps onto Not AI, Not worth it, Not ready or Go. |
| Revenue counted as drag (e.g. $170,400) | Revenue × margin × recapture | Recovered revenue is not profit. |
| Exec-vs-frontline delta with 4 evidence tiers | Same idea, simpler: export / agree / single estimate / conflicting | Kept the insight and dropped the extra flags. |
| Four mandatory diagrams | Quadrant chart (generated), before/after flow for the chosen job, roadmap table | Enough to support the decision. |
| Single approver, forbidden actions, rollback | Approver, asks-first, owner limits, rollback, Never list | Matches "asks before money moves". |
| 5 synthetic trap fixtures | 1 made-up example; real cases to be added | Fixtures should come from real diagnostics. |
| Remote MCP server, state store, auth, Skills over MCP, ui:// workbench, dual-era elicitation | Not built | See the roadmap triggers below. |
| Lite / Pro split | Not built | No vertical packs exist yet, so there is nothing to split. |

## Roadmap

Each step starts when its trigger happens, not by calendar.

1. **First real diagnostics (next).** Run the Skill with 2–3 real businesses. Save each anonymized input file as a test case. Calibrate `CLAIM_GAP_LIMIT` and `EVIDENCE_WEIGHT` against what the exports show.
2. **Day-30 check on each Go pilot.** Compare predicted weekly volume and hours back against the assistant's real logs. Change the interview or weights where predictions miss.
3. **Vertical notes.** Add `references/verticals/<vertical>.md` after the first real client in that vertical. The trades and e-commerce lists in the blueprint are the starting candidates.
4. **Lite / Pro split.** Do this once a vertical note exists that is worth charging for. A build flag on the same folder decides whether vertical notes are included.
5. **MCP server.** Build it when a paying client needs one of the following:
   - audit state across sessions or devices beyond the JSON file
   - read-only probes into their CRM, ERP or helpdesk
   - the methodology in a host that can't run Skills

   Start with the smallest server that meets that need. Check every version and protocol claim from the blueprint against official docs first.
6. **Interactive workbench (MCP App).** Only after the MCP server exists and clients ask to adjust results themselves.

## Proposed changes from the independent review (awaiting Kamran's decision)

The 2026-11-22 Gemini review ([reviews/2026-11-22-gemini-plan-review.md](reviews/2026-11-22-gemini-plan-review.md)) agrees with this plan and with deferring MCP. It proposes a "Step 0" before the first real client or a public release. Claude's view is noted on each item.

1. **Self-serve without a quote.** The script requires `build_cost` and `monthly_run_cost`, which only the implementer can supply, so an owner running it alone stalls. Proposal: when costs are missing, report the most a build could cost and still pay back in year one, and point to agenticworks.ca for a quote. *Claude: agree. It's small and needed for a lead magnet.*
2. **Conflicting owner/staff hours should not reach Go.** The example's invoice chasing has a 50% gap and still ranks #2. Proposal: a conflicting gap becomes a Not ready blocker until records settle it. *Claude: agree. It's simpler than discounting by 0.5 and fixes the double discount Gemini points out.*
3. **Local CSV profiler.** Stage 4 asks the model to count records and divide in prose, which breaks the no-math-in-prose rule. Proposal: a small stdlib `scripts/profile_csv.py` (row count, date span, weekly volume, blank rate per column). *Claude: agree.*
4. **Trap fixtures and behaviour checks.** Add the blueprint's five trap cases plus a "not yet" case as script tests, and a short manual checklist for agent behaviour (one question at a time, pushes back on rule-based jobs, triggers correctly). *Claude: agree on fixtures; keep the behaviour check a short manual checklist.*
5. **Small fixes.** Quadrant x-axis scaling for one or two jobs, and a one-line next step to agenticworks.ca in the report. *Claude: agree.*

Roadmap changes it proposes:
- Don't tune `EVIDENCE_WEIGHT` or `CLAIM_GAP_LIMIT` until about 10 diagnostics; use the first 2–3 to fix the interview.
- Draft vertical notes after client #1, but split Lite/Pro only after 3–5 clients in one vertical and evidence that owners will pay for the Skill itself.
- Drop "audit state across devices" as an MCP trigger, since a shared folder handles that.
- If a UI is ever built, make it a scope and approver sign-off sheet, not weight sliders.

*Claude: agree with all four.* None of these are applied yet.

## Open questions

- Is the evidence weighting (1.0 / 0.85 / 0.65 / 0.5) right? It needs real cases.
- Should Not worth it stay at "pays back within a year", or depend on the business?
- Pricing and packaging for Lite vs Pro.

## Review history

- 2026-11-22: Gemini 4 Neon High reviewed and polished the built Skill (18 fixes).
- 2026-11-22: Codex GPT-6.2-Astra reviewed and polished it. Most fixes were kept; Fraction math was dropped.
- 2026-11-22: Gemini 4 Neon High independently reviewed this plan against the blueprint. Verdict: agree, with the changes above. It also verified the blueprint's technical claims. See [reviews/](reviews/).
