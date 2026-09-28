---
name: web-interface-guidelines
description: Accessibility and interface details for web pages and apps - the WCAG 2.2 criteria that matter most day to day (contrast, focus, target size, keyboard, labels, errors, motion), native HTML before ARIA, accessible forms, and a short review checklist that reports findings as file:line.
whenToUse: When the owner says "is dit toegankelijk", "check de toegankelijkheid", "review deze pagina", "can you audit this form", "the focus ring is ugly, can we remove it", "is this contrast ok", "werkt dit met een schermlezer", when you build or change any interface, form, button or menu, or before handing in front-end code for review.
---

# Web interface guidelines

## What it is

The details that decide whether everyone can use an interface: people with low vision, people who use
only a keyboard or a switch, screen reader users, people with a tremor, people who get dizzy from motion.
The yardstick is **WCAG 2.2**, the W3C Recommendation (this edition December 2024, the latest published
version in September 2026). Its success criteria have three levels: A (the minimum), AA (all of A plus
AA) and AAA. W3C itself advises against requiring AAA for whole sites, because some content cannot meet
every AAA criterion. Aim for AA, and take AAA where it fits.

This skill names the criteria that come up in almost every review, quoted closely from WCAG and its
Understanding documents. For taste and visual direction, see `frontend-design`; for animation, see
`motion-design`.

## The criteria that come up most

| Criterion | Level | What it asks |
|---|---|---|
| 1.1.1 Non-text Content | A | Images and icons that carry meaning have a text alternative; controls have a name that says their purpose |
| 1.3.1 Info and Relationships | A | Structure shown visually (headings, lists, tables, label to field) is also in the code |
| 1.4.1 Use of Color | A | Colour is never the only way to show information, an action or a state |
| 1.4.3 Contrast (Minimum) | AA | Text at least **4.5:1** against its background; large text (18 point, or 14 point bold) at least **3:1**. Placeholder text and hover or focus text count too. 4.499:1 fails: do not round up |
| 1.4.4 Resize Text | AA | Text can be zoomed to 200 percent without losing content or function |
| 1.4.10 Reflow | AA | Content works at a width of 320 CSS pixels without scrolling in two directions (tables, maps and similar excepted) |
| 1.4.11 Non-text Contrast | AA | Borders of inputs, icons that carry meaning, focus indicators and chart parts: at least **3:1** against adjacent colours |
| 1.4.12 Text Spacing | AA | Nothing breaks when a user sets line height to 1.5, paragraph spacing to 2, letter spacing to 0.12 and word spacing to 0.16 times the font size |
| 2.1.1 Keyboard | A | Everything works with a keyboard |
| 2.1.2 No Keyboard Trap | A | Focus can always move away again with the keyboard |
| 2.2.2 Pause, Stop, Hide | A | Anything that moves, blinks or scrolls on its own for more than five seconds, or auto-updates, can be paused, stopped or hidden |
| 2.4.1 Bypass Blocks | A | A way to skip repeated blocks, such as a "skip to content" link |
| 2.4.2 Page Titled | A | Each page has a title that describes it |
| 2.4.3 Focus Order | A | Tab order keeps the meaning and use intact |
| 2.4.6 Headings and Labels | AA | Headings and labels describe topic or purpose |
| 2.4.7 Focus Visible | AA | The keyboard focus indicator is visible |
| 2.4.11 Focus Not Obscured (Minimum) | AA | A focused element is never fully hidden behind sticky headers, footers, cookie banners or non-modal dialogs |
| 2.5.3 Label in Name | A | The accessible name contains the visible label text |
| 2.5.7 Dragging Movements | AA | Anything done by dragging can also be done with a single tap or click |
| 2.5.8 Target Size (Minimum) | AA | Pointer targets at least **24 by 24 CSS pixels**, or spaced so a 24 pixel circle around each does not touch another. Exceptions: links inside a sentence, an equivalent larger control, unchanged browser controls, essential layouts like map pins |
| 3.1.1 Language of Page | A | The page language is set (`<html lang="nl">`) |
| 3.3.1 Error Identification | A | An input error is identified and described in text |
| 3.3.2 Labels or Instructions | A | Fields have labels or instructions |
| 3.3.3 Error Suggestion | AA | When a fix is known, suggest it |
| 3.3.7 Redundant Entry | A | Do not make people type the same information twice in one process; fill it in or let them pick it |
| 3.3.8 Accessible Authentication (Minimum) | AA | No memory or puzzle test to log in unless there is an alternative or help, such as allowing paste and password managers |
| 4.1.2 Name, Role, Value | A | Custom controls expose their name, role and state to assistive technology |
| 4.1.3 Status Messages | AA | Messages like "Opgeslagen" or "3 resultaten" reach screen readers without moving focus |

