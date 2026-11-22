---
name: ai-opportunity-diagnostic
description: Interview a small-business owner about where hours and money go, filter out jobs that need no AI, and decide whether an AI assistant is worth setting up now, which jobs it takes on, and what it must ask about first. Use when someone says "run an AI assessment", "where could AI help my business", "audit our workflows for AI", "should we get an AI assistant", "map AI use cases", or "prioritize automation projects". Not for building or configuring the assistant itself, writing a general AI strategy, or reviewing code.
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
- Every number has a source: an export, the owner, staff, or the implementer's quote. Never fill a gap with a guess; ask, or leave the field out.

## Stages

1. **Intake.** Follow sections 1–3 of [references/interview.md](references/interview.md). Record each job in the input file as you go.
2. **No-AI check.** For each job, decide whether a plain rule, a setting in a tool they already use, or a simple webhook handles most of it. See [references/gates.md](references/gates.md). If so, name the fix. For every job that survives, finish section 4 of [references/interview.md](references/interview.md).
3. **Score.** Run:

   ```
   python scripts/diagnose.py <input.json> --markdown
   ```

   The input format is [assets/example-case.json](assets/example-case.json). The script sorts each job into **Not AI**, **Not worth it**, **Not ready** (with its blockers) or **Go**, ranks the Go jobs, and prints a Mermaid quadrant chart.
4. **Evidence.** For the top three jobs by value in the script output (excluding Not AI), ask for 30 days of real records (an inbox or ticket count, booking calendar, invoice aging, order or refund list). Count `weekly_volume` from the records yourself, update the input file, set `"evidence": "export"`, and re-run stage 3.
5. **Case against.** Before recommending the top Go job, write the strongest case for *not* using AI on it. If that case wins, say so and recommend the next job or "not yet".
6. **Report.** Fill [references/report.md](references/report.md).

If the business has no Go jobs, the report says so and lists what would change that (usually the Not ready blockers).

## Re-running

The input file is the audit. Keep it with the client. Re-running next quarter means updating volumes and evidence in the same file and running stage 3 again.
