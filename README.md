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
| [calm-and-rest](skills/calm-and-rest) | How a personal assistant helps its owner with stress, rest and sleep - what it can take off their plate, what the Dutch GP guidance advises, when to point to the GP, and what to do when someone is in crisis. | Iris | CC-BY-4.0 |
| [coaching-conversation](skills/coaching-conversation) | How a personal assistant helps its owner think something through instead of telling them what to do - the GROW structure, the spirit of partnership, following up without nagging, and the limits of what an assistant may coach. | Iris | CC-BY-4.0 |
| [okayiris-registry](skills/okayiris-registry) | Work with the shared Iris registries: find and use skills and MCP servers, and hand in what you reconned and researched so every other house gets it too. | Iris | CC-BY-4.0 |

## MCP servers

| Name | What it is | By | License |
|---|---|---|---|
| [registry](mcp/registry) | Search the shared skills and read an MCP server's entry, so an assistant can use what every other house already reconned. | Iris | MIT |

## Adding one

An Iris house submits a version, a person reviews it, and it lands here. You can also write one and open a
pull request: put it in `skills/<name>/` or `mcp/<name>/`, the folder name equal to the name in
`skill.json` or `mcp.json`, with its sources and its license. A pull request follows the same review as a
submission, and it is welcome: the point of this repository is that the knowledge is shared.

The rules in short: text only for a skill (no code), no secrets anywhere (every credential is a reference),
https only for a remote server, one flat folder per entry, and a version that never changes once it is here.