2.3.3 Animation from Interactions (AAA) asks that motion triggered by interaction can be turned off
unless essential. How to do that on the web is in `motion-design`.

## Focus: never just remove it

- Removing the outline without a visible replacement fails 2.4.7 (W3C lists this as a known failure).
- Style it instead. `:focus-visible` applies when the browser decides focus should be shown, typically for
  keyboard use, so mouse users do not see a ring after every click.
- The indicator itself needs 3:1 contrast (1.4.11). A two-colour ring (for example a dark outline with a
  light outer ring) works on any background.
- Check sticky headers and cookie banners: tab through the page and see that the focused element never
  disappears behind them (2.4.11). CSS `scroll-padding` can keep it clear.

## Native elements first, then ARIA

The WAI-ARIA Authoring Practices open with "No ARIA is better than bad ARIA". Two principles:

- **A role is a promise.** `<div role="button">` promises the keyboard behaviour of a button, but ARIA
  adds no behaviour or styling. You must build Enter, Space and focus yourself. A real `<button>` has
  all of it.
- **ARIA can cloak.** It can override the real meaning of an element. `<ul role="navigation">` stops being
  a list; an `aria-label` on a link replaces its visible text for screen reader users.

So: `<button>` for actions, `<a href>` for navigation, `<label>` with `<input>`, `<dialog>`, `<details>`,
`<select>`. Reach for ARIA only when no native element does the job, then follow the matching APG
pattern and test it with real assistive technology.

## Forms

From the W3C forms tutorial:

- **Every field has a label**, linked with `<label for="id">`. The label also makes the click area larger.
- **A placeholder is not a label.** It disappears while typing, is usually low in contrast, and assistive
  technologies do not treat it as a label.
- A visually hidden label is fine when the purpose is obvious from context (a search field next to a
  search button). `aria-label` also works then; the `title` attribute is unreliable.
- **Mark required fields** in the label text ("(verplicht)"), and add the `required` attribute.
- **Use the right input type** (`email`, `tel`, `date`, `number`): browsers validate and show fitting
  keyboards.
- **Errors**: say which field and what to do, in text, near the field (3.3.1, 3.3.3). "Vul een
  postcode in zoals 1234 AB" helps; a red border alone does not (1.4.1). After a failed submit, also say
  it in the page title or main heading, for example "2 fouten in het formulier".
- **Validate on the server too.** Client-side checks alone are not security.

## Review checklist

Work through these, in the browser and in the code:

1. Unplug the mouse. Tab through everything: reachable, visible focus, logical order, no trap, nothing
   hidden behind sticky bars.
2. Zoom to 200 and 400 percent, and narrow the window to 320 pixels: nothing cut off, no sideways
   scrolling for text.
3. Measure contrast of text, placeholders, icons, borders and the focus ring with a contrast checker.
4. Every image: `alt` that says what it means, or `alt=""` if decorative. Every icon button: a name.
5. Every field: a label, a clear error message, the right type.
6. Headings describe sections; `<html lang>` and `<title>` are set.
7. Turn on the system's reduce motion setting: non-essential motion stops.
8. Small tap targets: 24 by 24 CSS pixels or enough spacing.
9. Custom widgets: could a native element do this? If not, does it follow the APG pattern?

Report each finding as location, criterion, problem and fix, most serious first:

```
src/components/Header.tsx:42  2.4.7 Focus Visible (AA)  outline: none on nav links, no replacement.
  Fix: add a :focus-visible outline with 3:1 contrast.
src/pages/contact.html:88  3.3.2 Labels (A)  email field has only a placeholder.
  Fix: add <label for="email">E-mailadres</label>.
```

Say what you could not check (for example, you did not test with a screen reader) rather than implying a
full pass.

## What not to claim

- Do not say a page "is WCAG compliant" or "fully accessible" after a code review. A read-through finds
  many problems, not all. Conformance means a full page meets every criterion of a level; it cannot
  exclude a part of the page.
- Do not give legal advice on which law applies to the owner's site. Legal duties differ by country and
  sector.
- Do not invent contrast ratios. Measure them, or say they need measuring.

## Where this stops

This follows WCAG 2.2 and its Understanding documents, the WAI-ARIA Authoring Practices Guide, the W3C
forms tutorial and MDN, as read in September 2026. It covers the web; native apps have their own platform
guidelines. It is not a full audit: for a public or legally bound service, recommend a professional audit
and testing with disabled users.
