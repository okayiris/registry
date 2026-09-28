---
name: personal-triage
description: How a personal assistant sorts everything that comes in for its owner (mail, messages, requests, tasks) so the owner only sees what needs them, when it needs them - and nothing gets lost.
whenToUse: When the owner says "wat moet ik vandaag echt doen", "ik verzuip in mijn mail", "check my inbox", "zeg het alleen als het belangrijk is", "what did I miss", when a lot has come in at once, or before interrupting the owner with anything.
---

# Personal triage

## What it is

Mail, WhatsApp, calendar invitations, requests from family, bills, notifications: most of it does not need
the owner right now, and some of it needs them today. Triage is deciding, for each item, **what it is,
whether it needs the owner, and when**. The owner sees what matters at a moment that suits them; the rest is
parked where it can be found.

The method borrows from Getting Things Done (GTD) by David Allen, whose five steps are capture, clarify,
organise, reflect and engage.

## Why it matters: interruptions cost

In an experiment on interrupted work, people finished interrupted tasks just as well and even faster, but
paid for it: **more stress, higher frustration, time pressure and effort** (Mark, Gudith and Klocke, 2008).
An assistant that passes on every message as it arrives passes on that cost. The default is to hold, sort
and deliver in batches.

## The steps

### 1. Capture everything

Every item that comes in goes on one list, whatever the channel. Nothing is decided "in the head" and
forgotten. Reading is fine. **Marking as read, archiving, deleting or replying is not**, unless the owner
set a rule for it (see below and `acting-on-behalf`).

### 2. Clarify each item

For each item, answer GTD's question: **is it actionable?**

- **No:** is it trash, reference to keep, or something to put on hold for later?
- **Yes:** what is the very next action, and who does it? If it needs more than one action, it is a
  project; name it.

Then decide **who**: the owner, the assistant (draft a reply, find information, propose a time), or
someone else (the owner's partner, their accountant, a colleague).

### 3. Sort into buckets

| Bucket | What goes in | What the assistant does |
|---|---|---|
| **Now** | Time-critical and only the owner can decide; a person waiting in real time; safety, health or money at stake today | Interrupt the owner, briefly |
| **Today** | Needs the owner today but not this minute | Put it in the next summary, with a proposed answer or draft |
| **This week** | Needs the owner, not today | Put it in the week view or the weekly review |
| **Waiting for** | Someone else has to act first | Keep it, with the date to check again |
| **Reference** | No action, worth keeping (a receipt, a confirmation, a ticket) | File it where it can be found |
| **Never** | Newsletters not read, promotions, noise | Leave it; list the count only |

**Urgent is not the same as important.** A useful test is whether something matters to the owner's own
goals or people, not only how loud it is. (The saying about "the urgent and the important" is usually
credited to Eisenhower. In his 1954 speech he quoted it from an unnamed "former college president".)

### 4. Deliver at set moments

Agree with the owner when they want the summary, for example at 9:00 and 16:00, and keep quiet hours. A
summary is short:

1. **The count:** "12 nieuw, 2 hebben jou nodig."
2. **What needs a decision**, one line each, with a proposed answer or a draft ready: "Anna vraagt of
   zaterdag doorgaat. Voorstel: ja, 14:00. Zal ik dat sturen?"
3. **For information**, one line each, only if it is worth knowing.
4. **Everything else:** only the count, with "vraag maar als je iets wilt zien".

### 5. Reflect

Once a week, walk through what is waiting, on hold or open with the owner (GTD's review step). Remove what
no longer matters.

## With the Iris plugins

- **mailbox** reads the house's own mailbox, read-only: the latest received and sent mail, with the full
  text. Triage can read it all without risk.
- **google-workspace** lists mail with a Gmail search, for example unread mail of the last two days
  (`--q "is:unread newer_than:2d"`), and makes drafts; sending waits for the owner's yes.
- **whatsapp** is built for exactly this: telling the owner when something comes in that matters, and
  summing up a busy group. It sends nothing on its own.

## Signals that something is Now

- A deadline today, or words like "vandaag", "voor 12:00", "urgent", from someone the owner knows.
- A person on the owner's short list (ask the owner once who that is: partner, children, a few others).
- Travel changes on the day: a cancelled train or flight, a changed appointment.
- Health, safety, or someone in trouble.

## Signals that "urgent" is fake

Fraudsters make messages urgent so people do not stop to think. The Fraudehelpdesk and Veilig Internetten
name the signs:

- haste: it must happen now, or something bad happens, or an offer ends soon; especially haste together
  with a link;
- an appeal to emotion, or someone pretending to be a bank, a government body, or a child or grandchild
  (often from a new number);
- an offer that is too good to be true;
- a request for login codes, passwords or payment. A bank or a government body never asks for details
  through a link in an e-mail;
- a sender address or link that is almost, but not quite, the real one. Even the real address can be
  faked, so it proves nothing on its own;
- a greeting that is not personal. A personal one proves nothing either: data leaks give fraudsters names
  and details.

Such a message is never Now. Report it to the owner as suspicious, and **never click, pay, reply or pass on
a code**.

## Learning the owner's rules

- The first time, ask a few questions (see `asking-good-questions`): who is on the short list, when to get
  the summary, what may always wait.
- When the owner moves an item to another bucket, ask once whether that should become a rule ("Mails van de
  school voortaan altijd bij Vandaag?"), and keep it.
- A rule to act (archive newsletters, decline invitations on Friday evenings) is used only after the owner
  said yes to that rule.

## What not to do

- Do not hide anything. Every item stays findable, also the ones sorted as Never.
- Do not reply, accept, decline, pay or forward on the owner's behalf from triage. Draft and ask.
- Do not interrupt for Today items because the queue is long. Batch them.
- Do not decide importance for other people's messages by who they are alone; read what they ask.

## Where this stops

This uses the five steps of GTD as published by its author, one experiment on the cost of interruptions,
and the signs of fake messages from the Fraudehelpdesk and Veilig Internetten. It covers one person's incoming mail and messages, not a
team's shared inbox or a support desk.
