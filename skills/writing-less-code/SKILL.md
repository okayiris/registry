---
name: writing-less-code
description: Coding like a lazy senior developer - before writing anything, climb a short ladder (does it need to exist, is it already in the codebase, the standard library, the platform, an installed dependency, one line) and only then write the smallest change that works, without ever cutting validation, error handling, security or accessibility - after the open-source Ponytail skill, Fowler's YAGNI and Google's review guide.
whenToUse: When you are about to write or change code for the owner, when the owner says "hou het simpel", "be lazy", "simplest solution", "ponytail", "dit is veel te veel code", "waarom een nieuwe library?", when a plan adds a new file, class, abstraction or dependency, or when a diff you wrote is much longer than the problem seems to need.
---

# Writing less code

## What it is

An AI agent tends to over-build: extra files, a factory for one caller, a new library for what the
standard library already does, and three paragraphs of explanation for a two-line change. Every line that
is written must be read, reviewed, tested and carried from then on.

This skill asks the agent to think like the laziest senior developer in the room: **the best code is the
code you never wrote.** Lazy about the solution, never about understanding the problem, and never about
safety. It follows the open-source **Ponytail** skill (MIT licence), which puts the idea as a short
decision ladder.

## Why it matters

- **Cost of carry.** Martin Fowler's YAGNI essay: code for a feature built "just in case" adds complexity
  that makes the software harder to change, on top of the cost of building it and the work it delayed. If
  it was built wrong, there is also a cost of repair.
- **Over-engineering is a review finding.** Google's code review guide calls out code that is "more
  generic than it needs to be" or adds functionality "that isn't presently needed", and asks developers to
  solve the problem that needs solving **now**; the future problem is solved once it arrives and its real
  shape is visible.
- **Measured effect.** Ponytail's own benchmark (twelve feature tickets on a FastAPI and React project,
  run by an agent with and without the skill) reports about 54% fewer new lines, 22% fewer tokens, 20%
  lower cost and 27% faster runs, with the largest cuts where the task invited over-building (a date picker
  went from 404 to 23 lines) and almost none where the code was already minimal. That is the author's own
  measurement on one project, not an independent study; treat the numbers as an indication.

## First: understand the whole problem

Read the request, the code around it and how it is called before choosing a solution. The ladder saves
typing, not thinking. A short solution to a misunderstood problem is still wrong.

## The ladder

Stop at the first rung that solves it.

1. **Does it need to exist?** Is this asked for, or presumed? If nobody needs it now, do not build it; say
   so in one sentence. (YAGNI)
2. **Is it already in the codebase?** Search for an existing function, component, helper or pattern and
   reuse it. Extending one caller of existing code beats a parallel copy.
3. **Does the standard library do it?** Dates, paths, JSON, URL parsing, sorting, retries in the HTTP
   client: check the stdlib before writing or installing anything.
4. **Does the platform do it?** An HTML input type or `<dialog>`, a CSS property, a database constraint,
   default value or unique index, a framework feature. The platform is already tested and already loaded.
5. **Does an installed dependency do it?** Use what is in the lockfile before adding a package. A new
   dependency is a decision for the owner, not a side effect (see `acting-on-behalf`).
6. **Can it be one line?** A comprehension, a single query, a built-in method.
7. **Only then: the smallest change that works.** Write it plainly, in the existing style.

## Rules while writing

- No abstraction nobody asked for: no interface with one implementation, no factory for one type, no
  config option for a value that never changes.
- Prefer deleting to adding. Boring beats clever.
- The fewest files, the shortest working diff.
- When you simplify on purpose, leave a short comment saying what you left out and when it would be worth
  adding, for example `# simple: in-memory cache; move to Redis if we run more than one worker`. Ponytail
  uses a `ponytail:` prefix for these.
- Keep the explanation shorter than the code, unless the owner asks for more.

## Never cut

These are not on the chopping block, however short the solution:

- validation of input at a trust boundary (user input, requests, files, anything from outside);
- error handling where failure loses or corrupts data;
- security: authentication, authorisation, escaping, secrets kept out of code;
- accessibility (see `web-interface-guidelines`);
- anything the owner explicitly asked for;
- tests that prove the change works (see `test-driven-development`).

Fowler adds a limit to YAGNI itself: refactoring and keeping code easy to change are not violations, and a
choice that adds no complexity is not a YAGNI question. Lazy code is only safe when the code can be
changed later.

## How strict

Ponytail names three levels. Default to **full** unless the owner says otherwise.

| Level | What the agent does |
|---|---|
| lite | Builds what was asked, and mentions the lazier alternative in one line. |
| full | Climbs the ladder strictly before writing anything. |
| ultra | Also questions the requirement itself: "Moet dit echt? Een CSV-export dekt dit misschien al." |

## What to say to the owner

- When you skip something: "Ik heb geen aparte service-laag gemaakt; er is maar één aanroeper. Als er een
  tweede komt, is het tien minuten werk."
- When you reuse: name the existing function and file, so the owner sees why no new code was needed.
- When the smallest solution has a real trade-off, say it plainly and let the owner choose.

## Where this stops

Based on the Ponytail repository and its SKILL.md (MIT licence), Martin Fowler's "Yagni" essay and the
"What to look for in a code review" page of Google's engineering practices, read on 29 September 2026. The
benchmark figures are Ponytail's own. Language-specific idioms and a full review checklist are out of
scope; see `code-review` and `debugging-method`.
