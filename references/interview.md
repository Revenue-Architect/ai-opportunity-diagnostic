# Interview

One question per message. Plain words, no jargon. Field names in `code` are the input-file fields from [assets/example-case.json](../assets/example-case.json).

## 1. Context (two or three questions)

- What the business does, how many people, which tools it runs on (email, calendar, booking, invoicing, CRM or store).
- What a fully loaded hour of staff time costs them (wage plus overhead). This is `loaded_hourly_cost`. If they don't know, ask for the hourly wage and the rough overhead on top.

## 2. Walk the week, job by job

Go through these areas in order and skip any that don't apply: new inquiries and leads, booking and scheduling, quotes and estimates, doing and delivering the work, customer questions and support, invoicing and collections, back-office admin.

For each job that takes real time, ask, one at a time:

1. Who does it? (`done_by`)
2. How many times a week? (`weekly_volume`)
3. How long does one take, start to finish? (`minutes_per_item`)
4. How often does it go wrong or need redoing, and what does that cost? (Fold rework time into `weekly_volume` or `minutes_per_item`, lost sales into question 5, and costly mistakes into `asks_first`.)
5. Does it lose sales or revenue when it's slow or missed? (missed calls, unpaid invoices, lost quotes) If yes, ask roughly how much revenue a year (`recovered_revenue_annual`) and, next, their gross margin on that work (`gross_margin`).

Check every hours claim against volume × minutes. If the owner says "ten hours a week" but 30 items × 5 minutes is 2.5 hours, ask which number is right. Record the owner's weekly hours claim in `hours_claims.owner`.

## 3. A second view

If someone else does the job, ask for their weekly hours estimate too, ideally in a separate short conversation. Record it in `hours_claims.staff`. When the script flags a big gap, treat it as a finding and ask what explains it. Report it without blaming either person.

## 4. For each job that survives the No-AI check

1. What share of these could an assistant fully handle, the way a capable new hire would? (`share_handled`)
2. If the job loses revenue, what share of that lost revenue could an assistant realistically win back? (`recapture_rate`)
3. Which steps move money, commit the business, or can't be undone? Those go in `asks_first`. Then ask whether small ones may go through without asking; if the owner names an amount, record it in `owner_limits`.
4. Can everything the assistant does on its own be undone easily? (`on_own_is_reversible`)
5. Who is the one person who owns this job and approves any asks-first items? (`approver`)
6. If the assistant misbehaves, how do you switch back to the old way the same day? (`rollback`)
7. Where do the records live, and are they complete enough to work from? (`data_ready`, `data_blocker`)

Build and run costs (`build_cost`, `monthly_run_cost`) come from the implementer's quote, not from the owner.
