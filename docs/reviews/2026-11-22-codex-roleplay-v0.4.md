# Isolated roleplay test of v0.4 (Codex GPT-6.2-Sol, 2026-11-22)

Each run used two separate Codex sessions relayed turn by turn:
- **Agent:** saw only the Skill.
- **Owner:** saw only a hidden persona brief, never the Skill, spec or pass criteria.

Personas:
- Dana (plumbing) and Priya (physio clinic), as in the v0.2 test
- Marco, an unseen holdout running a small online bike-parts store

## Results

| | v0.2 (self-played) | v0.4 round 1 | v0.4 round 2 (final) |
|---|---|---|---|
| Agent messages, Dana / Priya / Marco | 37 / 34 / – | 13 / 14 / 7 | 7 / 14 / 14 |
| First useful advice (agent message) | 26 / 24 / – | 4 / 4 / 4 | 2 / 3 / 4 |
| Owner's own problem addressed | no / no / – | yes / partly / yes | yes / yes / yes |
| Owner left with a step they'd take | no / yes / – | yes / yes / yes | yes / yes / yes |

**Against the pass criteria** ([../v0.4-spec.md](../v0.4-spec.md)):
- **1–4 pass for all three owners.**
- **5 passes in part.** No jargon was spoken, and Priya's staff worry was handled with a no-names tally. The script could not run, because `python` is not on the PATH in Codex's sandboxed shell on this machine. The agent tried it each time and correctly did not invent totals. v0.4 now tells the agent to try `python3` or `py`, and to mark numbers as pending if no Python exists.
- **6 passes:** 27 checks.

