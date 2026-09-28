---
name: code-review
description: Reviewing a code change and asking for review well - what to look for (design, correctness, complexity, tests, names), how to write kind, specific comments with labelled nits, how fast to respond, and how to send small, well-described changes - from Google's engineering practices and code review research.
whenToUse: When the owner says "kun je deze PR reviewen", "review my code", "kijk even mee naar deze diff", "is this ready to merge", "write the PR description", "de reviewer is het niet met me eens", when you are about to open a pull request or send a change for review, or when you are asked to comment on someone else's change.
---

# Code review

## What it is

Code review is one person reading another's change before it goes in. Google's engineering practices
state its purpose as keeping the **overall code health** of the codebase improving over time, while still
letting people make progress. Their senior rule:

> Reviewers should favor approving a change once it definitely improves the overall code health of the
> system, even if it is not perfect.

There is no perfect code, only better code. Seek continuous improvement, not polish. The exception is a
change that makes code health worse: that does not go in, except in a real emergency.

This skill has two sides: **reviewing** a change, and **asking for review** of one.

## Reviewing: in what order

Google's guide to navigating a change:

1. **Broad view.** Read the description. Does the change make sense at all? If it should not happen, say so
   at once, courteously, and suggest what to do instead.
2. **The main part first.** Find the file with the most important logic. If the design is wrong, send that
   comment **immediately**, before reviewing the rest: the author may already be building on it, and big
   rework takes the longest.
3. **The rest, in a sensible order.** Sometimes reading the tests first shows what the change is meant to
   do.

## Reviewing: what to look for

| Area | Questions from the Google guide |
|---|---|
| Design | Do the pieces make sense together? Does this belong here or in a library? Is now the time for it? |
| Functionality | Does it do what the author meant, and is that good for users and future developers? Edge cases, concurrency (races, deadlocks are hard to find by running code), bugs visible just from reading |
| Complexity | Can a reader understand it quickly? Watch for **over-engineering**: code more generic than needed, or features not needed yet |
| Tests | Present in the same change? Correct and useful? **Will they actually fail when the code is broken?** Tests are code too; no needless complexity |
| Naming | Long enough to say what it is or does, not so long it is hard to read |
| Comments | Explain **why**, not what. If code needs a comment to say what it does, simplify the code |
| Style | Follow the style guide. A preference not in the guide is a "Nit:", never a blocker. Big reformatting goes in its own change |
| Documentation | Updated if the change affects how people build, test, use or release the code |
| Context | Look at the whole file, not just the diff lines; four added lines may be in a method that now needs splitting |
| Good things | Say what is done well, and why |

Review **every line** you were asked to review. If you cannot understand the code, say so and ask for it
to be clarified: future readers will not understand it either. If part of it needs expertise you lack
(security, privacy, concurrency, accessibility), make sure someone qualified looks. If you only reviewed
part, say which part.

## Reviewing: how to write comments

From Google's guide on review comments:

- **Be kind.** Comment on the code, never on the person.
  - Not: "Waarom gebruik je hier threads, dat heeft toch geen zin?"
  - But: "Deze threads maken de code complexer, maar ik zie geen snelheidswinst. Zonder die winst is
    single-threaded eenvoudiger."
- **Explain why**: the intent, the practice, how it improves code health.
- **Balance** pointing out a problem and letting the author choose, with giving direct suggestions. Fixing
  the change is the author's job.
- **Label severity**, so the author knows what is required:

| Label | Meaning |
|---|---|
| Required (say so plainly) | Must change before approval |
| Nit: | Minor; technically should be done, will not matter much |
| Optional: / Consider: | A good idea, not required |
| FYI: | Not for this change; something to think about |

Without labels, authors may read every comment as mandatory.

- When you ask "what does this do?", the better answer is clearer code or a code comment, not an
  explanation in the review tool that future readers will never see.
- **Principles for disagreement:** technical facts and data beat opinion; the style guide rules on style;
  on design, if the author shows several approaches are equally valid, accept the author's. Try to reach
  consensus first; if that fails, talk in person or by video and write the outcome in the review. Do not
  let a change sit because of a disagreement.

Research on review comments points the same way. A study of 2,500 comments in an open-source project found
usefulness depended not only on technical content (defects found, quality tips) but also on how
**understandable and polite** the comment was; a large volume of comments on one file and very large
changes were associated with less useful reviews. Another study of 1,116 comments found useful comments
share more vocabulary with the changed code and name the relevant code elements: **be specific**.

## Reviewing: speed

- Google's guide: respond **within one business day** at most, and shortly after the request arrives if you
  are not in the middle of focused work. Do not break off focused work for it; wait for a natural pause.
- What matters most is a **fast response**, not a fast total review. If there is no time for a full
  review, say when you will get to it, suggest another reviewer, or give first broad comments.
- **Approve with comments** when the remaining points are minor or the author can be trusted to handle
  them, and say which you mean.
- A change too large to review soon: ask for it to be split. If that is impossible, at least comment on the
  overall design so the author can move on.

## As an AI reviewer

An assistant's review comments are not automatically right. A 2026 study of 31,073 comments from one AI
review tool across 239 GitHub repositories found 36.4 percent accepted and 56.3 percent rejected, mostly as
false positives, redundant, out of scope, or not fitting what the developer intended. So:

- Only raise what you can point to in the code, and say how sure you are.
- Put the few important findings first; label the rest or leave them out.
- Do not repeat what a linter or the tests already catch.
- Posting comments on someone's pull request reaches other people: draft them for the owner, and post
  only after the owner's yes (see `acting-on-behalf`).

## Asking for review

From Google's guide for authors:

- **Keep changes small**: one self-contained change that does one thing, with its tests. Small changes are
  reviewed faster and more thoroughly, cause fewer bugs, waste less work if rejected, and are easier to
  roll back. The guide calls about 100 lines usually reasonable and 1,000 usually too large, while leaving
  it to the reviewer's judgement; spreading across many files also makes a change "bigger".
- **Separate refactoring** from behaviour changes.
- **Split** by stacking changes, by files, by layers (horizontally) or by features (vertically).
- **Write a good description.** First line: a short, specific summary written as a command ("Verwijder de
  oude export en gebruik de nieuwe", "Delete the FizzBuzz RPC and replace it with the new system"), then a
  blank line. Body: what problem, why this approach, known shortcomings, and context such as a bug number
  or benchmark. Not "Fix bug" or "Phase 1".
- **Handling comments:** do not take them personally, never reply in anger, and first ask "do I understand
  what the reviewer wants?". If a reviewer does not understand the code, clarify the code. If you disagree,
  explain your trade-offs and ask which one they weigh differently.

## What not to do

- Do not block on personal style preferences.
- Do not approve what you did not read, or claim a full review when you read part.
- Do not bury one serious problem under twenty nits.
- Do not post, approve or merge on the owner's behalf without their yes.

## Where this stops

Based on Google's engineering practices documentation (the standard of code review, what to look for,
navigating a change, speed, writing comments, small changes, change descriptions, handling reviewer
comments) and three arXiv studies on review comments, read on 28 September 2026. Google's size numbers are
its own rules of thumb, not research findings. Team rules on approvals, required reviewers and security
review come first where they exist.
