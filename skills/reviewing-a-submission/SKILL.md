---
name: reviewing-a-submission
description: The reviewer's checklist for skills, MCP servers and plugins handed in to the Iris registries - sources that say what the text says, nothing personal, no secrets, permissions that match the code, self-contained stdio packages, names, versions and licenses, and what the store already refused.
whenToUse: When the operator says "kijk je even deze inzending na", "review this skill", "is this server safe to publish", "wat vind je van deze plugin", when a submission is waiting in the review queue, or before the owner hands in their own skill, server or plugin and wants it to pass the first time.
---

# Reviewing a submission

## What it is

Every skill, MCP server and plugin that is handed in to the Iris registries waits for a person to read it.
Nothing is published without that step, and a published version never changes: a fix is a new version. So
the review is the one moment a mistake can still be stopped cheaply.

This skill is the checklist for that read. The assistant prepares it: it opens the files, reads the
sources, runs the checks and writes down what it found. **The operator decides.** The same list works for a
house checking its own work before `skills publish`, `mcp publish` or `plugin publish`.

## What the store already refused

A submission reaches a person only after the store's own checks. Know them, so you do not spend time on
what cannot get through, and so you know what they do **not** cover.

| Shelf | Refused before a person reads it |
|---|---|
| Skill | Anything that is not text (`.py`, `.js`, `.sh`, binaries). Secrets: a private key, an API token, a password, a connection string with a password in it (the submitter is told which file and line). A name another house already published. A version that already exists. No sources, no license, or a frontmatter name that disagrees with `skill.json`. Over 256 kB, or a file name that could climb out of its folder. |
| MCP server | A secret in the package: every `env` value must be a reference (the file and key are named). `http://`, a bare IP, `localhost`, a `.internal` name or a private address range. Credentials in the URL (`https://user:pass@host`). A `command` that is not in the package, or a file a server has no business carrying (`.sh`, binaries). A name of another house, a version that exists, anything over 6 MB. |
| Plugin | The docs name a style gate for the first four design rules (only the kit, only the house colours, English code with `lang-en.json`, fits any size): a window or screen that breaks one is not shown and not accepted. The first home to publish a name owns it. |

Also on every shelf: one house may have at most 5 versions waiting in one registry, and hold at most 50 names
in one registry's store.

What these checks cannot tell you: whether the text is true, whether the permissions are honest, whether
the code sends the owner's data somewhere, or whether a secret is written in a shape the scan does not know.
That is the review.

## The checklist

Go through it in this order. Stop at the first real problem and write it down; you do not need ten reasons
to send something back.

### 1. Is it on the right shelf?

- Knowledge (how something works, what to check) is a **skill**, and a skill is text only.
- A service used inside Iris, with a command, a window, a page or a key from the vault, is a **plugin**.
- A service that other MCP clients must be able to use too is an **MCP server**.

The skills registry asks this question explicitly: is it a skill at all, or should it have been a plugin?

### 2. Do the sources say what the text says?

This is the heart of it, and the step most often skipped.

- Open every source. Skills and servers carry 1 to 12 `https` links. For a skill they are what the research
  actually read; for a server, the server's own documentation.
- For each number, date, deadline, rate or rule in the text, find the sentence in a source that says it.
  No sentence, no claim: it goes out, or it is stated plainly as experience rather than fact.
- Check that the source is the right kind: the tax office itself, the standard, the protocol, the manual of
  the thing. A blog summarising the law is weaker than the law (see `source-checking`).
- Check the date. A rule or a figure from last year may no longer hold.
- For a server or plugin: does the manifest's `description` and `tools` list match what the code really
  does? The server's own tool list is what counts once it runs.

### 3. Nothing personal

- No name, address, customer, case or conversation of a real person, in any file. A skill is general
  knowledge; anything about a person stays in that person's house.
- Examples must be invented. Plugin screenshots use made-up demo content, never someone's real messages or
  data.
- For a plugin with a database: personal data belongs in the owner's `data.db`, never in what is published.
- For a public plugin route (`public: true`): it must never show the owner's data, and never anyone's data
  without the key of the thing they are looking at.

### 4. No secrets

