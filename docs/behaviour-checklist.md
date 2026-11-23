# Behaviour checklist

The script tests cover the math. This checklist covers what only a live agent can show. Run it by hand in a fresh session whenever `SKILL.md` or a reference file changes, in each agent you care about (Claude, Codex, Cursor). Use a test session, never a real client chat.

## Triggering

| Prompt | Expected |
|---|---|
| "Where could AI save my plumbing business time?" | Skill loads |
| "Run an AI assessment for my clinic" | Skill loads |
| "Should we get an AI assistant for our store?" | Skill loads |
| "Write our company's AI strategy deck" | Skill does not load |
| "Review this Python function for bugs" | Skill does not load |
| "Set up the AI assistant we scoped last week" | Skill does not load |

## Interview behaviour

Start with "Should my HVAC company get an AI assistant?" and play the owner.

- [ ] Asks one question per message, including follow-ups.
- [ ] Asks about time and money before mentioning AI or tools.
- [ ] Questions a weekly-hours claim that doesn't match volume × minutes.
- [ ] Says "we want AI to tag orders by SKU prefix" is a plain rule (Not AI) and names the rule.
- [ ] Refuses to let refunds run with no approval unless you name a limit yourself, and never suggests an amount.
- [ ] Runs `scripts/diagnose.py` rather than adding up numbers in its reply.
- [ ] With no quote, marks jobs Not ready with the most a build could cost, and does not invent a quote.
- [ ] Offers `scripts/profile_csv.py` when given an export, and doesn't count rows by eye.
- [ ] Writes a case against the top Go job before recommending it.
- [ ] Ends the report with the agenticworks.ca next step.

Write down any miss with the prompt that caused it. Fix the instruction where that fact lives, then re-run the checklist.
