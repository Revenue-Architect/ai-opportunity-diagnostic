# Behaviour checklist

The script tests cover the math. This checklist covers what only a live agent can show. Run it by hand in a fresh test session, never a real client chat, whenever `SKILL.md` or a reference file changes. Do it in each agent you care about (Claude, Codex, Cursor). The isolated roleplay in [v0.4-spec.md](v0.4-spec.md) section 6 is the fuller version.

## Triggering

| Prompt | Expected |
|---|---|
| "Where could AI save my plumbing business time?" | Skill loads |
| "Run an AI assessment for my clinic" | Skill loads |
| "Should we get an AI assistant for our store?" | Skill loads |
| "Write our company's AI strategy deck" | Skill does not load |
| "Review this Python function for bugs" | Skill does not load |
| "Set up the AI assistant we scoped last week" | Skill does not load |

## Conversation

Start with "Should my HVAC company get an AI assistant?" and play a busy owner who gives vague answers.

- [ ] Opens with at most two context questions, then asks for a real recent story.
- [ ] Follows up on vague, surprising or emotional answers instead of moving to the next topic.
- [ ] Gives a business-specific early read (the bottleneck, a no-AI fix) by its fifth or sixth question.
- [ ] Asks about only one or two focus jobs in detail, and about 20 questions or fewer in all.
- [ ] Proposes rough assumptions for you to confirm, rather than asking for figures you can't know.
- [ ] Never says field names such as `share_handled`.
- [ ] Says "AI to tag orders by SKU prefix" is a plain rule (Not AI) and names the rule.
- [ ] Tests "I want it to handle everything" on a real example rather than agreeing or ignoring it.
- [ ] Stops to address a staff worry when you raise one.
- [ ] Doesn't let refunds run without approval unless you name a limit yourself, and never suggests an amount.
- [ ] Runs `scripts/diagnose.py` for totals and outcomes, and `scripts/profile_csv.py` for any export.
- [ ] Checks "does this line up with what you're seeing?" before the report.
- [ ] Answers the problem you came with, and ends with a next step you'd actually take.

Write down any miss with the prompt that caused it. Fix the instruction where that fact lives, then re-run the checklist.
