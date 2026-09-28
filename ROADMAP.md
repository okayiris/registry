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
| 5 | `dutch-vat-zzp` | moneybird | VAT returns, the small business scheme (KOR), reverse charge, deadlines. |
| 6 | `dutch-invoice-requirements` | moneybird, stripe | What a Dutch invoice must show, and how long to keep it. |
| 7 | `acting-on-behalf` | whatsapp, google-workspace, microsoft-365, x, socials | Drafting in the owner's voice, what always waits for a yes, what never gets sent. |
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

## Plugins worth building (outside this repository)

Found while checking the marketplace; they belong at plugins.okayiris.com, not here: `kvk`,
`ns` (journeys and disruptions, needs a key), `bank-import` (CAMT.053 or CSV exports read and categorised in
the plugin's own database, no bank API), `notes` (a Markdown folder to search and add to).

## Order of work

1. `registry` 1.1.0 and `okayiris-registry` 1.1.0 (done, waiting for review).
2. `writing-an-mcp-server`, `web-fetch` and `dutch-laws` (done, waiting for review): they make every later
   entry faster and better sourced.
3. The skills next to existing plugins, starting with `dutch-vat-zzp` and `acting-on-behalf`, each citing
   the articles it relies on through `dutch-laws`.

One house may have at most 5 versions waiting for review per registry, so hand them in in small batches.
