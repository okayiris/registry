---
name: permissions-explained
description: The six permissions an Iris plugin or MCP server can ask for (internet, files, secrets, phone, voice, messages) in plain words - what each lets it do, what to ask before saying yes, and how an update that asks for more is handled.
whenToUse: When the owner says "installeer die plugin maar", "wat betekent 'secrets'?", "is dit veilig?", "why does this want my messages", when you are about to install a plugin or MCP server and must read its permissions out loud, or when an update is waiting because it asks for more than before.
---

# Permissions explained

## What it is

A plugin or an MCP server brings real tools, so it says up front what it may do. That list is its
permissions, chosen from six: `internet`, `files`, `secrets`, `phone`, `voice` and `messages`. People read
it before they install, and a new version that asks for more is never put in without their yes.

This skill is what the assistant reads out to the owner before an install, in plain words, and what to ask
about each one. A **skill** is different: it is text, it reads nothing and runs nothing, and its permission
list is normally empty.

## The six, in plain words

| Permission | What the docs say | What to tell the owner |
|---|---|---|
| `internet` | Fetches something from the internet. | "Het kan dingen ophalen van internet, en dus ook dingen versturen naar een website." |
| `files` | Reads or writes files outside its own folder. | "It can read and change files of yours, not just its own." |
| `secrets` | Uses a key from the owner's vault (an API token, a login). | "Het mag een sleutel uit je kluis gebruiken, zoals je Moneybird-token, om namens jou in te loggen bij die dienst." |
| `phone` | Sends something to the owner's phone. | "It can send notifications or messages to your phone." |
| `voice` | Speaks or listens. | "Het kan praten, en het kan luisteren." |
| `messages` | Reads and sends messages in the owner's name (WhatsApp, mail, Telegram). | "It can read your messages and send messages as you." |

An **empty list** is fine, and it is trusted most.

## What each one really means, and what to ask

### internet

The most common one. Nearly every service lives on the internet. Anything that can fetch can also send, so
the question is **where** it talks to.

- Ask: which service or addresses does it talk to? Is that the service the owner asked for?
- A server that only reads public pages needs `internet` and nothing else.

### files

It can reach the owner's files outside its own folder. A plugin's own database (`data.db`) lives inside its
own folder and does not need this.

- Ask: which files, and why? Reading one folder of notes is different from writing anywhere.
- Say yes only when the job is about the owner's files.

### secrets

The plugin may use a key from the vault. How that works matters: **a plugin never sees the secret.** It asks
the vault to make the call and gets back only the answer. The token stays in the vault. When a key is
missing, the plugin should ask for it through a safe window (`vault ask`), not in the chat.

- Ask: which key, for which service? It should match the service the owner wants connected.
- Having the key means acting as the owner at that service, within what the key allows. A token that can
  only read is safer than one that can also pay or delete; that is decided at the service, when the owner
  makes the token.

### phone

It can send something to the owner's phone.

- Ask: how often, and about what? A reminder of an overdue invoice is useful; ten pings a day is not.

### voice

It can speak, listen, or both.

- Ask: does it listen, and when? Only while the owner is talking to it, or also otherwise? Where does the
  sound go?

### messages

The heaviest one. It can **read** the owner's messages and **send** messages in their name: WhatsApp, mail,
Telegram.

- Ask: does it need to read, to send, or both? For which conversations?
- Other people's words are in those messages. Say so.
- Even with this permission, sending in the owner's name still waits for the owner's yes, each time
  (see `acting-on-behalf`).
- A plugin or server that wants the vault or the owner's messages is a conversation, not a click.

## How to read it out before an install

1. Read the entry first: what it does, who made it, its permissions, and for a plugin its `usage` (what
   costs money once it runs; installing is always free).
2. Say each permission in plain words, using the table. Do not read out only the codes.
3. Say whether the list fits the job. "Het haalt je facturen op bij Moneybird: daarvoor heeft het internet
   en je Moneybird-sleutel nodig. Meer vraagt het niet."
4. If something does not fit, say so plainly. "It is a weather plugin but it asks for `messages`. I would
   not install this."
5. Wait for a clear yes that covers **every** permission on the list. Then install.

For an MCP server, the house's install tool refuses until the owner's yes covers everything the server asks
for (see `okayiris-registry`).

## Extra things to notice on a plugin

These are not permissions, but they are worth a sentence to the owner:

- **A public page** (`routes` with `public: true`): someone who is not signed in can open it. It should never
  show the owner's data.
- **A database** (`database: true`): the plugin keeps its own SQLite database in its own folder. Nothing of
  it leaves the house, and it stays when the plugin updates.
- **Costs** in `usage`: what a call or a text costs once it runs.

## Where a server runs

| Shape | Where it runs | What that means |
|---|---|---|
| `stdio` | Inside the house's own sandbox, with nothing of the registry's and no vault. | The code is in the package and was reviewed. |
| `streamable-http` | At whoever owns that `https` address. | Nothing of it runs in the house. What the owner sends it goes to that address. |

## Updates that ask for more

| Update | What happens |
|---|---|
| **Plugin**, same or fewer permissions | Every Iris checks the marketplace every ten minutes. It goes in by itself, and the owner gets a message. The owner can switch this off in the Marketplace screen; then they get a message that an update is waiting. |
| **Plugin**, asks for more | It waits. Iris asks her owner, and only on a yes runs `plugin update <name>`. |
| **MCP server**, asks for more | Never swapped in silently: the house asks its owner first. |

Folders the owner wrote themselves are never replaced; only plugins installed from the marketplace are.

When an update asks for more, say **what is new** and **why it might need it**: "De nieuwe versie wil ook
`phone`. Volgens de beschrijving stuurt hij nu een melding als een factuur te laat is. Wil je dat?" If the
reason is not clear from the entry, say that too. Saying no keeps the version the owner has.

## What not to do

- Do not install first and explain later.
- Do not summarise a list as "the usual permissions". Say each one.
- Do not treat a yes to one permission as a yes to all.
- Do not paste a key into the chat for a plugin; keys go into the vault through its own window.
- Do not promise a plugin is safe. The list says what it **may** do; a person reviewed it, but the owner
  decides whether they trust it.

## Where this stops

This follows the registries' own documentation at plugins.okayiris.com and mcp.okayiris.com as of September
2026. The six permissions and the update rules are defined there; if those pages change, they win. What a
key allows at the service itself (read only, or also pay or delete) is set at that service, not here.
