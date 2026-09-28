---
name: frontend-design
description: Building web interfaces that are distinctive and easy to use - decide the purpose and an aesthetic direction first, then typography, colour, spacing and layout, and motion, checked against WCAG and on real devices instead of settling for the generic template look.
whenToUse: When the owner says "maak een website voor", "bouw een landingspagina", "dit ziet er zo standaard uit", "can you make it look better", "design a dashboard", "welk lettertype", "welke kleuren", when you are about to write HTML and CSS for a page, component or app, or when a design looks like every other template.
---

# Frontend design

## What it is

A good interface does its job, reads comfortably, works for everyone, and looks like it was made for this
purpose by someone who cared. The generic look (a centred hero, a stock gradient, three identical cards,
every heading huge) usually comes from skipping the decisions, not from a lack of talent. This skill puts
the decisions in order.

The measurable parts (sizes, contrast, reflow) come from WCAG 2.2, web.dev, MDN, Butterick's Practical
Typography and Apple's Human Interface Guidelines. The rest, direction and taste, is practice advice and
is labelled as such.

## 1. Purpose and direction first

Before any CSS, answer with the owner:

- **Who uses this, where, and for what?** A booking page on a phone at the station differs from a
  dashboard on a large screen.
- **The one thing a visitor must do or understand.** That thing gets the most visual weight; everything
  else steps back.
- **A direction in a few words.** For example "rustig en ambachtelijk", "zakelijk en precies", "speels
  maar leesbaar". Ask for two or three sites the owner likes, and what they like about them.
- **What exists already**: logo, colours, photos, tone of voice. Build from those.

Practice advice: pick one idea and carry it through (a typeface with character, one strong colour, a
layout grid, a photographic style). Distinctive usually means a few deliberate choices done consistently,
not many effects. Use `asking-good-questions` when the owner is unsure; show a small sample rather than
describing it.

## 2. Typography

For body text, Butterick names four choices that matter most: point size, line spacing, line length and
the font.

| Choice | Guidance | Source |
|---|---|---|
| Body size | 15 to 25 pixels on the web; never below the user's own setting (`1rem`) | Butterick; web.dev |
| Fluid size | `font-size: clamp(1rem, 0.75rem + 1.5vw, 2rem)`; never `vw` alone, or users cannot resize text | web.dev |
| Line length | 45 to 90 characters (Butterick); 45 to 75 is Bringhurst's range, quoted by web.dev; WCAG AAA asks for a way to get no more than 80. Use `max-inline-size: 66ch` or similar, not pixels | Butterick; web.dev; WCAG 1.4.8 |
| Line spacing | Butterick: 120 to 145 percent of the size. Short lines can take more; very loose spacing on long lines makes the next line hard to find. Use a unitless `line-height` | Butterick; web.dev |
| Weights | Avoid thin and light weights for small text; they are hard to read | Apple HIG |
| Number of typefaces | Few. Too many blur the hierarchy and make the interface feel inconsistent | Apple HIG |

**Hierarchy** comes from size, weight and colour together, used with restraint. Butterick calls the
browser habit of doubling the size for headings unnecessary; a smaller step is often enough. A type scale
(a fixed set of sizes) keeps it consistent.

**Web fonts** cost loading time. Use `woff2`, preload the main file, and set `font-display` so text stays
readable while the font loads (web.dev). Butterick advises a professional font over default system fonts
for character; Apple points to its own system fonts as typefaces designed for legibility. For a web page with
a clear direction, one well-made web font plus a system fallback is a sound middle.

**What users may change** must not break the page (WCAG 2.2): text zoomed to 200 percent (1.4.4), and
line height 1.5, paragraph spacing 2, letter spacing 0.12 and word spacing 0.16 times the font size
(1.4.12). Test it; do not fix heights on text boxes.

## 3. Colour

