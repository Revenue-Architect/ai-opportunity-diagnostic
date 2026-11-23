# Interview

A conversation, not a questionnaire. Aim for something useful by your fifth or sixth question and about twenty questions in all. Field names in `code` are for the input file only; never say them to the owner. Record shares and margins as decimals (40% is `0.4`).

## 1. Open (two questions at most)

- What the business does and roughly how many people work in it.
- Then the story: "What slips through the cracks, or eats your week, more than anything else?" Followed by: "Tell me about the last time that happened."

If the owner opens with an AI idea ("I want an AI receptionist that handles everything"), don't argue and don't ignore it. Test it on their real story: "Let's take last Tuesday's lunch rush. Walk me through what came in, and we'll see what an assistant could have done with each one."

## 2. Follow the pain

Trace that one case from start to finish: what came in, who touched it, where it waited, why, and what the customer experienced. Check what happens downstream: who acts on the result, and do they have time to?

Ask a follow-up when an answer is:
- **vague** ("a lot", "depends"): ask for last week, or a range
- **surprising**: ask how that came about
- **emotional** ("it drives me crazy"): ask what it costs them
- **a cause** ("nobody checks it after 4"): ask what happens then

"What happens then?" is the question that finds the cost: a lost job, a refund, an angry review, a late night. When the owner mentions money going out the door (returns, refunds, write-offs, lost jobs), ask roughly how much a year before moving on. It is often the biggest number in the conversation.

Use [common-jobs.md](common-jobs.md) for the job the owner is describing. It suggests the sharp follow-ups and the usual non-AI fixes. Don't walk through the other jobs in it.

## 3. Early read and one sweep

By your fifth or sixth question, say what you're hearing:
- the real bottleneck
- which parts an assistant could safely take
- which parts need a person or a process change
- any fix that needs no AI (name it now, see [gates.md](gates.md))

Tell them what's left: "A few quick questions and I'll give you a one-page summary with the numbers."

Then one sweep: "Besides that, is there anything else eating the week, or costing you money when it goes wrong?" Agree on the one or two jobs worth going deeper on. Note any other pains in a line for the report.

## 4. Size the focus jobs

Only for the one or two focus jobs, and only for the kinds of value the story points to. Use a typical week, never a busy week times 52. Note seasonal spikes in `noted_benefits`. Rough is fine; check it back out loud ("so about 2 hours a week?").

**Time back.** How many a week (`weekly_volume`), how many minutes of hands-on work each (`minutes_per_item`; leave out waiting), and how much of that an assistant would remove (`share_handled`).
- For drafted work, ask: "Once someone checks and sends the draft, how much of those minutes actually goes away?"
- If the owner does the job, ask what they'd do with the time back. Use a higher `hourly_value` than the staff rate only if all three hold:
  1. there's real unmet paying work
  2. the time comes back in usable blocks, not scattered minutes
  3. the rate is what they *keep* per billable hour after materials and travel, not what they charge

  Otherwise use the staff rate, and put "evenings back" in `noted_benefits`. Record why in `hourly_value_basis`.
- If someone else does the job, ask their weekly hours too, ideally separately (`hours_claims.owner`, `hours_claims.staff`). When the script flags a gap, treat it as a finding: what is each person counting? Update the claims only when both agree on the same scope. Report it without blaming anyone.
- The business-wide hourly cost of staff time (wage plus overhead) is `loaded_hourly_cost`. Propose a figure from what they pay and let them correct it.

**Revenue won or kept.** If slow or missed work loses sales: roughly how much a year (`recovered_revenue_annual`), what share of each sale is left after the cost of doing the work (`gross_margin`), and what share an assistant could realistically win back (`recapture_rate`).

**Money not lost.** Write-offs, refunds, chargebacks, scrapped parts, costly mistakes: roughly how much is actually lost a year (`losses_avoided_annual`), and what share the assistant would prevent (`share_avoided`). Use cash actually lost, not list price.

**Noted, not priced.** Anything else that matters to them in their own words: faster replies, reviews, staff stress, evenings back (`noted_benefits`). These are reported, never added to the dollars.

If a kind of value clearly applies but the owner can't estimate it, don't push. Record it in `unpriced_drivers` with the reason (for example `{"revenue": "owner couldn't say how many callers hang up"}`). If records back a money figure, set `money_evidence` to `"records"`.

**Don't count the same money twice:**
1. If the owner's time is priced at a billable rate, don't also count revenue that would need those same hours.
2. Rework counted in minutes isn't counted again in money not lost.
3. A botched order counts as revenue or as money not lost, never both.

Saving labour and winning sales on the same queue are different things, and both count.

## 5. Set up the job they want to pursue

Only for the job the owner wants to go ahead with. Keep it to a few turns.

1. **What it does on its own and where a person takes over.** These are the specific steps.
2. **For draft-only work, confirm the defaults in one go:** "So it drafts, [approver] checks and sends, nothing goes out on its own, and if it's not working you just stop using it. Anything it should never touch?" This settles `approver`, `on_own_is_reversible`, `rollback` and the never list.
3. **If money moves or the business commits to something,** those steps go in `asks_first`. Ask whether the owner wants to approve every one, or set a limit they choose (`owner_limits`, see [gates.md](gates.md)). Skip this when no money moves.
4. **Which tools and records it would work in** (`tools_needed`), and whether it can use them as they are (`data_ready`, `data_blocker`).
5. **How the business talks to customers, or how internal notes should read** (tone, for the brief).
6. **Which AI tool, if any, the business already pays for** (`ai_tool`, or `"none"`).

Build and run costs (`build_cost`, `monthly_run_cost`) come from the implementer's quote, not from the owner. With no quote yet, leave both out.

In self-serve mode, with no staff present and no records to hand, don't stall. Say what a staff check or records would change, and carry on.
