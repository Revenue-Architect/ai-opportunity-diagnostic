# Judgment calls behind the gates

The script applies the gates and owns every threshold (see the constants at the top of [scripts/diagnose.py](../scripts/diagnose.py)). This file covers only the yes/no calls you make when filling in the input.

## `rule_covers_most`: does this need AI at all?

Set it to `true` when most of the job's cases follow fixed logic that needs no reading of free text, audio or images. Examples: route an order by SKU or region, send a reminder 24 hours before a booking, tag a customer by spend, sync a record between two systems. Then fill `rule_fix` with the specific rule, tool setting or webhook that would do it.

Set it to `false` when the job depends on understanding messages, documents, calls or photos, or on judgment that changes case by case.

When in doubt, write the rule out. If you can't write it in a few lines, it's probably `false`.

## `data_ready`: can the assistant work from the records?

`false` when the information it needs is missing, scattered across places with no access, or too messy to act on (for example, many blank job types or free-text part numbers). Fill `data_blocker` with what is missing or unusable.

## `on_own_is_reversible`: is everything it does alone easy to undo?

`true` only if every action outside `asks_first` can be undone cheaply: a draft, a reply, a reschedule, a reminder. Refunds, payments, cancelled orders, binding quotes and anything that affects safety belong in `asks_first`. If they can't go there, set this to `false`.

The one exception is an owner limit: the owner may let a money action run on its own up to an amount they choose (for example, refunds up to $50). Record it in `owner_limits`. Actions inside an owner limit are the owner's accepted risk and don't make this `false`; anything above the limit stays in `asks_first`. Never suggest a limit yourself; the owner names the amount.

## `evidence`

`"export"` once you have updated `weekly_volume` from real records. Otherwise leave it out; the script works out the evidence level from `hours_claims`.
