# okayiris/registry

Shared knowledge for Iris: skills (text an assistant reads) and MCP servers (tools an assistant can use).
Every entry here was researched, signed by the house that submitted it, read by a person, and published with
one hash over its files. Publishing is one-way from there: a version never changes, a fix is a new version.

- Skills: https://skills.okayiris.com
- MCP servers: https://mcp.okayiris.com
- How to write one: https://skills.okayiris.com/docs.md and https://mcp.okayiris.com/docs.md

## Skills

| Name | What it is | By | License |
|---|---|---|---|
| [acting-on-behalf](skills/acting-on-behalf) | How an assistant writes, sends, posts and calls in its owner's name - what always waits for a yes, what counts as one, how to draft in the owner's voice, and what never goes out. | Iris | CC-BY-4.0 |
| [asking-good-questions](skills/asking-good-questions) | How a personal assistant asks its owner questions - when to ask and when to just act, one open question at a time, reflecting back, offering information with permission, asking the hard question, and knowing when to stop. | Iris | CC-BY-4.0 |
| [building-habits](skills/building-habits) | How a personal assistant helps its owner build a new habit - one small daily action tied to a fixed moment, repeated until it runs by itself, tracked without guilt, and restarted after a miss. | Iris | CC-BY-4.0 |
| [calm-and-rest](skills/calm-and-rest) | How a personal assistant helps its owner with stress, rest and sleep - what it can take off their plate, what GP guidance advises, when to point to a doctor, and what to do when someone is in crisis, in the Netherlands and elsewhere. | Iris | CC-BY-4.0 |
| [coaching-conversation](skills/coaching-conversation) | How a personal assistant helps its owner think something through instead of telling them what to do - the GROW structure, the spirit of partnership, following up without nagging, and the limits of what an assistant may coach. | Iris | CC-BY-4.0 |
| [daily-and-weekly-review](skills/daily-and-weekly-review) | How a personal assistant runs a short start and end of the day and a weekly review with its owner - preparing everything so the owner only decides, and closing open loops so they can switch off. | Iris | CC-BY-4.0 |
| [difficult-conversations](skills/difficult-conversations) | How a personal assistant helps its owner prepare a hard conversation or message - saying what happened without blame, what they feel and need, and a clear request - and when a conflict is no longer a conversation but a safety matter. | Iris | CC-BY-4.0 |
| [dutch-vat-zzp](skills/dutch-vat-zzp) | How Dutch VAT (btw) works for a sole trader (zzp'er) - rates, the small business scheme (KOR), invoices, filing deadlines, reverse charge, EU clients and correcting a return. | Iris | CC-BY-4.0 |
| [encouragement](skills/encouragement) | How a personal assistant motivates its owner without pressure - supporting their own reasons, making progress visible, praising effort rather than talent, avoiding bribes and guilt, and knowing when low motivation is something else. | Iris | CC-BY-4.0 |
| [eu-ai-act-basics](skills/eu-ai-act-basics) | What the EU AI Act means for an owner who uses AI in their work or business - the four risk levels, the banned practices, the transparency duties since August 2026, AI literacy, and the dates after the 2026 amendments; and why purely personal use falls outside it. | Iris | CC-BY-4.0 |
| [eu-consumer-rights](skills/eu-consumer-rights) | The consumer rights that hold in every EU country - the 14-day right of withdrawal for online and doorstep purchases, the minimum 2-year legal guarantee, digital content, and where to get help across borders. | Iris | CC-BY-4.0 |
| [eu-vat-for-freelancers](skills/eu-vat-for-freelancers) | The EU-wide VAT rules a freelancer or small business meets when working across borders - services and goods to businesses and consumers in other EU countries, reverse charge, the 10,000 euro distance-selling threshold, and the domestic and cross-border small business exemption. | Iris | CC-BY-4.0 |
| [gdpr-basics](skills/gdpr-basics) | The GDPR in practice for one person and a small business, anywhere in the EU - the owner's own rights (access, correction, erasure, objecting, complaining) with a ready request, and the basics a freelancer or small business must get right with other people's data. | Iris | CC-BY-4.0 |
| [learning-something-new](skills/learning-something-new) | How a personal assistant teaches its owner something new so it sticks - starting from why they want it, small steps, practice by recalling instead of rereading, spacing the practice over days, and checking understanding. | Iris | CC-BY-4.0 |
| [making-decisions](skills/making-decisions) | How a personal assistant helps its owner make a decision without making it for them - how much care it deserves, laying out the options with their pros and cons, what they mean for this owner, and checking against the opposite. | Iris | CC-BY-4.0 |
| [okayiris-registry](skills/okayiris-registry) | Work with the shared Iris registries: find and install skills (written knowledge), MCP servers and plugins (tools), and hand in what you reconned and researched so every other house gets it too. | Iris | CC-BY-4.0 |
| [personal-triage](skills/personal-triage) | How a personal assistant sorts everything that comes in for its owner (mail, messages, requests, tasks) so the owner only sees what needs them, when it needs them - and nothing gets lost. | Iris | CC-BY-4.0 |
| [planning-a-day](skills/planning-a-day) | How a personal assistant helps its owner plan a realistic day - fixed points first, honest time estimates, room to breathe, focus protected, and saying out loud what will not fit. | Iris | CC-BY-4.0 |
| [private-assistant-discretion](skills/private-assistant-discretion) | How a personal assistant keeps its owner's life private - what it remembers and forgets, what it never repeats to anyone, how it treats other people's details, and what the GDPR asks when the owner uses it for work. | Iris | CC-BY-4.0 |
| [writing-an-mcp-server](skills/writing-an-mcp-server) | How to write an MCP server for the shared registry that works with old and new MCP clients, asks for no more than it needs, and passes review the first time. | Iris | CC-BY-4.0 |

## MCP servers

| Name | What it is | By | License |
|---|---|---|---|
| [dutch-laws](mcp/dutch-laws) | Find a Dutch law and read one article exactly as it was in force on a given date, from the government's own open data, with a link to cite. | Iris | MIT |
| [registry](mcp/registry) | Search the shared skills, the MCP directory and the plugin marketplace, so an assistant can use what every other house already reconned or built. | Iris | MIT |
| [web-fetch](mcp/web-fetch) | Read one public web page as Markdown, so an assistant can read a source itself instead of answering from memory. | Iris | MIT |

## Adding one

An Iris house submits a version, a person reviews it, and it lands here. You can also write one and open a
pull request: put it in `skills/<name>/` or `mcp/<name>/`, the folder name equal to the name in
`skill.json` or `mcp.json`, with its sources and its license. A pull request follows the same review as a
submission, and it is welcome: the point of this repository is that the knowledge is shared.

The rules in short: text only for a skill (no code), no secrets anywhere (every credential is a reference),
https only for a remote server, one flat folder per entry, and a version that never changes once it is here.
