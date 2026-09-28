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
| [okayiris-registry](skills/okayiris-registry) | Work with the shared Iris registries: find and use skills, MCP servers and plugins, and hand in what you reconned and researched so every other house gets it too. | Iris | CC-BY-4.0 |
| [writing-an-mcp-server](skills/writing-an-mcp-server) | How to write an MCP server for the shared registry that works with old and new MCP clients, asks for no more than it needs, and passes review the first time. | Iris | CC-BY-4.0 |
| [acting-on-behalf](skills/acting-on-behalf) | How an assistant writes, sends, posts and calls in its owner's name - what always waits for a yes, what counts as one, how to draft in the owner's voice, and what never goes out. | Iris | CC-BY-4.0 |
| [dutch-vat-zzp](skills/dutch-vat-zzp) | How Dutch VAT (btw) works for a sole trader (zzp'er) - rates, the small business scheme (KOR), invoices, filing deadlines, reverse charge, EU clients and correcting a return. | Iris | CC-BY-4.0 |

## MCP servers

| Name | What it is | By | License |
|---|---|---|---|
| [registry](mcp/registry) | Search the shared skills, the MCP directory and the plugin marketplace, so an assistant can use what every other house already reconned or built. | Iris | MIT |
| [web-fetch](mcp/web-fetch) | Read one public web page as Markdown, so an assistant can read a source itself instead of answering from memory. | Iris | MIT |
| [dutch-laws](mcp/dutch-laws) | Find a Dutch law and read one article exactly as it was in force on a given date, from the government's own open data, with a link to cite. | Iris | MIT |

## What comes next

What we still want to build, and why it is a skill, a server or a plugin: [ROADMAP.md](ROADMAP.md). What
other agent systems install most, and where the gap is: [LANDSCAPE.md](LANDSCAPE.md).

## Adding one

An Iris house submits a version, a person reviews it, and it lands here. You can also write one and open a
pull request: put it in `skills/<name>/` or `mcp/<name>/`, the folder name equal to the name in
`skill.json` or `mcp.json`, with its sources and its license. A pull request follows the same review as a
submission, and it is welcome: the point of this repository is that the knowledge is shared.

The rules in short: text only for a skill (no code), no secrets anywhere (every credential is a reference),
https only for a remote server, one flat folder per entry, and a version that never changes once it is here.
