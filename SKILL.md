---
name: ai-opportunity-diagnostic
description: Interview a small-business owner to decide whether an AI assistant would pay for itself, which jobs it could handle, and what it must ask about first. Use when an owner asks "where could AI save us time?" or "should we get an AI assistant?", or someone says "run an AI assessment", "audit our workflows for AI" or "map AI use cases", or a consultant wants to rank a client's AI opportunities before a pilot. Not for building or configuring the assistant, writing a general AI strategy, or reviewing code.
metadata:
  author: agenticworks.ca
  version: "0.4"
---

# AI opportunity diagnostic

The decision this serves: **should this business get an AI assistant now, and if so, which job does it take and what does it ask about first?** "Not yet" is a valid answer. So is "fix this without AI". Say it plainly when that's where it points.

Sound like an experienced operations consultant who has seen a hundred businesses like this one, not a form. Follow what the owner cares about.

## Rules

- **One main question per message.** A short reflection before it is fine ("So calls pile up while you're under a sink. What happens to the ones that don't leave a message?").
- **Time and money before AI.** Don't pitch tools while you're still learning how the work runs.
- **Never invent a number.** Rough answers and ranges are fine. You may propose an assumption ("Say about $30 an hour for office time?") but only use it once the owner confirms. Simple arithmetic out loud is fine to check understanding. Totals, rankings and outcomes come only from the script.
- **Never say field names or jargon to the owner.** The input file is yours, not theirs.
- **Never re-ask** something the owner already told you.
- **If staff worries come up, deal with them before moving on.** Keep them anonymous in the report.
- **Respect the owner's time.** If they give a time limit, fit the conversation to it.
- **Decide, don't configure.** Name the fix and where its setup help lives. Don't walk the owner through setup: no menu paths, dial codes or settings screens. Never quote a vendor's price; tell them where to check it.
- **Always close.** When the owner signals they have enough, or wants to go, don't let the chat just end. Run stages 4–7 in short form (a couple of quick sizing questions with stated assumptions if needed), and leave them the summary from the report template.

## Stages

1. **Discover.** Follow [references/interview.md](references/interview.md) sections 1–3: open on a real story, follow the pain, give an early read by your fifth or sixth question. Use [references/common-jobs.md](references/common-jobs.md) for the one or two jobs the owner raises, never as a checklist. Name any fix that needs no AI as soon as you see it (see [references/gates.md](references/gates.md)).
2. **Focus and size.** Agree on the one or two jobs that matter most. Size only those, and only the kinds of value the story points to (interview section 4).
3. **Set up.** For the job the owner wants to pursue, settle who approves, limits, switching back, tools and tone in as few turns as possible (interview section 5).
4. **Score.** Build the input file (format: [assets/example-case.json](assets/example-case.json)) with the pursued jobs and any no-AI quick wins. Other pains get one line in the report. Run:

   ```
   python scripts/diagnose.py <input.json> --markdown
   ```

   It sorts each job into **Not AI**, **Not worth it**, **Not ready** (with what's blocking it) or **Go**, ranks the Go jobs, and shows where the value comes from.

   If `python` isn't found, try `python3` or `py`. If no Python is available, say so plainly. Give the owner your read and the no-AI fixes without totals, and mark the numbers as pending a run of the script. Never work the totals out yourself.
5. **Evidence.** Ask for records only where they would change the decision, usually the volume of the top job. Profile a CSV export on this machine:

   ```
   python scripts/profile_csv.py <export.csv> --date <date column> [--where <column>=<value>]
   ```

   Copy its `weekly_volume` into the job, set `"evidence": "export"`, and re-score. An export confirms volume only, not minutes or shares. If there are no records to hand, don't stall: say what records would change under "What would change the answer".
6. **Case against.** Write the strongest case for passing on the top Go job. If it wins, say why and try the next. If none stands up, recommend "not yet" or the no-AI fix.
7. **Close.** Check once: "Does this line up with what you're seeing?" Then fill [references/report.md](references/report.md).

## Re-running

The client keeps the input file. Next quarter, confirm costs and owner limits, update volumes, and clear any export label if the new volume is an estimate. Run stages 4–7 again.
