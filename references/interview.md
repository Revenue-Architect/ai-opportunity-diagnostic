# Interview

Ask one question per message, including follow-ups. Give each job a name and a unique `id`. For shares and margins, record a percentage like 40% as `0.4`.

## 1. Context

- What the business does, how many people, which tools it runs on (email, calendar, booking, invoicing, CRM or store).
- What a fully loaded hour of staff time costs them (wage plus overhead). This is `loaded_hourly_cost`. If they don't know, ask for the hourly wage and the rough overhead on top.

## 2. Walk the week, job by job

Go through these areas in order and skip any that don't apply: new inquiries and leads, booking and scheduling, quotes and estimates, doing and delivering the work, customer questions and support, invoicing and collections, back-office admin.

For each job that takes real time, ask, one at a time:

1. Who does it? (`done_by`)
2. How many times a week? (`weekly_volume`)
3. How many minutes does someone spend working on one? (`minutes_per_item`; leave out time spent waiting for a reply.)
4. How often does someone have to redo it? Ask what that costs. Count the extra work once, in the volume or the time per item. Follow up on lost sales below and on steps that need approval in section 4.
5. When this job runs late or gets missed, do you lose sales? If yes, ask how much revenue is lost in a year, before allowing for what the assistant might win back (`recovered_revenue_annual`). Then ask what share of each sale is left after the cost of doing the work (`gross_margin`). Leave the revenue fields out if there is no lost revenue.

Ask the owner for their weekly hours estimate before sharing the calculation. Record their answer in `hours_claims.owner` if they know. If they say ten hours but 30 items × 5 minutes comes to 2.5 hours, ask what explains the difference.

## 3. A second view

If someone else does the job, ask for their weekly hours estimate too, ideally in a separate short conversation. Record it in `hours_claims.staff`. When the script flags a big gap, treat it as a finding and ask what explains it. Report it without blaming either person.

## 4. For each job that survives the No-AI check

1. What share of these could an assistant fully handle, the way a capable new hire would? (`share_handled`)
2. If the job loses revenue, what share of that lost revenue could an assistant realistically win back? (`recapture_rate`)
3. Which steps should wait for someone's say-so? Prompt for money, commitments, safety, and anything they can't undo. For a money step, ask whether they want to approve it every time. If they want a limit, ask what amount they choose. Record `asks_first` and `owner_limits` as described in the gates reference.
4. Apart from any money action within the limit you set, could you easily undo everything the assistant would do on its own? (`on_own_is_reversible`: yes is `true`.)
5. Who is the one person who owns this job and approves any asks-first items? (`approver`)
6. If the assistant misbehaves, how do you switch back to the old way the same day? (`rollback`)
7. Where do you keep the records? Then ask whether the assistant can get to them and use them as they are (`data_ready`). If the answer is no, ask what's missing (`data_blocker`).

Build and run costs (`build_cost`, `monthly_run_cost`) come from the implementer's quote, not from the owner.
