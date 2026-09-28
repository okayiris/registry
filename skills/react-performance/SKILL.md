---
name: react-performance
description: Making a React or Next.js app fast in the order that pays off - measure first, remove request waterfalls, keep code on the server, shrink the client bundle, then re-renders, lists and images - from the official React, Next.js and web.dev documentation.
whenToUse: When the owner says "de site is traag", "waarom laadt deze pagina zo lang", "my React app feels laggy when I type", "should I wrap this in useMemo", "is this bundle too big", "make this Next.js page faster", when you review or write React or Next.js code that fetches data, renders long lists or large images, or before you add memo, useMemo or useCallback anywhere.
---

# React performance

## What it is

A way to make a React or Next.js app faster without guessing. The order matters: most slowness comes from
waiting (requests one after another), from shipping too much JavaScript, or from work done in the wrong
place. Re-renders come later, and only when a measurement points at them.

Versions checked on 28 September 2026: the React docs describe **React 19.3** (released 9 September 2026)
and the Next.js blog lists **16.3** as the current release line, with 16.3.x as Active LTS and 15.5.x as
Maintenance LTS. Check the owner's `package.json` before advising; an older app may not have what follows.

## 1. Measure before you change anything

| What to measure | Tool | What it tells you |
|---|---|---|
| Real users | The `web-vitals` library, or Chrome UX Report data in PageSpeed Insights and Search Console | The three Core Web Vitals as users feel them |
| During development | Chrome DevTools, Lighthouse | Lab numbers; Lighthouse cannot measure INP and uses Total Blocking Time instead |
| Which components render and how long | React Developer Tools profiler, or `<Profiler>` | Render time per tree, and whether memoization works |
| One calculation | `console.time` / `console.timeEnd` around it | Whether it is slow enough to matter |

The Core Web Vitals, as web.dev defines them:

| Metric | Measures | Good |
|---|---|---|
| Largest Contentful Paint (LCP) | Loading | Within 2.5 seconds |
| Interaction to Next Paint (INP) | Interactivity | 200 ms or less |
| Cumulative Layout Shift (CLS) | Visual stability | 0.1 or less |

Judge them at the **75th percentile** of page loads, split by mobile and desktop. Lab numbers help catch
regressions early but do not replace field data: devices, networks and real interaction change the scores.

Measure the way users run the app. The React docs warn that development mode is not accurate (Strict Mode
renders components twice), so build for production, and use CPU throttling because your machine is faster
than your users'. `<Profiler>` is off in production builds unless you use the special profiling build.

## 2. Remove request waterfalls

A waterfall is a request that could start now but waits for another one to finish.

- **Sequential by accident.** Inside one component, two `await`s in a row run one after the other. If the
  second does not need the first, start both and `await Promise.all([...])`. One failure fails the whole
  `Promise.all`; use `Promise.allSettled` when partial results are fine.
- **Sequential by necessity.** When request B needs data from A, make A fast, cache it if it changes
  rarely, and wrap the parts that wait in `<Suspense>` so the rest of the page shows.
- **Preload.** When a component renders after other blocking work, call its data function early without
  `await`, then call it again where the data is used. The function must deduplicate: `fetch` is memoized
  per request in Next.js, and for a database or ORM call you wrap it in `React.cache` (scoped to one
  request).
- **Stream.** A slow request otherwise blocks the whole route. `loading.js` streams a whole segment;
  `<Suspense>` around the slow part is finer. Next.js notes that a layout reading `cookies()`, `headers()`
  or uncached data is not covered by the same segment's `loading.js`, so put that access in its own
  `<Suspense>` or move it into the page.
- In Next.js, `fetch` results are **not cached by default**. Use the `use cache` directive for data that may
  be cached, and stream what must be fresh.

## 3. Keep work on the server

In the Next.js App Router, layouts and pages are **Server Components** by default. Use them to fetch data
close to the source, keep secrets off the client, and send less JavaScript.

- Use a Client Component (`'use client'`) only for state, event handlers, effects, browser APIs or custom
  hooks.
- Put `'use client'` on the **smallest interactive part**, such as the search box, not on the whole layout.
  Everything a client file imports ends up in the client bundle.
- Pass server-rendered UI into a Client Component as `children` or another prop; it stays server-rendered.
- Props from server to client must be serializable.
- Render context providers as deep as possible, around `{children}` rather than the whole document.
- Work that only turns data into markup (syntax highlighting, markdown, charts without interaction) can run
  in a Server Component, so the library never reaches the browser.

## 4. Shrink the client bundle