- `env` values are references only: `"$GITHUB_TOKEN"` or `"vault:github"`, never the value.
- A plugin never sees a secret: it asks the vault to make the call (`vault call ... {g}`). A plugin that
  reads a token from a file or a hard-coded string is wrong even if the scan missed it.
- Look for secrets in shapes a scan may miss: in a URL query, in an example, in a comment, in a screenshot.

### 5. Permissions that match the code

People read the permission list before they install, so it must be honest: not more than the code needs,
and not less than it does. Read the code and match it:

| If the code | It needs |
|---|---|
| fetches something from the internet | `internet` |
| reads or writes files outside its own folder | `files` |
| uses a key from the owner's vault | `secrets` |
| sends something to the owner's phone | `phone` |
| speaks or listens | `voice` |
| reads or sends messages in the owner's name | `messages` |

A permission that nothing in the code uses gets sent back. So does code that does something the list does
not name. See `permissions-explained` for the meaning of each one in plain words.

### 6. Does the owner's data stay in the house?

For a server or plugin, follow where data goes. Does it send the owner's data to an address that has
nothing to do with the job? A server that only reads public pages should only talk to those hosts.

### 7. Is a stdio server complete, and does it start?

- Its `command` is a file in its own flat folder. A listing can never start a program it does not carry.
- It downloads nothing when it starts: installing one never downloads anything.
- It comes up. `mcp try` starts it the way a client would and lists its tools. A server that does not come
  up is not a server.
- A remote server has only `mcp.json` with an `https` `url`: a name, not an IP, not a private address.

### 8. Names, versions, author

- The name equals the folder name, in lowercase letters, digits and `-` (at most 40 characters for a server
  or plugin), and for a skill equals the frontmatter `name`.
- The version is three numbers and was never published before; for a plugin, higher than the one listed.
- The `author` field is only what the submitter wrote it as. The registry stamps the entry with the house
  that submitted it; nothing a package claims can attribute work to somebody else.

### 9. License

| Shelf | Allowed licenses |
|---|---|
| Skill | `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, `MIT`, `Apache-2.0` |
| MCP server | `MIT`, `Apache-2.0`, `BSD-3-Clause`, `AGPL-3.0`, `MPL-2.0`, `proprietary` |

The plugin docs list no license field; check that the submitter may share what they hand in.

### 10. Will it be used at the right moment?

For a skill: is the `whenToUse` specific? It should name the sentences someone would actually say and the
situation, not only the topic. Is `description` one line, and the same in the frontmatter and `skill.json`?

For a plugin: does a command keep clear of existing names (it never replaces `web` or `klus`)? Does the
`README.md` say what the person needs, such as an account or an API key?

## Writing the verdict

- **Yes:** say so, with one line on what you checked.
- **No:** one sentence the submitter can act on. A rejected version is told why in one sentence.
  - "The 2026 rate in section 2 is not in any of the sources; add the tax office page or remove it."
  - "The code calls an outside API but `permissions` does not list `internet`."
  - "`config.json` holds a written-out token; make it `vault:<name>`."
- A rejected or waiting version can be fixed and handed in again with a **higher version**. While it is still
  waiting, the submitting house can also withdraw it.
- Once published, a version cannot be withdrawn. The way out is a takedown by whoever runs the registry; a
  plugin can be taken out in the admin panel, and a home that already installed it keeps its copy.

## What not to do

- Do not approve because the automatic checks passed. They catch shapes, not truth.
- Do not approve a claim because it sounds right. If you cannot find it in a source, it is not checked.
- Do not fix a submission yourself and approve your own version. Send it back with the reason.
- Do not copy anything personal from a submission into your notes or verdict.
- Do not decide for the operator. Prepare, list findings, recommend; they say yes or no.

## Where this stops

This follows the registries' own documentation at skills.okayiris.com, mcp.okayiris.com and
plugins.okayiris.com as of September 2026. Those pages are the rules; if they change, they win over this
list. It does not replace reading the code line by line for a server or plugin that asks for `secrets`,
`files` or `messages`. For the protocol details of a server, see `writing-an-mcp-server`; for how to hand
something in, see `okayiris-registry`.
