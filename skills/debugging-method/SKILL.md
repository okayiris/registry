---
name: debugging-method
description: A systematic way to find and fix a bug - reproduce it, read what it says, test one hypothesis at a time, shrink the case, bisect the history, fix the cause rather than the symptom, add a test, and stop to rethink when fixes keep failing - from Zeller's Debugging Book, the Google SRE book and the git bisect manual.
whenToUse: When the owner says "het werkt niet", "ik snap niet waarom dit faalt", "this test is flaky", "it worked yesterday", "can you fix this error", "de build is stuk sinds vorige week", when you are about to change code because something fails, when a fix you made did not work, or when a problem report comes in about software the owner runs.
---

# Debugging method

## What it is

A bug shows itself as a **failure**: something visibly wrong. Behind it is a chain. Andreas Zeller's
Debugging Book names the links: a **mistake** by a person leads to a **defect** in the code, which, when
run, creates a **fault** (a wrong value) in the program state, which spreads until it becomes the failure.
Not every defect causes a failure, but every failure can be traced back to the defect that caused it.
Debugging is finding the step where a correct state first turns wrong, and fixing the code there.

The method is the **scientific method**: observe, form a hypothesis, predict what you would see if it is
true, test that in an experiment, and repeat until hypothesis and observations agree. The Google SRE book
describes troubleshooting the same way (hypothetico-deductive): hypothesize causes, then test them.

## The steps

### 1. Stop the bleeding first (when it is live)

If users are hurt right now, the SRE book puts making the system work as well as it can first: roll back,
divert traffic, switch a feature off. Root cause comes after. Preserve evidence such as logs while you do
it. Any action that reaches production or other people waits for the owner's yes (see `acting-on-behalf`).

### 2. Get a clear report and reproduce it

A good problem report says the **expected** behaviour, the **actual** behaviour, and how to reproduce it
(SRE book). Ask for what is missing, one question at a time (see `asking-good-questions`):
"Wat verwachtte je dat er zou gebeuren, en wat gebeurde er echt?"

Then make it fail on purpose, in a test or a small script, and note the exact command. This is practice
advice: a failure you cannot trigger is one you cannot check a fix against. When reproducing is not
possible (production, race conditions), say so: the SRE book notes that you may then only find **probable**
causes.

### 3. Read what it says

Practice advice, but the cheapest step: read the whole error message and stack trace, the first error
rather than the last, the exact line and value. Look at what the system **is** doing, not only what it is
not doing; the SRE book suggests asking "what", "where" and "why".

### 4. One hypothesis at a time, written down

- Write each hypothesis with the prediction that would confirm or refute it, and the outcome. Zeller
  keeps a numbered table of experiments; the SRE book says to take clear notes of ideas, tests and results.
  Every new idea can then be checked against earlier observations.
- Test the **likely and cheap** ones first ("when you hear hoofbeats, think of horses, not zebras"), and
  prefer simpler explanations.
- Design a test whose outcome splits the hypotheses: one result rules some in, the other rules them out.
- Change **one thing** per experiment. Active tests can have side effects (verbose logging can itself make
  a latency problem worse), so note what you changed and put it back.
- A refuted hypothesis is progress. The SRE book: negative results are conclusive and worth recording.
- Use assertions to check assumptions. Zeller: "Debugging is a game of falsifying assumptions"; an
  `assert` makes the failure show up earlier, closer to the fault.

### 5. Look at what changed

Systems tend to keep working until something acts on them, such as a configuration change or a change in
load; the SRE book calls recent changes "a productive place to start". Check the last deploys, dependency
updates and config changes.

### 6. Shrink the case

Remove everything that is not needed for the failure. Kernighan and Pike, quoted by Zeller: for every
circumstance, check whether it matters; if not, remove it. For an input: throw away half and see if it
still fails; if not, go back and try the other half. **Delta debugging** automates this and gives a result
where every remaining part is needed. In a system of many parts, the SRE book suggests working through
the components from one end, or splitting the system in half (bisection) when it is large.

### 7. Bisect the history

When it worked before, `git bisect` finds the commit that broke it by binary search:

```
git bisect start
git bisect bad                 # the current commit fails
git bisect good v1.4.0         # this one was fine
# test the commit git checks out, then mark it: git bisect good / git bisect bad
git bisect reset               # back to where you started
```

- `git bisect run ./test.sh` automates it. The script exits **0** for good, **1 to 127 except 125** for
  bad, and **125** for "cannot test this one" (skipped). Other codes abort the bisect.
- `git bisect skip` skips a commit that cannot be tested (for example, it does not build).
- The terms `old` and `new` (or your own) help when you look for a change that is not a bug, such as the
  commit that made something slow.
- `--first-parent` follows only the first parent at merges, useful when a merged branch contains commits
  that do not build.

### 8. Fix the cause, not the symptom

Before fixing, Zeller asks for a diagnosis that shows both:

- **causality**: how the defect causes the failure, and
- **incorrectness**: why that code is wrong.

If a change makes the failure go away but you cannot say why that line is wrong, you may be fixing the
symptom. If you found wrong code but did not show it causes this failure, the fix may not address it.
Zeller's "devil's guide" lists what not to do: scatter prints everywhere, change things at random until it
works ("debugging into existence"), and apply the most obvious fix to the symptom.

### 9. Prove it and prevent it

- Add a test that fails without the fix and passes with it, so the bug cannot quietly return (Zeller: add
  a test that catches the bug and similar ones). See `test-driven-development`.
- Check whether the same mistake was made elsewhere in the code.
- Remove temporary debug output; Zeller notes a forgotten debug print once logged passwords in clear text.
- Write the diagnosis in the commit message or the issue, so a reviewer can follow it (see `code-review`).

## When fixes keep failing

This is practice advice, not a research finding. If two or three fixes in a row have not worked, stop
changing code. The pattern usually means the hypothesis is wrong, not the fix. Go back to step 4: reread
the notes, list what is known for sure, and question an assumption you have not tested. Explaining the
problem out loud helps; Zeller describes "rubber duck debugging", where explaining the problem to someone,
or something, makes you explain it to yourself. Tell the owner plainly: "Drie pogingen hebben niet
gewerkt. Ik stop even met aanpassen en zoek eerst uit wat we echt zeker weten."

## What not to do

- Do not claim a bug is fixed without running the reproduction again.
- Do not change several things at once and call the one that "worked" the cause.
- Do not chase a correlation without checking it; the SRE book warns that many metrics correlate by
  coincidence or through a shared cause.
- Do not assume it is the same cause as last time just because it happened once before.
- Do not run experiments on production without the owner's yes.

## Where this stops

Based on Andreas Zeller's The Debugging Book (the chapters "Introduction to Debugging" and "Reducing
Failure-Inducing Inputs"), the chapter "Effective Troubleshooting" in Google's Site Reliability
Engineering book, and the git-bisect manual, read on 28 September 2026. Reading the error, making it fail
on purpose and stopping after repeated failed fixes are practice advice. Language-specific debuggers,
profilers and tracing tools are out of scope.