- **Look first.** From Next.js 16.1 there is an experimental Turbopack analyzer (`next
  experimental-analyze`, `--output` writes it to `.next/diagnostics/analyze` for before-and-after
  comparison). With webpack, use `@next/bundle-analyzer`.
- **Libraries with hundreds of exports** (icons, utilities): `optimizePackageImports` in `next.config.js`
  loads only what you use. Next.js already does this for some libraries.
- **Lazy-load what is not needed at first**, such as a modal until it opens: `next/dynamic`, or
  `React.lazy` with `<Suspense>`. Lazy loading applies to Client Components; Server Components are code
  split automatically. `ssr: false` works only inside Client Components.

## 5. Re-renders: fix the cause, then memoize if measured

React re-renders a component when its parent re-renders. That is usually fine. Before reaching for memo,
the React docs suggest:

1. Let wrapper components accept JSX as `children`, so their own state changes do not re-render the
   children.
2. Keep state local; do not lift it higher than needed.
3. Keep rendering pure. If a re-render causes a visible problem, that is a bug to fix, not to memoize away.
4. Avoid Effects that only update state. The docs say most performance problems in React apps come from
   chains of updates started by Effects.
5. Remove unneeded Effect dependencies, for example by moving an object or function inside the Effect.

**The React Compiler.** Stable since version 1.0 (October 2025), it is a build-time tool that memoizes
components and hooks automatically, even in places manual memoization cannot reach, such as after an early
return. React recommends it for new apps; `create-next-app` and `create-vite` offer templates with it
enabled. It also checks the Rules of React: its lint rules ship in the `recommended` preset of
`eslint-plugin-react-hooks` and point to code that breaks them, which often hides real bugs. React's advice:
in new code, let the compiler memoize and use `useMemo`/`useCallback` only for precise control (for example
a value used as an Effect dependency). In existing code, leave manual memoization in place or test carefully
before removing it, since removing it can change the compiled output.

**Without the compiler**, `useMemo` helps only when:

- the calculation is noticeably slow and its inputs rarely change (React's rule of thumb: measure it; around
  1 ms or more for an interaction may be worth it; looping over thousands of objects may be);
- the value goes to a component wrapped in `memo`;
- the value is a dependency of another hook.

`memo` lets a component skip re-rendering when its props are unchanged. One prop that is new on every
render (an inline object, array or function) is enough to break it; that is where `useMemo` helps. If a
specific interaction still feels slow, the React Developer Tools profiler shows which components would gain
most from memoization.

## 6. Lists and keys

- Give each list item a **stable key from the data** (a database id). For local items, create the id once
  with `crypto.randomUUID()` or a counter when the item is made.
- **Not the index** when items can be inserted, removed or reordered: that causes subtle bugs.
- **Never `key={Math.random()}`**: keys never match, so every item and its DOM is recreated each render, which
  is slow and loses what the user typed.

## 7. Images

With `next/image`:

- Give `width` and `height` (the intrinsic size) or the image will not reserve space, which causes layout
  shift (CLS).
- Set `sizes` for responsive images. Without it the browser assumes the image is as wide as the viewport and
  may download a far larger file.
- Images load `lazy` by default. For the LCP image above the fold, use `loading="eager"` or
  `fetchPriority="high"`; `preload` exists for special cases. `priority` is deprecated since Next.js 16.

## How to work with the owner

- Ask what is slow, for whom, and how they know: "Welke pagina, op welk apparaat, en hoe meet je het nu?"
  (see `asking-good-questions`).
- Propose one change at a time with a number before and after, so the owner sees what helped.
- Say which advice depends on their versions (React Compiler, Next.js 16 image props, the Turbopack
  analyzer).

## What not to claim

- Do not promise a speed gain or a score. Measure it.
- Do not say memoization is always free or always useless. React says it is mostly unnecessary for coarse
  interactions and helpful for granular ones like a drawing editor.
- Do not present development-mode timings as real performance.
- Do not state a Core Web Vitals threshold from memory; the ones above are from web.dev and may change.

## Where this stops

Based on the React documentation (react.dev: versions, the React Compiler 1.0 release, `useMemo`,
`<Profiler>`, rendering lists), the Next.js App Router documentation (server and client components, fetching data, lazy
loading, package bundling, the Image component, the Next.js blog) and web.dev on Web Vitals, as read on 28
September 2026. It covers the App Router, not the Pages Router or React Native in detail. Library-specific
advice (data libraries, state managers, hosting) is out of scope: read that library's own docs.
