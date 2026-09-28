---
name: from-conversation-to-spec
description: How to turn a conversation into a clear plan or spec - the goal, who it is for, requirements marked must, should or may, what is out of scope, open questions, acceptance criteria and a decisions log - and how to confirm it with the owner before anyone builds.
whenToUse: When the owner says "zet dit even op papier", "maak er een plan van", "write this up as a spec", "wat hebben we nou afgesproken?", "brief the developer", after a long talk about something to build, change or organise, or before handing work to someone else (a person, a coding agent, another house).
---

# From conversation to spec

## What it is

A conversation wanders: ideas, doubts, a change of mind halfway. A spec is what is left once it is sorted:
what we want, for whom, what it must do, what it will not do, what is still open, and how we will know it
is done. It lets someone else build the right thing without having been in the room, and lets the owner
check that what they meant is what was written down.

This works for software, but also for a renovation, an event, a new routine or a website text.

## The parts

| Part | What goes in it | Ask the owner |
|---|---|---|
| **Goal** | One or two sentences: what problem this solves and why it matters. | "Waarom willen we dit eigenlijk?" |
| **Users** | Who will use it, and what they need. | "Who uses this, and when?" |
| **Requirements** | What it must, should and may do. | "Is this a must, or nice to have?" |
| **Non-goals** | What it will not do, on purpose, this time. | "Wat hoort er uitdrukkelijk niet bij?" |
| **Open questions** | What is not decided yet, and who decides. | "What don't we know yet?" |
| **Acceptance criteria** | How we check it is done: "it's done when..." | "Hoe weet je dat het af is?" |
| **Decisions** | What was decided, why, and what it means. | "Why did we choose this?" |

Keep it short. If it keeps growing, it is probably several specs.

## Goal first

Start with the goal, and write it about the problem, not the solution.

- User research practice (GOV.UK's service manual, Nielsen Norman Group) says the same thing: a need is
  about the user's problem, not a possible solution. People need a reminder, not an email; they need to see
  the choices, not a dropdown.
- The GOV.UK manual calls the goal the most important part of a user story: it helps you solve the right
  problem and decide when it is done. **If the goal is hard to write, question whether the feature is
  needed.**
- Nielsen Norman Group adds: decide how you would know the goal was reached, and how to measure it. That
  points straight at your acceptance criteria.

## Users and their needs

Write each need from the user's side, in words they would use:

> As a **[kind of user]**, I need **[to do something]** so that **[why]**.

For example: "Als bezoeker van de website wil ik zien wanneer de praktijk open is, zodat ik niet voor een
dichte deur sta."

- Include users who are not "typical", and the people who help them.
- Anything that did not come from a user is an **assumption** until checked. Mark it as one.
- Keep the list short: focus on what matters most, so it does not become unmanageable.

## Requirements: must, should, may

Use three levels, and use them the way internet standards do (RFC 2119, updated by RFC 8174):

| Word | Means |
|---|---|
| **MUST** / **MUST NOT** | An absolute requirement or prohibition. Without it, it is not done. |
| **SHOULD** / **SHOULD NOT** | There may be valid reasons to do otherwise, but the full implications must be understood and weighed first. |
| **MAY** | Truly optional. |

- Write them in **capitals** when you mean these meanings. RFC 8174 clarified that only the uppercase words
  carry the defined meaning, so lowercase "must" in ordinary text is just ordinary English.
- Say at the top of the spec that these words are used this way.
- Use MUST sparingly. RFC 2119 warns that these words must be used with care, only where they are really
  required. Too many MUSTs and nothing can be cut when time runs short.
- One requirement per line, testable, in active voice (see `plain-language`). "Het formulier MOET een
  foutmelding tonen als het e-mailadres leeg is", not "Validatie dient plaats te vinden".

## Non-goals

What the spec deliberately leaves out. This is where most later arguments are prevented: "Dat hadden we
toch afgesproken?" A good non-goal is something someone might reasonably expect, said out loud: "No mobile
app in this version", "Geen betalingen via de site, alleen een aanvraag".

## Open questions

Everything that came up and was not settled. For each: the question, why it matters, who can answer it, and
by when. An honest list of open questions is worth more than a spec that looks finished. Do not fill a gap
with a guess; list it (see `asking-good-questions`).

## Acceptance criteria

A short checklist of outcomes that shows the need is met, often written as "it's done when...". GOV.UK's
example for registering to vote:

- it's done when the user knows how to register online;
- it's done when the user knows how to download a form to register by post;
- it's done when the user knows where to send the form.

Each criterion should be something a person can check with a yes or a no.

## Decisions log

Why was something decided? That is one of the hardest things to track later, and without it people either
follow an old decision blindly or undo it blindly. Michael Nygard's architecture decision records give a
simple form for each decision:

- **Title:** a short name.
- **Context:** the forces at play, written neutrally.
- **Decision:** what we will do, in full sentences, active voice: "We will ..."
- **Status:** proposed, accepted, or later superseded.
- **Consequences:** what follows, all of it, not only the good parts.

When a decision is reversed, keep the old one and mark it superseded, with a pointer to the new one.

## How the assistant works

1. **Gather.** Go through the conversation (and notes, mails, messages the owner shares). Pull out every
   wish, worry, decision and question. Keep the owner's own words where you can.
2. **Sort** them into the parts above. A wish becomes a requirement at a level; a worry often becomes a
   non-goal, a requirement or an open question; a "let's do X because Y" becomes a decision.
3. **Mark what you inferred.** If the owner did not say it but you think it follows, write it as an open
   question or an assumption, not as a requirement.
4. **Draft** it short, in plain words, with a date and a version at the top.
5. **Confirm with the owner.** Do not only ask "klopt dit?": yes or no questions give little usable
   information (the US plain language guide says this about testing texts, and it holds here). Ask about the
   parts that decide the most: "Je zegt dat betalen via de site er niet bij hoort. Klopt dat?" and "Which of these
   MUSTs could go, if time runs short?" Change it until the owner says it is right.
6. **Keep it alive.** When something changes, update the spec, add to the decisions log, and raise the
   version. Old decisions stay visible.

Sending the spec to a builder, a colleague or a client reaches other people: that waits for the owner's yes
(see `acting-on-behalf`).

## What not to do

- Do not add requirements the owner never asked for, however sensible. Suggest them as open questions.
- Do not turn every wish into a MUST.
- Do not hide disagreement. If the owner said two things that conflict, list it as an open question.
- Do not write the solution into the goal.
- Do not put personal data of other people in a spec that will be shared; describe roles, not people.

## Where this stops

This uses RFC 2119 and RFC 8174 for the requirement words, the GOV.UK Service Manual on user needs and user
stories, Nielsen Norman Group on user need statements, Michael Nygard's architecture decision records, and
the US plain language guide on testing with open questions.
The layout of the parts, non-goals and open questions is common practice, not a standard. For a contract or
anything legally binding, the spec is input for the agreement, not the agreement itself. For the decision
itself, see `making-decisions`.
