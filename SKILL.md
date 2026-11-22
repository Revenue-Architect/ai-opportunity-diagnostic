---
name: ai-opportunity-diagnostic
description: Interview a small-business owner to decide whether an AI assistant would pay for itself, which jobs it could handle, and what it must ask about first. Use when an owner asks "where could AI save us time?" or "should we get an AI assistant?", or someone says "run an AI assessment", "audit our workflows for AI" or "map AI use cases", or a consultant wants to rank a client's AI opportunities before a pilot. Not for building or configuring the assistant, writing a general AI strategy, or reviewing code.
metadata:
  author: agenticworks.ca
  version: "0.1"
---

# AI opportunity diagnostic

The decision this serves: **should this business get an AI assistant now, and if so, which jobs does it take and which does it ask about first?** "Not yet" is a valid answer. Say it plainly when the numbers point there.

## Rules

- Ask **one question at a time**. Wait for the answer before the next one.
- Talk about time and money before AI. Do not suggest tools during intake.
- Never compute a value, total, ranking or outcome in prose. Put the facts in the input file and run the script. Quote its numbers as given.
- Every number has a source: an export, the owner, staff, or the implementer's quote. Never fill a gap with a guess. Ask for it, or say which job still needs it.

## Stages

1. **Intake.** Follow sections 1–3 of [references/interview.md](references/interview.md). Record each job in the input file as you go.
2. **No-AI check.** For each job, decide whether a plain rule, a setting in a tool they already use, or a simple webhook handles most of it. See [references/gates.md](references/gates.md). If so, name the fix. For every job that survives, finish section 4 of [references/interview.md](references/interview.md).
3. **Score.** Run:

   ```
   python scripts/diagnose.py <input.json> --markdown
   ```

   Use [assets/example-case.json](assets/example-case.json) for the input format. For estimates, omit `evidence`. The script uses `hours_claims` to distinguish one estimate, agreement and disagreement. It assigns **Not AI**, **Not worth it**, **Not ready** (with its blockers) or **Go**, ranks the Go jobs, and charts the scored jobs.
4. **Evidence.** Take the first three scored rows in the table, or all scored rows if there are fewer. Ask for 30 days of records for each (inquiries, bookings, invoices or orders). Count the items for that job and set `weekly_volume` to the count × 7 / 30. Mark that job's `evidence` as `"export"` only after updating its volume. If records are unavailable, keep the estimate and say so. Re-score once after this pass.
5. **Case against.** Write the strongest case for passing on the highest-ranked Go job. If it wins, explain why and consider the next Go job the same way. If none stands up, recommend "not yet".
6. **Report.** Fill [references/report.md](references/report.md).

If the business has no Go jobs, the report says so and lists what would change that (usually the Not ready blockers).

## Re-running

The client keeps the input file. Next quarter, confirm costs and owner limits, update volumes, and clear any export label if the new volume is an estimate. Run stages 3–6 again.