**Round 1 found three issues, fixed before round 2:**
- The agent never closed or summarized.
- It drifted into setup steps (menu paths, carrier dial codes, a vendor's price).
- It missed Marco's biggest cost (wrong-fit returns).

Round 2 asked what returns cost ($6k a year, a third preventable) and recommended a product-page fix over a chatbot. Setup detail dropped to one vendor link.

**Not covered:**
- The owner-time guardrail was not stress-tested. Marco's "evenings back" was correctly kept as a noted benefit, not priced.
- The full written report and the assistant brief were not exercised, because no owner reached a Go job. In each run, "not yet" or a no-AI fix was the honest answer.

**Harness limit:** the harness stopped when the owner said goodbye, so each agent's closing turn was run afterwards and is appended to its transcript. All transcripts below are round 2.

## Dana

**Owner:** Hi. Someone told me to try this. I run a small plumbing and heating outfit. Is AI actually going to help me or is this a waste of time?

**Agent:** It could help. I’d look at where you’re losing time or jobs before spending anything on AI.

Thinking back over the last week, what’s one thing that slipped through the cracks or took longer than it should have?

**Owner:** The phone, for sure. When I’m on a job it goes to voicemail, and by the time I call back at the end of the day, some people have already found someone. And I have no idea how many just hang up.

**Agent:** If someone can return calls while you’re on a job, that may solve a lot of this on its own. Who, if anyone, is free to call customers back during the day?

**Owner:** Nobody, really. The techs are on jobs and my bookkeeper’s only part-time. It’s just me calling people back when I get a break or at the end of the day.

**Agent:** An automatic text when you miss a call would give people a way to tell you what they need, even if they hang up without leaving a voicemail.

Just counting the callers who told you they’d already hired someone else, roughly how much work do you think you lose that way in a year?

**Owner:** I honestly have no idea. I hear “we already found someone” more often when it first gets cold, but I don’t keep track. The text sounds useful, though. What would it actually say?

**Agent:** “Hi, it’s [Business Name]. Thanks for calling. Text me your name, what town you’re in, and what you need help with. I’ll get back to you as soon as I can.”

On a busy day, could you answer a quick text sooner than you could return a call?

**Owner:** Yeah, I could usually answer a text between jobs. A call can turn into ten minutes, and sometimes all I need to know is where they are and what’s wrong. Would the replies come to the phone I already use?

**Agent:** Yes, if your business number can receive texts. Depending on how the line is set up, replies could come to your regular Messages app or your phone provider’s app on the same phone.

Since you can answer texts between jobs, I’d start with the automatic reply. It can ask for the two details you need to decide what to do next.

Do customers call your cell number directly, or do they call a separate business number?

**Owner:** They call my cell directly. It’s the number on the vans. Can I set up the auto-text without changing that number?

**Agent:** Yes, you can often keep the number on the vans. I’d check with your cell carrier first to see if it can send an automatic text when a call goes unanswered.

Another option is to move the same number to a business phone service that offers missed-call texts. Customers would still dial the number on the vans, and you’d get calls and texts through an app on the phone you already carry. [See how that works](https://www.quo.com/features/business-sms-mms).

Who’s your cell carrier?

**Owner:** Rogers. I’d rather keep the number where it is if I can. What exactly should I ask them for?

**Agent:** I’d ask Rogers Wireless support for an **automatic text after a missed call**. You can use this wording.

> Can my current Rogers cell line automatically text someone when I miss their call, even if they hang up without leaving a voicemail? I want the text to come from the number I already have, with replies coming into my regular texting app. Can Rogers do that on my current line?

**Owner:** Okay, I can ask Rogers that. If they can do it on my line, I’ll try it. That’s what I needed. [END]

**Agent (closing turn, added after the harness stopped):** If Rogers can do it on your current line, I’d start with the standard missed-call text. You can reply between jobs, and you’ll already know where the caller is and what they need.

During the first busy week you try it, keep a quick tally of how many text replies turn into booked jobs. That’ll give you something concrete to go on.

## Priya

**Owner:** Hi! We're a physio clinic and I really want to set up an AI receptionist that can handle everything for us. Where do we start?

**Agent:** Think back to the last time you wished you had an extra person at the front desk. What happened?

**Owner:** Yesterday at lunch we were checking people in and the phone kept ringing. A couple of calls went to voicemail, and by the time we got to them we also had emails from people trying to move their appointments. We had a same-day cancellation and never got anyone into that slot.

**Agent:** When you got to the voicemails, what were people calling about?

**Owner:** One person wanted to move their appointment, and the other asked if their insurance would cover physio. By the time we called back, we got voicemail ourselves for one of them.

**Agent:** What happened with the caller who didn’t pick up when you called back?

**Owner:** We left a message. I don’t think they’d called back by the end of the day.

**Agent:** What did your team do when that same-day slot opened up?

**Owner:** We called a couple of people we knew were looking for an earlier appointment. Neither could make it on short notice, and then we got busy at the desk again. The slot stayed empty.

**Agent:** A text to patients waiting for an earlier appointment could save your team from calling people one at a time. An AI assistant could draft replies to rescheduling requests and pass insurance questions to your team.

In a typical week, would quicker replies or filling last-minute openings make a bigger difference?

**Owner:** Quicker replies, I think. We get behind on calls and emails most days, so I’d start there. I’d want the team to see how it helps them before we add anything else.

**Agent:** Your team could check and send the drafted replies during a small trial so they can see whether it saves them time. In a typical week, roughly how many calls and emails do they have to catch up on later?

**Owner:** The shared inbox gets about 30 to 40 emails a week. I don’t know how many we have to come back to later, and I don’t have a count for missed calls. Lunch and first thing in the morning are when the phone’s hardest to keep up with.

**Agent:** Of those 30 to 40 emails, roughly how many are about booking or moving an appointment?

**Owner:** Maybe half? That’s a guess. I can pull a list from the shared inbox later if that would help.

**Agent:** That’s enough for a rough estimate. About how many minutes does your team spend on a typical booking or rescheduling email, including checking the schedule and replying?

**Owner:** Probably 5 to 8 minutes, if they can get through it in one go. I’m happy to give you a ballpark, but I don’t want the team to feel like I’m timing them.

**Agent:** We can use your estimate and ask the team whether the drafts make their work easier. If they still check the schedule and send each reply, about how many minutes do you think a draft would save per email?

**Owner:** Maybe a minute or two? They’d still have to check Jane for openings, and that’s usually the part that takes longest.

**Agent:** If patients can see available times themselves, that could save your team some of those schedule checks. Can patients already book or move appointments online through Jane?

**Owner:** They can book online through Jane. I’m not sure if they can move an existing appointment themselves. We still get quite a few emails asking us to do it.

**Agent:** I’d check whether online rescheduling is turned on in Jane. Patients can move their own appointments when it’s enabled and they give enough notice under your clinic’s policy. [Jane’s guide to online rescheduling](https://jane.app/guide/cancellation-policy)

How much notice do patients usually give when they email to move an appointment?

**Owner:** It varies. Some give us a day or two, and some email the morning of. I don’t know which is more common offhand.

**Agent:** If online rescheduling is on, your team could use a saved reply with the Jane link for patients who give enough notice. What usually happens when a patient has to wait for a reply about moving an appointment?

**Owner:** Usually they call to make sure we saw the email, especially if the appointment is that day. Then we’ve got a voicemail and an email about the same appointment. I can check the Jane setting. What would you start with for the phone at lunch?

**Agent:** I’d start with one person handling the lunch voicemails and checking the shared inbox before calling back. That way, an email and a voicemail about the same appointment get handled together. You can give callers a callback window in the greeting once you know what the team can manage.

When could someone reliably start returning those calls?

**Owner:** Probably around 1:30, once the lunch rush settles down. Some days check-ins run long, so I’d be more comfortable saying we’ll call back by 2.

**Agent:** I’d use “We’ll call you back by 2 p.m.” in the lunch greeting. Starting callbacks around 1:30 gives the team some room when check-ins run long.

Who could take the lunch callbacks each day?

**Owner:** The two of them could take turns, depending on who’s covering check-ins. I can ask what works for them and try it for a week. Between that and checking the Jane setting, I’ve got enough to get started. [END]

**Agent (closing turn, added after the harness stopped):** I’d start with the one-week trial and hold off on the AI receptionist for now.

- **Lunch calls.** Let the two team members decide who takes callbacks each day. Start around 1:30, check the shared inbox for messages about the same appointment, and use 2 p.m. as the callback promise.
- **Rescheduling emails.** Check whether patients can move appointments online in Jane. If they can, give the team a saved reply with the link for patients who give enough notice. [Jane’s guide to online rescheduling](https://jane.app/guide/cancellation-policy)

After a week, ask the team whether the callback window worked and whether they spent less time following up twice on the same request. If the inbox still backs up, a count of booking and rescheduling emails would help decide whether AI drafts are worth trying. Your estimate was a minute or two saved per draft, with most of the work going into checking the schedule.

Does that line up with what you want to try?

## Marco

**Owner:** Hey, I run a small online bike parts shop. I keep hearing I should get an AI chatbot. Is that worth it for a shop my size?

**Agent:** A chatbot could be worth it if customer questions take up a lot of your time or slow replies are costing you sales. Can you walk me through the last customer question that took a while to sort out?

**Owner:** Yeah, last night someone asked if a rear derailleur would fit their bike. They knew the bike model but had bought it used, so I had to ask for a photo of what was actually on it. Once they sent it, I still had to dig through the supplier’s spec sheet before I could tell them what to order.

**Agent:** Once you had the photo, roughly how long did it take to check the specs and reply?

**Owner:** Maybe 15 minutes? The supplier had two versions on the same spec sheet, so I spent most of that figuring out which one I was looking at.

**Agent:** What finally tipped you off to which version it was?

**Owner:** I zoomed in on the photo and could just about read the model number stamped on the derailleur. That matched one of the two versions on the sheet.

**Agent:** For this kind of question, I’d ask for a close-up of the stamped model number up front and keep a short list that matches each number to its version. How often do you get fit questions that take this much digging?

**Owner:** The ones where I have to dig through a spec sheet? Maybe two or three a week. Fit questions come in pretty much every day, but a lot of them are quicker. Asking for that close-up first would save some back-and-forth.

**Agent:** I’d start with a saved reply asking for the close-up and a short model-number lookup. An assistant could draft routine replies. When the stamp is hard to read, you’d still need to check the part against the specs.

Besides fit questions, is there anything else that regularly eats up your time or costs the shop money?

**Owner:** “Where’s my order?” emails are a daily thing. And when someone orders a part that doesn’t fit, I pay the return shipping and sometimes can’t resell the part. We also get the odd chargeback from someone saying their order never arrived, even though tracking says it was delivered.

**Agent:** For the daily order emails, I’d make the tracking link easy to spot in the shipping confirmation.

Over the past year, roughly how much did wrong-fit returns cost you, counting return postage and what you paid for parts you couldn’t resell?

**Owner:** Maybe $6,000 over the year? That’s a guess. I don’t track the postage and the parts I can’t resell separately.

**Agent:** A rough total is fine for now. Thinking back to the last few wrong-fit returns, what led customers to pick the wrong part?

**Owner:** One guy ordered the 12-speed version when his bike was 11-speed. Another went by the bike model, but it was used and the previous owner had swapped some parts. The two versions look almost identical in the photos, so I can see how people get them mixed up.

**Agent:** I’d show “11-speed” or “12-speed” right where shoppers pick a version, with a note for used-bike owners to check the model number on the part that’s actually on their bike.

Roughly what share of your wrong-fit returns do you think those checks could have prevented?

**Owner:** Maybe a third? Total guess. I can think of a few where putting “11-speed” right in the dropdown would’ve helped. So would you put that ahead of the chatbot?

**Agent:** Yes. I’d put “11-speed” and “12-speed” in the dropdown first. That helps shoppers choose the right version even if they never message you. I’d put the note about checking the stamped model number next to the dropdown, too.

For those daily “Where’s my order?” emails, do your shipping confirmations already include a tracking link?

**Owner:** Yeah, Shopify puts the link in there. I still get people emailing me for it, so I’m guessing some of them miss the email or just don’t see the link.

**Agent:** In a typical week, roughly how much time do you spend looking up orders and replying to those emails?

**Owner:** Maybe an hour or two a week just on tracking emails? That’s a guess. The fit questions are usually what keep me at the laptop longer.

**Agent:** Including the quick replies and the ones that send you to a spec sheet, roughly how much time do fit questions take you in a typical week?

**Owner:** Probably three or four hours a week, give or take. I’m mostly guessing from how many nights I end up answering emails after dinner.

**Agent:** Of those three or four hours, roughly how much time do you think the saved reply and a quick model-number lookup would save you in a typical week?

**Owner:** Maybe an hour a week? Hard to say until I try it. I could start with the parts people ask about all the time.

**Agent:** With the saved reply and lookup in place for those parts, what do you think would still take the most time when answering fit questions?

**Owner:** The used bikes where someone’s swapped parts. Even with a model number, sometimes I still need to ask what else is on the bike and check the specs. I’m up for trying the saved reply, but is there enough left after that to make a chatbot worth paying for?

**Agent:** I’d hold off on paying for a chatbot. The fit questions that keep you at the laptop involve used bikes with swapped parts. A bot could draft the follow-up, and you’d still spend time figuring out what’s on the bike and checking the supplier specs.

Start with the parts people ask about most. Put “11-speed” and “12-speed” in the dropdown, add the note about checking the stamped model number, and try the saved reply and lookup. For tracking emails, a saved reply with the customer’s existing tracking link keeps that job simple.

Once you’ve tried those changes, see how much time you still spend writing fit replies after you’ve found the answer. That’s the time a drafting tool could save, and it gives you something concrete to compare with the price. Does that line up with what you’re seeing?

**Owner:** Yeah, that makes sense. Once I know what fits, typing the reply is the easy bit. I’ll start with the dropdowns and saved replies and see how much of my evening I get back. Thanks. [END]

**Agent (closing turn, added after the harness stopped):** I’d hold off on the chatbot for now. As you try the dropdowns and saved replies, keep a rough tally of wrong-version returns and how much time you still spend checking specs after dinner. That’ll help you see what the changes saved you.
