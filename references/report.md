# Diagnostic report and build brief

Produce two separate documents under `$HERMES_HOME/workspace/diagnostic/<business-slug>/`: `<YYYY-MM-DD>-owner-report.md` and `<YYYY-MM-DD>-build-brief.md`. Keep the input file beside them. The owner report starts as an unsent draft. The build brief, input, raw scorer output and client-specific implementation material stay with Agentic Works. This public repository holds blank templates only. Never commit completed briefs, reports, source records, credentials or internal pricing material.

## Owner report

Build the report from the allowed fields below, not by redacting the build brief. Use plain language, no em dashes, and say “AI employee” or “your assistant,” not the software underneath. Don't include prices, payback ceilings, net first-year value, cost charts, delivery dates, booking links, raw input or output, internal links, or a build recipe. That's also the boundary for the live interview, follow-up chat and anything the customer might paste into their own AI. Do not give their AI internal files or instructions and rely on a prompt to hide them.

### 1. The answer

In the owner's words, name the job to start with, the no-AI fix, or “not yet,” and why. If the case against a higher-ranked job won, say why. Explain the finding when asked rather than withholding it.

### 2. All scored jobs

| Job | Where it landed | Estimated first-year value before costs | Why |
|---|---|---|---|

Use the scorer's value as printed, not ROI or a savings promise. Use a dash or “not estimated” when the scorer has no value. Explain which inputs came from records and which are estimates; an export may confirm volume without confirming minutes or shares. If you show the value drivers, say which amounts are before evidence adjustments and explain the adjustment in plain words so the components don't appear to add up to the adjusted total. Don't recompute or round the figures yourself. For **Not AI**, give the concrete fix and point to verified help for the tool they already use, without a setup walkthrough. Mention significant unscored pains separately.

### 3. The recommended job

Include only for a recommended **Go** job. Describe the outcomes, what decisions stay with people, how staff can switch back the same day, the strongest argument against the recommendation and why it didn't win, and two or three things the owner could check after a pilot. Keep staff concerns anonymous. If a diagram helps, show the decision and hold points: an item needing approval stays on hold unless the approver agrees. Don't expose prompts, implementation steps, exact approval thresholds, tool wiring, field mappings or test cases.

### 4. Illustrative 90-day outline

Only for a recommended **Go** job. Use outcome milestones and decisions, not an implementation checklist or promised dates. Start with a small pilot; continue or expand only if the owner agrees after reviewing the results.

### 5. What would change the answer

Translate each blocker into the owner's language and name what would clear it. If a quote is the only blocker, say “Worth a closer look; needs a quote.” If there are additional blockers, name them too. Do not disclose the internal ceiling. If this is a no-AI or “not yet” answer, sections 1, 2, 5 and 6 can be brief.

### 6. Next step and send check

For an owner-prioritized Go job or one that only needs a quote, offer a short scoping conversation with Kamran at Agentic Works. Don't promise a pilot for a quote-only job. Otherwise give the next useful action the owner can take, and don't pitch work they didn't ask for. For requests for exact prompts or setup, offer to scope the build while still answering questions about findings, rationale and no-AI alternatives.

Run the owner draft through `humanizer`, then check it for leaked prompts, internal costs, raw output, technical build detail and internal links. Send only the owner report and only after Kamran explicitly approves the exact recipient(s) and final text. Never send or attach the build brief, input or raw output.

## Build brief (internal only)

Use this as the handoff to `strategy-call`. Include the business, date, owner report path, input path, recommended job or reason to stop, outcome, evidence level, first-year value, net first year (if scored), and the scorer's first-year break-even threshold (if printed, otherwise N/A). The threshold is a fit check for build plus a year of running costs, not a quote or a standalone build budget.

For a job worth scoping, record the client-specific assistant brief separately inside this document: duties it may do alone, the named approver, actions it must ask about and hold until approved, exact owner limits, prohibitions, tools and data mappings, tone, manual fallback and acceptance tests. Anything uncertain or not explicitly allowed requires approval. For a no-AI or “not yet” case, document the stop decision and what would change it rather than inventing an assistant design.

Record the AI tool they already pay for, data readiness and blockers, any CSV blank shares, owner and staff hours and scorer-reported gaps, unpriced benefits, other pains and the strongest case against the recommendation. Include the raw `--markdown` output, including the table, value breakdown and chart when present. Keep any comparison with `strategy-call` pricing internal; route commercial decisions to Kamran.
