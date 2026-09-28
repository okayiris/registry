---
name: okayiris-registry
description: Work with the shared Iris registries: find and install skills (written knowledge), MCP servers and plugins (tools), and hand in what you reconned and researched so every other house gets it too.
whenToUse: When a topic comes up you may not know well enough (tax, a protocol, a country's rules, a tool's real behaviour), when you are about to answer something a shared skill could have taught you, when someone asks for a new tool or connection, when someone wants a service connected ("can you do my Moneybird", "hook up my calendar"), or when you have just figured something out that is worth keeping.
---

# The shared registries

Three shelves hold what we know and what we built together:

- **skills.okayiris.com** — skills: text, an assistant reads them. How to recon a topic, how a discipline
  works, what to check before saying something is done, what not to claim.
- **mcp.okayiris.com** — MCP servers: tools, any MCP client can use them. Git, a database, a mailbox, a
  service.
- **plugins.okayiris.com** — plugins: commands, windows and pages inside one Iris. Most services an owner
  asks for (mail, calendars, GitHub, Moneybird, Home Assistant, WhatsApp) already live here.

A skill is text only. Nothing in one runs, gets a command, or changes anything by itself: it is knowledge,
with its sources named. A server or a plugin is the opposite: it brings real tools, so it asks for real
permissions and the owner has to agree to them.

## Which tools you have

The names differ by where you are; the steps below are the same.

| What | House tool | House command | Registry MCP server |
|---|---|---|---|
| Find a skill | `registry_skill_search` | `skills search "<words>"` | `mcp__registry__search_skills` |
| Read a skill | `registry_skill_read` | | `mcp__registry__read_skill` |
| Install a skill | `registry_skill_install` | `skills install <name>` | (read it, there is nothing to run) |
| Find a server | `registry_mcp_search` | `mcp search "<words>"` | `mcp__registry__list_mcp` |
| Read a server | `registry_mcp_read` | | `mcp__registry__read_mcp` |
| Install a server | `registry_mcp_install` | `mcp install <name>` | (not from here) |
| Find a plugin | | `plugin browse` | `mcp__registry__list_plugins` |
| Read a plugin | | | `mcp__registry__read_plugin` |
| Install a plugin | | `plugin install <name>` | (not from here) |
| Hand in | `registry_contribute` | `skills publish`, `mcp publish`, `plugin publish` | (a pull request) |

Use the first column you actually have. If none of them is there, the Markdown twins and the JSON catalogs
at the end of this skill are the door.

## Skill, server or plugin?

Before you build anything, decide which of the three it is:

- **It is knowledge** (how something works, what to check, what the rules are) → a **skill**. No code, ever.
- **It is a service, for Iris** (a command, a window, a slash command, a page on the house's address, an
  answer from a key in the vault) → a **plugin**. Look in the marketplace first: it may already be there.
- **It is a service that other MCP clients must be able to use too**, or one that is already an MCP server
  somewhere → an **MCP server**. Do not wrap a plugin that already exists in a server just to have both.

Often the right answer is a plugin plus a skill: the plugin does the calls, the skill knows the domain
(Moneybird does the bookkeeping; a skill knows what Dutch VAT asks of the invoices in it).

## Look before you write

Before you answer from memory, or before you build something that may already exist:

1. `registry_skill_search` with the words of the topic. Try both the plain word and the jargon.
2. `registry_skill_read` the closest match. Read the sources it names, not only its body: a skill is only as
   good as the pages behind it, and those pages may have moved on.
3. Use it, and say where it came from when you rely on it ("the shared skill on Dutch tax, from the tax
   office's own pages"). If it is wrong or thin, that is your cue to contribute a better version.
4. `registry_skill_install` what you will keep needing, so it sits among your own skills next time.

Do the same on the tool side before building a connection: search the plugins and the servers, then read
the closest one for its commands or tools, what it needs from the owner and what it may do.

## Installing a server or a plugin

Read its entry first, and read the permission list out loud to the owner in plain words. Then
`registry_mcp_install` with `acknowledge` naming exactly what the owner said yes to: the tool refuses until
that list covers everything the server asks for, on purpose. Its tools appear as `mcp__<name>__<tool>` once
the profile reloads. A plugin is the same conversation: read its permissions out loud, then
`plugin install <name>`. If a server or a plugin wants the vault or your owner's messages, that is a
conversation, not a click.

## Recon, research, write, hand in

This is the loop, and it is the whole point of sharing: one house researches something once and every house
benefits. A skill without sources is a guess with a title, and it gets sent back.

1. **Recon.** Write down what the topic actually is, who it matters to, what a good answer must contain, and
   what you do not know yet. Vague topics produce vague skills. If you cannot say what a wrong answer would
   look like, you are not ready to research it.
2. **Research.** Read the primary sources: the tax office itself, the standard, the protocol, the manual of
   the thing. Keep the links as you go, not afterwards. For anything that surprises you, find a second,
   independent source. Note the date on the rules: numbers from last year are wrong numbers.
3. **Write.** A folder `~/skills/<name>/` with two files:
   - `SKILL.md` — frontmatter (`name`, `description`, `whenToUse`) and a short body: what it is, how to work
     with it, what to check, what goes wrong, where the knowledge stops. Write `whenToUse` last and make it
     the sentences somebody would actually say.
   - `skill.json` — `name`, `version`, `author`, `description`, `tags`, `license`, and `sources` with the
     links you read.
4. **Hand in.** `registry_contribute` with the folder. It checks the format, the sources, the license and the
   secret scan, then submits: signed through the registry if this house has a house key, otherwise as a pull
   request against the public repository. Either way a person reads it before it is published. `dryRun: true`
   checks without submitting. With the house commands that is `skills check` (or `mcp check` and `mcp try`
   for a server, `plugin check` for a plugin), then `publish`.

```
~/skills/dutch-tax/
  SKILL.md
  skill.json
```

```json
{
  "name": "dutch-tax",
  "version": "1.0.0",
  "author": "the name your owner agreed to show",
  "description": "How Dutch income tax works for one employer and a side income.",
  "tags": ["tax", "nl"],
  "license": "CC-BY-4.0",
  "sources": ["https://www.belastingdienst.nl/..."]
}
```

## What never goes in

The store refuses it, and you should refuse it earlier:

- **Someone's data.** No names, addresses, customers, cases, conversations, invoice numbers. A skill is
  general knowledge; anything about a person stays in that person's house.
- **A secret.** No keys, tokens, passwords, connection strings. Every credential is a reference
  (`$GITHUB_TOKEN`, `vault:github`), never a value; the scan catches the obvious shapes and returns the
  submission to you.
- **Code in a skill.** No `.py`, `.js`, `.sh`: a folder with a program in it is a plugin or a server, not a
  skill.
- **A claim you cannot point at.** If no source says it, either find one or say plainly that this is your
  experience and not documented.
- **More permission than the job needs.** A server that only reads the internet does not need the vault.

## Serving what is already there

All three are also readable without any of this: every skill and server has a Markdown twin
(`skills.okayiris.com/s/<name>.md`, `mcp.okayiris.com/m/<name>.md`), and all three publish their catalog as
JSON (`/api/skills`, `/api/mcp`, `plugins.okayiris.com/api/plugins`) with one hash per version. A plugin's
README is inside its package at `plugins.okayiris.com/api/plugins/<name>`. If you are working outside a house, that is the
door: read the twin, keep the hash, say where it came from.
