# Roadmap

What this registry still needs, in the order we want to build it. Checked against the plugin marketplace
(plugins.okayiris.com, 28 plugins on 2026-09-28): a service that is already a plugin is not rebuilt here as an
MCP server. Where a plugin does the calls, the gap is usually a skill that knows the domain behind it.

## Skill, server or plugin

- **Knowledge** (how something works, what to check, what the rules are): a skill, here in `skills/`.
- **A service for Iris** (a command, a window, a slash command, a page on the house's address, a key from
  the vault): a plugin, in the marketplace, not in this repository.
- **A service other MCP clients should be able to use as well**, or one that already is an MCP server
  somewhere: an MCP server, here in `mcp/`.

Already a plugin, so not an MCP server here: github, calendars, family-agenda, google-workspace,
microsoft-365, mailbox, maillog, whatsapp, telegram, x, socials, phone, voices, homeassistant, search, maps,
travel, parcels, moneybird, stripe, google-ads, spotify, youtube, openrouter, node, process-monitor, meals.

## Done

- [x] `registry` 1.1.0 (MCP): also searches and reads the plugin marketplace; tool failures come back as
  `isError` results as the MCP spec asks, `ping` is answered, and reads stay on the three registry hosts,
  also across a redirect.
- [x] `okayiris-registry` 1.1.0 (skill): names the tools as they exist in a house, as house commands and
  as the registry MCP server; adds plugins as the third shelf and says when to build which.
- [x] `writing-an-mcp-server` 1.0.0 (skill): the two protocol eras, stdio pitfalls, tool errors against
  protocol errors, permissions, testing and review.
- [x] `web-fetch` 1.0.0 (MCP): one public page as Markdown, refusing addresses inside a network.
- [x] `dutch-laws` 1.0.0 (MCP): Dutch laws and articles as in force on a date, from the BWB open data.
- [x] `dutch-vat-zzp` 1.0.0 and `acting-on-behalf` 1.0.0 (skills).

All three servers are dual-era: they answer legacy clients (`initialize`, 2025-11-25 and earlier) and
modern ones (`server/discover` and per-request `_meta`, 2026-07-28), because MCP dropped the handshake in
its 2026-07-28 revision and a house may run either.

## MCP servers

All read-only, no key, open data: they need only `internet`, which makes them easy to review and to trust.

| # | Name | Category | What it does | Permissions |
|---|---|---|---|---|
| 1 | ~~`web-fetch`~~ (done) | knowledge | Read one public page as Markdown, for the research step of a skill. The `search` plugin finds pages; nothing reads them yet. | internet |
| 2 | ~~`dutch-laws`~~ (done) | knowledge | Look up Dutch legislation and a specific article on wetten.overheid.nl, with the version valid on a given date. Backs every NL skill with a primary source. | internet |
| 3 | `pdok` | knowledge | Addresses, postcodes and buildings from the BAG through PDOK's locatieserver. | internet |
| 4 | `rdw` | knowledge | Vehicle data by licence plate from the RDW open data. | internet |
| 5 | `cbs` | knowledge | Figures from CBS StatLine (inflation, population, prices) with the table they came from. | internet |
| 6 | `weather` | home | Forecast and warnings through a keyless open weather API. | internet |

Later, only when someone asks: `kvk` (company register, needs a key: likely a plugin rather than a server),
`rechtspraak` (published court decisions, open data), and `streamable-http` listings for well-known hosted
servers, which need no code here, only a reviewed `mcp.json`.

## Skills

Text only, sources named, `CC-BY-4.0` unless there is a reason for another.

### How we work

| # | Name | What it knows |
|---|---|---|
| 1 | ~~`writing-an-mcp-server`~~ (done) | stdio against streamable-http, the JSON-RPC handshake, tool errors against protocol errors, stdout for messages only, the smallest honest permission list, `env` as references. |
| 2 | `reviewing-a-submission` | The reviewer's checklist for all three shelves: sources that say what the text says, nothing personal, no secrets, permissions that match the code. |
| 3 | `source-checking` | Primary against secondary sources, a second independent one for anything surprising, the date a rule is valid from. |
| 4 | `permissions-explained` | Each of the six permissions in plain words, to read out to an owner before an install. |

### Next to a plugin that already exists

| # | Name | Next to | What it knows |
|---|---|---|---|
| 5 | ~~`dutch-vat-zzp`~~ (done) | moneybird | VAT returns, the small business scheme (KOR), reverse charge, deadlines. |
| 6 | `dutch-invoice-requirements` | moneybird, stripe | What a Dutch invoice must show, and how long to keep it. |
| 7 | ~~`acting-on-behalf`~~ (done) | whatsapp, google-workspace, microsoft-365, x, socials | Drafting in the owner's voice, what always waits for a yes, what never gets sent. |
| 8 | `scheduling` | calendars, family-agenda | Time zones, buffers, overlapping agendas, declining politely. |
| 9 | `saas-metrics` | stripe | MRR, churn, refunds and what the numbers do and do not say. |
| 10 | `ads-reporting` | google-ads | Reading spend, CPC, conversions and ROAS without overclaiming. |
| 11 | `home-automation-safety` | homeassistant | What may be switched without asking (lights) and what never is (locks, heating at night, alarms). |
| 12 | `git-workflow` | github | Branches, commits, pull requests and review etiquette. |

### Dutch life and work

| # | Name | What it knows |
|---|---|---|
| 13 | `dutch-tax` | Income tax for one employer and a side income (the example in the skills docs). |
| 14 | `starting-as-zzp` | Registering at the KVK, VAT number, insurance, the hours criterion. |
| 15 | `toeslagen` | Healthcare, rent and childcare allowance, and paying back. |
| 16 | `huurrecht` | Rent increases, the points system, the rent tribunal. |
| 17 | `avg-basics` | What the GDPR allows with personal data, for a small business. |
| 18 | `government-doors` | Which matter goes through DigiD, MijnOverheid, the tax office or the municipality. |

