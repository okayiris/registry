---
name: motion-design
description: Interface motion that helps instead of distracts - when motion earns its place (feedback, state change, orientation), duration and easing, animating only cheap properties for smooth performance, and respecting prefers-reduced-motion and the WCAG criteria on animation and flashing.
whenToUse: When the owner says "maak het wat levendiger", "voeg een animatie toe", "this feels janky", "add a nice transition", "moet dit bewegen", "the page makes me dizzy", when you write CSS transitions, keyframes or JavaScript animation, review a design with parallax, auto-playing carousels or scroll effects, or when a page stutters while something moves.
---

# Motion design

## What it is

Motion draws the eye. That is its use and its risk: human vision is very sensitive to movement, so a
small animation makes sure feedback is noticed, and a needless one pulls attention away from the task.
Apple's Human Interface Guidelines put it simply: add motion purposefully, do not add motion for its own
sake, and make it optional. For some people motion is not a matter of taste: movement such as parallax,
zooming or scaling large objects can trigger vestibular reactions like dizziness, nausea and headaches.

This skill helps an assistant decide whether something should move, how long and how, how to keep it
smooth, and how to switch it off for people who asked for less motion.

## When motion earns its place

From Nielsen Norman Group's review of interface animation, motion helps when it does one of these:

| Purpose | Example |
|---|---|
| Feedback that an action was received | A menu slides in when the menu button is tapped; the cart icon moves when an item is added, so the change is not missed |
| State or mode change | An edit icon morphs into a save icon; a skeleton screen shows that content is loading |
| Orientation in space | A zoom in and out between years, months and days; a slide forward through checkout steps; a smooth scroll to an anchor so it is clear you stayed on the same page |
| Signifier | A card that rises from the bottom suggests it can be pulled down to close |

It does not earn its place when it only fills time, decorates, or hijacks attention (a flashing countdown
to create urgency is a dark pattern). Apple adds: avoid adding motion to interactions people do very
often, and let people act without waiting for an animation to finish.

Ask the owner one question before adding motion: "Wat moet de gebruiker hierdoor beter snappen?" If
there is no answer, leave it still.

## Duration and easing

Nielsen Norman Group's guidance, as practice rather than a standard:

- Most interface animations fall between **100 and 500 ms**. Aim for the shortest time that is not
  jarring; animations are far more often too slow than too fast.
- Simple feedback (a checkbox, a toggle): about **100 ms**.
- Bigger changes, such as a modal entering: about **200 to 300 ms**.
- Around 500 ms, animations start to feel like a drag. Keep 400 ms for large movements on large screens.
- Things appearing may take a little longer than things leaving (for example 300 ms in, 200 to 250 ms
  out).
- **Ease-out** (fast start, slow finish) suits most entrances: it feels responsive and lets the eye see
  where the element lands. Ease-in suits exits. Linear motion tends to look mechanical.

The CSS keywords, as MDN defines them:

| Keyword | Equals | Feels like |
|---|---|---|
| `ease` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Slow start, sharp speed-up, gradual slow-down |
| `ease-in` | `cubic-bezier(0.42, 0, 1, 1)` | Slow start, abrupt stop |
| `ease-out` | `cubic-bezier(0, 0, 0.58, 1)` | Abrupt start, gentle stop |
| `ease-in-out` | `cubic-bezier(0.42, 0, 0.58, 1)` | Slow at both ends |
| `linear` | `cubic-bezier(0, 0, 1, 1)` | Constant speed |

Put durations and easings in CSS custom properties (`--duration-short: 120ms;`) so the whole interface
moves consistently and one place changes it.

## Keep it smooth

web.dev explains why some animations stutter. The browser works in four steps: style, layout, paint and
composite. Animating a property reruns every step after the one it touches. For 60 frames per second each
frame has about 16.7 ms.

- **Animate `transform` and `opacity`.** Browsers can animate these two cheaply, often on the compositor
  thread, so they keep running even when the main thread is busy.
- **Do not animate layout properties** such as `width`, `height`, `top`, `left` or `margin`. Move with
  `transform: translate()`, resize with `transform: scale()`, show and hide with `opacity`.
- **Avoid animating to or from `auto`**; MDN notes the results differ between browsers.
- **Use `will-change` sparingly**, only when you see a problem, and remove it after. Every extra layer
  costs memory.
- **Measure** with the Performance panel in the browser's developer tools, not by eye alone.

## Reduced motion and WCAG

Operating systems have a setting to reduce motion (recent macOS and iOS: Accessibility, Motion; Windows 11:
Accessibility, Visual effects, Animation effects; Android: Remove animations). Browsers expose it as the
`prefers-reduced-motion` media feature, widely supported since January 2020.

```css
/* Motion only for people who have not asked for less */
@media (prefers-reduced-motion: no-preference) {
  .panel { transition: transform var(--duration-medium) ease-out; }
}
```

- **Reduce, do not always remove.** Replace a slide or zoom with a quick fade, or tone a scale down. Keep
  what carries meaning, like a progress indicator.
- **Put motion inside `no-preference`**, as web.dev does, so browsers that do not know the query also get
  the calm version.
- **JavaScript animation** does not follow CSS media queries by itself. Check
  `matchMedia('(prefers-reduced-motion: reduce)')` and listen for changes.

The WCAG 2.2 criteria:

| Criterion | Level | Rule |
|---|---|---|
| 2.2.2 Pause, Stop, Hide | A | Anything that moves, blinks or scrolls on its own for more than five seconds alongside other content, such as a carousel or ticker, needs a way to pause, stop or hide it. Auto-updating content needs this too, or control over how often it updates |
| 2.3.1 Three Flashes or Below Threshold | A | Nothing flashes more than three times in any one second, unless below the flash thresholds |
| 2.3.3 Animation from Interactions | AAA | Motion triggered by interaction can be turned off, unless essential. Honouring the reduce motion setting is one of the ways W3C names |

Parallax scrolling is W3C's own example of non-essential motion that can trigger vestibular reactions.
Scroll effects and parallax always get a reduced motion version.

## What not to do

- Do not use motion as the only way to convey something; add text, an icon or a state.
- Do not make people wait for an animation before they can act again.
- Do not autoplay moving backgrounds or carousels without a visible pause control.
- Do not ship an animation you have not watched with reduce motion switched on.

## What not to claim

- Do not present the durations above as a standard. They are Nielsen Norman Group's practice guidance; the
  standards (WCAG) set no durations.
- Do not claim an animation "meets WCAG" because it is short. WCAG asks about control, flashing and
  auto-play, not about length.

## Where this stops

This follows WCAG 2.2 and its Understanding documents, MDN on `prefers-reduced-motion`, transitions and
easing functions, web.dev on animation performance and reduced motion, Apple's Human Interface Guidelines
on motion, and Nielsen Norman Group on the purpose and timing of animation, as read in September 2026. It
is about interface motion on the web, not video, motion graphics or games. For layout and colour see
`frontend-design`; for the wider accessibility review see `web-interface-guidelines`.
