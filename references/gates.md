# Judgment calls behind the gates

The script applies the gates and owns the thresholds. Use these questions to record the owner's answers.

`done_by`, `asks_first` and `owner_limits` are for the audit and report. The script reads your answer to `on_own_is_reversible` directly.

## `rule_covers_most`: does this need AI at all?

Set it to `true` when most of the job's cases follow fixed logic that needs no reading of free text, audio or images. Examples: route an order by SKU or region, send a reminder 24 hours before a booking, tag a customer by spend, sync a record between two systems. Then fill `rule_fix` with the specific rule, tool setting or webhook that would do it.

Set it to `false` when the job depends on understanding messages, documents, calls or photos, or on judgment that changes case by case.

When in doubt, write the rule out. If you can't write it in a few lines, it's probably `false`.

## `data_ready`: can the assistant work from the records?

`false` when the information it needs is missing, scattered across places with no access, or too messy to act on (for example, many blank job types or free-text part numbers). Fill `data_blocker` with what is missing or unusable.

## `on_own_is_reversible`: is everything it does alone easy to undo?

By default, put every money-moving or irreversible step in `asks_first`, along with binding commitments and safety decisions. Drafting a reply is easy to undo. A customer may already have acted on a sent reply.

Only the owner can make an exception for a specific money action. Record the action and the amount they name in `owner_limits`. In `asks_first`, list that action only above the limit. Set `on_own_is_reversible` to `true` if every other step the assistant takes on its own is easy to undo. Otherwise set it to `false`.