- **Contrast is not optional.** Body text at least 4.5:1 against its background, large text (18 point, or
  14 point bold) at least 3:1 (WCAG 1.4.3). Borders of inputs, meaningful icons and focus rings at least
  3:1 (1.4.11). Measure, do not guess; 4.499:1 fails.
- **Never colour alone** to carry meaning, such as an error or a status. Add text or a shape (WCAG 1.4.1;
  Apple HIG).
- **One colour, one meaning.** Apple: do not use the same colour for different things, like the brand
  colour for both buttons and plain text.
- **A small palette**, as practice advice: a background, a text colour, one or two accents, and states
  (error, success). Fewer colours make the accent stronger.
- **Mind culture.** Apple notes red means danger in some cultures and something positive in others.
- **Dark mode**: `prefers-color-scheme` tells you the user's choice. Set `color-scheme` so form controls
  follow, and check contrast again in dark mode (web.dev; Apple HIG).

Store colours as CSS custom properties on `:root` and switch them in one place (web.dev; MDN):

```css
:root {
  --page: #fbfaf7;
  --ink: #1d1d1b;
  --accent: #0b5d4b;
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 2rem;
}
@media (prefers-color-scheme: dark) {
  :root { --page: #161615; --ink: #eceae4; --accent: #5cc2a6; }
}
body { background: var(--page); color: var(--ink); }
```

MDN notes custom properties cannot be used inside a media query condition itself, only in property
values. The values above are an example; measure contrast for your own.

## 4. Space and layout

- **Content order first.** Write the HTML in a sensible single-column order; that is what small screens
  get (web.dev).
- **Grid for the page**, flexbox for rows of things. `grid-template-columns: repeat(auto-fill,
  minmax(15em, 1fr))` makes cards fit without media queries (web.dev).
- **Relative units** (`rem`, `em`, `ch`) so layout follows the user's text size.
- **A spacing scale** (a few fixed steps, as custom properties) keeps rhythm consistent. Related things
  sit closer together than unrelated things. This is practice advice, not a standard.
- **Reflow**: at a width of 320 CSS pixels, content must work without scrolling sideways (WCAG 1.4.10).

## 5. Motion

Motion should explain something: feedback, a change of state, where something came from. Keep it short,
animate `transform` and `opacity`, and honour reduced motion. The details are in `motion-design`.

## 6. Check it for real

- **On devices**: a real phone, a large screen, in bright light and in the dark. Apple advises testing
  colours in different lighting and on different devices; colours look darker and duller in sunlight.
- **With the keyboard and zoom**: see the checklist in `web-interface-guidelines`.
- **Against the purpose**: can someone new do the one main thing in a few seconds? Ask the owner to try it
  with someone else.
- **Loading**: fonts, images and scripts cost speed; a design that feels fast is part of the design
  (web.dev).

## What goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Looks like every template | No direction chosen; default fonts and gradients | Go back to step 1; one deliberate typeface, colour and grid |
| Tiring to read | Lines too long, small light text, tight spacing | `max-inline-size` in `ch`, size up, unitless line height |
| Everything shouts | Too many sizes, colours and bold | Fewer levels; let the main action lead |
| Grey on grey | Contrast not measured | Measure against 4.5:1 and 3:1 |
| Breaks on a phone | Fixed widths in pixels | Relative units, grid with `minmax`, test at 320 pixels |

## What not to claim

- Do not call a design "accessible" because it looks clean. Check the WCAG criteria.
- Do not present taste as a rule. Say "I would suggest" for direction and palette choices; state
  standards only where WCAG or the platform says so.
- Do not use fonts, photos or logos without a licence. Ask where they come from.

## Where this stops

This follows WCAG 2.2 and its Understanding documents, web.dev's Learn Design course, MDN, Butterick's
Practical Typography and Apple's Human Interface Guidelines on typography and colour, as read in September
2026. It gives direction and craft, not a brand identity: for a logo or a full brand, a designer is worth
it. Publishing the site or sending it to anyone waits for the owner's yes (`acting-on-behalf`).