### Personal and soft skills

The gap found in [LANDSCAPE.md](LANDSCAPE.md): other directories are full of skills for building software,
and almost empty for a person's own life. Iris lives with one owner, so these come first. Each is written
from the research or the professional standard behind it, not from general advice. The sources named are
where the research starts.

| # | Name | What it knows | Research starts at |
|---|---|---|---|
| 19 | `asking-good-questions` | Doorvragen: one open question at a time, summarising back, asking what is really meant before acting, knowing when to stop asking. | Motivational interviewing (OARS), SAMHSA TIP 35 |
| 20 | `personal-triage` | Sorting what comes in (mail, messages, requests, tasks) into now, today, this week, someone else, or never, and telling the owner only what needs them. | Getting Things Done (clarify, two-minute rule), the urgent/important matrix |
| 21 | `daily-and-weekly-review` | A short start of the day and a weekly review: what is open, what is next, what can go. | GTD weekly review |
| 22 | `planning-a-day` | A realistic day: fixed appointments first, time blocks, buffers, energy, and saying what will not fit. | Timeboxing, planning-fallacy research |
| 23 | `coaching-conversation` | Helping the owner think instead of telling them: goal, reality, options, will (GROW), and not giving advice too early. | ICF core competencies, GROW model |
| 24 | `learning-something-new` | Teaching the owner a topic: tied to why they want it, small steps, retrieval practice, spacing, checking understanding. | Dunlosky et al. (2013), learning-sciences summaries |
| 25 | `building-habits` | Small habits, when-then plans, tracking without guilt, restarting after a lapse. | Implementation intentions (Gollwitzer), habit formation (Lally et al.) |
| 26 | `encouragement` | Motivating without pressure: autonomy, competence, connection; noticing progress; no guilt, no nagging. | Self-determination theory |
| 27 | `calm-and-rest` | Rest, sleep and stress in plain words, what an assistant can do (fewer interruptions, a quieter day) and where it must refer: the GP, and 113 in a crisis. Never therapy. | Thuisarts.nl (NHG), 113 Zelfmoordpreventie |
| 28 | `making-decisions` | Reversible or not, what would change the owner's mind, a pre-mortem, and leaving the choice with the owner. | Decision research (pre-mortem, Klein) |
| 29 | `difficult-conversations` | Preparing a hard talk or message: observation, feeling, need, request; giving and receiving feedback. | Nonviolent Communication (CNVC) |
| 30 | `private-assistant-discretion` | What an assistant remembers, what it forgets on request, what it never repeats, and how it keeps one person's life private from everyone else. | AVG/GDPR, Autoriteit Persoonsgegevens |

### Craft skills

The most-installed skills elsewhere (see [LANDSCAPE.md](LANDSCAPE.md)), written again from primary sources
so they can carry our license and our review. Only text; the tool-heavy ones are plugins.

| # | Name | What it knows | Primary sources |
|---|---|---|---|
| 31 | `frontend-design` | Choosing an aesthetic first, then type, colour, space and motion; avoiding the generic look. | W3C, web.dev, type and colour references |
| 32 | `web-interface-guidelines` | Accessibility and interface details: focus, contrast, forms, touch targets, reduced motion. | WCAG 2.2, WAI-ARIA Authoring Practices |
| 33 | `react-performance` | Waterfalls, bundle size, re-renders, server and client components. | react.dev, Next.js docs, web.dev Core Web Vitals |
| 34 | `postgres-practices` | Indexes, query plans, connection pooling, row-level security, locking. | postgresql.org documentation |
| 35 | `debugging-method` | Root cause before a fix, one hypothesis at a time, stop after three failed fixes. | Engineering practice, cited where possible |
| 36 | `code-review` | Reviewing a change and asking for a review: correctness first, then clarity. | Google engineering practices |
| 37 | `test-driven-development` | Red, green, refactor, and what a good failing test looks like. | Kent Beck, Martin Fowler |
| 38 | `motion-design` | Interface motion that helps: timing, easing, purpose, and respecting reduced motion. | WCAG 2.2 (animation), platform motion guidelines |
| 39 | `seo-basics` | What search engines actually document: crawling, titles, structured data, helpful content. | Google Search Central |
| 40 | `plain-language` | Writing so everyone understands, in Dutch at B1 level and in English. | Rijksoverheid (B1), plainlanguage.gov |
| 41 | `from-conversation-to-spec` | Turning a talk into a clear plan or spec, with open questions listed. | Requirements practice |

## Plugins worth building (outside this repository)

Found while checking the marketplace; they belong at plugins.okayiris.com, not here: `kvk`,
`ns` (journeys and disruptions, needs a key), `bank-import` (CAMT.053 or CSV exports read and categorised in
the plugin's own database, no bank API), `notes` (a Markdown folder to search and add to).

## Order of work

1. `registry` 1.1.0 and `okayiris-registry` 1.1.0 (done, waiting for review).
2. `writing-an-mcp-server`, `web-fetch` and `dutch-laws` (done, waiting for review): they make every later
   entry faster and better sourced.
3. The skills next to existing plugins: `dutch-vat-zzp` and `acting-on-behalf` are done.
4. The personal and soft skills, starting with `asking-good-questions`, `personal-triage` and
   `calm-and-rest`: that is where other directories are empty and where Iris differs.
5. Then the rest of the list, alternating craft skills with the Dutch ones.

One house may have at most 5 versions waiting for review per registry, so hand them in in small batches.
