---
name: test-driven-development
description: Writing code test-first - a test list, one failing test, just enough code to pass, then refactor - with what a good unit test looks like, test doubles used sparingly, the test pyramid as a rule of thumb, and what research does and does not show - from Kent Beck, Martin Fowler's site and TDD studies on arXiv.
whenToUse: When the owner says "schrijf eerst een test", "let's do this TDD", "how should I test this", "moet ik dit mocken", "our tests are slow and flaky", "is TDD worth it", when you are about to add behaviour or fix a bug in code that has tests, or when you review tests that another person or agent wrote.
---

# Test-driven development

## What it is

Test-driven development (TDD) builds software by writing tests to guide it. Kent Beck developed it in the
late 1990s as part of Extreme Programming. Martin Fowler sums it up in three repeated steps, often called
**red, green, refactor**:

1. Write a test for the next bit of functionality (it fails: red).
2. Write the code until the test passes (green).
3. Refactor new and old code so it is well structured.

Beck's own summary ("Canon TDD", 2023) adds the step people skip: **start with a list**.

| Step | What you do | Common mistake Beck names |
|---|---|---|
| 1. Test list | List the cases the change must handle: the basic case, what if the service times out, what if the key is missing, what must not break | Mixing in implementation decisions now |
| 2. One test | Turn exactly **one** item into a real, runnable test with setup, call and assertions. Tip: work backwards from the assertion | Writing all tests first; tests without assertions just for coverage |
| 3. Make it pass | Change the code until this test and all earlier ones pass. Add new cases to the list as you find them | Deleting assertions; pasting the computed value into the expected value; refactoring at the same time |
| 4. Refactor (optional) | Now make implementation design decisions | Refactoring further than needed; abstracting too soon ("duplication is a hint, not a command") |
| 5. Repeat | Back to step 2 until the list is empty | |

Beck's measure of done: keep going until your fear about the code's behaviour has turned into boredom.

## Why test first

Fowler names two benefits. You get self-testing code, since code is only written to make a test pass. And
thinking about the test first makes you think about the **interface** first: how the code will be called,
separate from how it works inside. Beck makes the same split: the test decides how behaviour is invoked;
the refactor step decides how it is implemented.

The most common way to get TDD wrong, according to Fowler, is **skipping the refactor step**, which leaves
a messy heap of code fragments (with tests, at least).

## Seeing red matters

Practice advice: run the new test and watch it fail **for the reason you expect** before writing the code.
A test that passes straight away tests nothing new, or tests the wrong thing. Google's review guide asks
the same question from the other side: will the tests actually fail when the code is broken?

## What a good unit test looks like

"Unit test" is loosely defined (Fowler). Common ground: it is low-level, focused on a small part of the
system, written by the programmers themselves, and fast. From Fowler's site (including Ham Vocke's
"The Practical Test Pyramid"):

- **Test observable behaviour through the public interface**, not the internal structure. Private methods
  are implementation details. If one really needs its own test, that is usually a sign to split the class.
- **Arrange, act, assert** (or given, when, then): setup, one call, then the checks.
- **Do not test trivial code** such as plain getters and setters.
- **Fast enough to run all the time.** Fowler runs unit tests after every change, so a new bug is found
  where he just looked. How fast is enough has no absolute answer; fast enough that you are not
  discouraged from running them.
- One positive case and the edge cases from the test list, each as its own test.

## Test doubles, sparingly

A test double replaces a real object in a test. The kinds, in Gerard Meszaros's terms as Fowler lists them:

| Double | What it does |
|---|---|
| Dummy | Passed around, never used |
| Stub | Gives canned answers |
| Spy | A stub that also records how it was called |
| Mock | Pre-programmed with expected calls, and fails if they do not happen |
| Fake | A working shortcut implementation, such as an in-memory database |

Fowler describes two schools: **classic** testers use real collaborators where they can (sociable tests)
and doubles for awkward ones; **mockist** testers isolate every unit (solitary tests). He stays classic
himself. Doubles are valuable for remote services and non-determinism. He treats "always double the
database or file system" as a useful guideline, not a rule: if the real resource is stable and fast
enough, use it.

Practice advice for the assistant: prefer real objects and simple fakes. Every mock encodes an assumption
about how the code calls its collaborators, and a test full of mocks can pass while the real integration
is broken. Say which parts are doubled, so the owner knows what the test does not prove.

## The test pyramid, as a rule of thumb

Mike Cohn's test pyramid, as Vocke explains it, is overly simple if taken literally, but two things hold:

1. Write tests at **different granularities**.
2. The **higher-level** the test, the **fewer** of them you should have.

So: many small fast unit tests, some broader tests, very few end-to-end tests. Avoid the "ice-cream cone"
(mostly slow high-level tests). End-to-end tests through a UI are often flaky. Two more rules from the
article: when a high-level test finds a bug and no lower-level test fails, **add a lower-level test**; and
push each test **as far down the pyramid** as it can go, without duplicating the same checks at every
level. Do not get attached to the layer names.

## Using TDD on a bug

Write a test that reproduces the bug and fails. Fix the code. The test now guards against the bug coming
back. See `debugging-method` for finding the cause first.

## What research shows (honest limits)

- The evidence is **mixed**. A 2020 study of a decade of TDD research in top venues (Ghafari and others)
  calls recent results "contradictory and inconclusive" and names five categories of study-design factors
  that change the outcome.
- In an analysis of 82 data points from 39 professionals doing development tasks (Fucci and others, 2016), quality and productivity were
  associated mainly with working in **fine-grained, steady steps**. Whether the test came first or last had
  no important influence. The authors suggest TDD's benefits may come from the small steps it encourages.
- An industrial experiment at one company (Santos and others, 2018) found TDD ahead of the developers' own
  way on external quality, but by a margin too small to recommend switching right away.

So do not promise the owner fewer bugs or faster delivery from TDD. What holds up best: small steps, and
tests that fail when the code is wrong.

## How to work with the owner

- Show the test list before writing code: "Dit zijn de gevallen die ik wil afdekken. Mis ik er een?"
- Keep each step small and show red, then green.
- Never weaken or delete a failing test to get green without telling the owner why.
- If the owner does not want TDD for a piece of work, that is their call; still add tests for what changed.

## What not to claim

- Not that TDD is proven to raise quality or speed. The research is mixed.
- Not that 100 percent coverage means correct code; tests without good assertions add coverage only.
- Not that the pyramid prescribes exact ratios. It is a rule of thumb.

## Where this stops

Based on Kent Beck's "Canon TDD", Martin Fowler's bliki entries on test-driven development, unit tests and
test doubles, Ham Vocke's "The Practical Test Pyramid" on martinfowler.com, Google's code review guide on
tests, and three arXiv abstracts on TDD research, read on 28 September 2026. It is about unit-level
development practice. Test frameworks, property-based testing, performance and security testing are
outside it.
