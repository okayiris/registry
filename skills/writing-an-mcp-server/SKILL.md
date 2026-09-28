---
name: writing-an-mcp-server
description: How to write an MCP server for the shared registry that works with old and new MCP clients, asks for no more than it needs, and passes review the first time.
whenToUse: When someone says "make an MCP server for ...", "can other assistants use this too", "wrap this API as tools", when you are about to hand in a server with `mcp publish`, or when a server you wrote does not show up, hangs, or its tools fail silently in a client.
---

# Writing an MCP server

## What it is

An MCP server gives an assistant tools. For this registry it is one flat folder: an `mcp.json` that says
what the server is and may do, and, for a local server, the server itself as one `.py` or `.js` file in that
same folder. A person reads every submission before it is published, and a published version never changes.

First check that it should be a server at all:

- Knowledge (how something works, what to check) is a **skill**. No code.
- A service used only inside Iris, with a window, a slash command or a key from the vault, is usually a
  **plugin** (plugins.okayiris.com). Look there first; the service may already be one.
- A server is for tools that **any** MCP client should be able to use.

## The two shapes

| Transport | What you hand in | Where it runs |
|---|---|---|
| `stdio` | `mcp.json` plus the server file, `command` naming that file | In the house's own sandbox, started by the client |
| `streamable-http` | Only `mcp.json`, with an `https` `url` | Wherever that address is |

A `stdio` package must be complete: it may not download anything when it starts, and its `command` must
be a file in the folder. Python 3 with only its standard library is the easiest to review and to run.

## Speak both eras of the protocol

The MCP specification changed shape in revision **2026-07-28**. Clients from before it (**legacy**:
2025-11-25 and earlier) open with an `initialize` handshake. Clients from after it (**modern**) send no
handshake; every request carries its protocol version and the client's capabilities in
`params._meta`, under `io.modelcontextprotocol/protocolVersion` and
`io.modelcontextprotocol/clientCapabilities`. You do not know which one a house runs, so answer both. A
server that does is called dual-era, and the spec allows it.

A tools-only server that keeps no state needs just this:

1. **`initialize`** (legacy): answer `protocolVersion` (the one asked for when you support it, otherwise
   your newest legacy one), `capabilities: {"tools": {}}`, and `serverInfo` with `name` and `version`.
2. **`server/discover`** (modern, required): answer `supportedVersions`, `capabilities`, and, like every
   modern result, `resultType: "complete"`. It is cacheable, so it also needs `ttlMs` and `cacheScope`
   (`"public"` when nothing in it is about one user).
3. **A version you do not know** in `_meta`: answer error `-32022` with
   `data: {"supported": [...], "requested": "..."}`, so the client can retry with one you do.
4. **`tools/list`**: the tools, in the same order every time, plus `resultType`, `ttlMs` and `cacheScope`.
5. **`tools/call`**: see errors below. Put `resultType: "complete"` on every result; a legacy client ignores
   it. Identify yourself in each result's `_meta` as `io.modelcontextprotocol/serverInfo`.
6. **Notifications** (a message without an `id`, like `notifications/initialized` or
   `notifications/cancelled`): never answer them.
7. **`ping`** is gone in the modern era. Answering it with `{}` for legacy clients costs nothing.

An unknown method is `-32601`. Keep your own error codes out of `-32020` to `-32099`: that range is
reserved for the specification.

## stdio rules that break servers

- One JSON-RPC message per line on stdout, no newlines inside a message. `json.dumps` without `indent` does
  this.
- **Nothing else on stdout.** A stray `print` for debugging corrupts the stream and the client drops the
  server. Log to stderr.
- Flush after every message.
- Exit when stdin closes. That is how a client stops you; `for line in sys.stdin` does it for you.
- JSON that does not parse gets error `-32700` with `id: null`, and then the server carries on.

## Two kinds of errors

This is the one most servers get wrong, and it decides whether the model can recover:

- **The tool ran and failed** (a 404 from the API, a date in the wrong format, nothing found): return a
  normal result with `isError: true` and one sentence the model can act on ("a date is YYYY-MM-DD, not
  28-09"). The model reads it and tries again.
- **The request itself is wrong** (a tool that does not exist, arguments that do not fit the schema):
  a JSON-RPC error, `-32602`. A client may not show these to the model at all.

Raising an exception out of a tool, so it becomes a JSON-RPC error, hides a fixable mistake from the model.

## Tools the model can use well

- Tool names: ASCII letters, digits, `_`, `-` and `.`, at most 128 characters, unique within the server.
  Clients mix tools from many servers, so a plain `search` is easy to confuse; `search_laws` is not.
- The `description` is for the model: say when to use the tool and what comes back, not how it is built.
- Give every argument a `description` and mark what is `required` in the `inputSchema`.
- Keep the output short and readable. It is an answer, not a log. Split long text into parts and say how
  to read on ("ask again with start=20000").
- Put the source in the answer: the address the data came from, the date it holds for. An assistant that
  can cite it will.

## Permissions and secrets

`permissions` picks from `internet`, `files`, `secrets`, `phone`, `voice` and `messages`. People read the
list before they install, and a version that asks for more is never swapped in without their yes. Ask for
exactly what the code does. A server that only reads public pages needs only `internet`.

No value of a secret goes anywhere in the folder. `env` holds references (`"$GITHUB_TOKEN"` or
`"vault:github"`). A written-out token is refused before a person even reads the submission.

A server that fetches addresses it is given must refuse addresses inside a network (localhost, private and
link-local ranges such as `169.254.169.254`), and check again on every redirect. Otherwise a page can talk
it into reading something that is not public.

The spec also asks servers to validate every input and to sanitize what they return. Check an identifier
against its pattern before it goes into a URL, and read only from the hosts the server is for.

## Test it before you hand it in

```sh
cd ~/mcp/<name>
mcp check        # is the folder right? changes nothing
mcp try          # starts it the way a client would and lists its tools
```

Also feed it lines by hand, once per era:

```sh
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25"}}' \
  '{"jsonrpc":"2.0","id":2,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"nope"}}' \
  | python3 server.py
```

Expect three answers: a handshake, a discover result with `resultType`, and a `-32602` error. Then call
every tool once with good arguments and once with bad ones. A bad argument should come back as `isError`.

## What the review checks

- Does `mcp.json` describe what the server really does, and do its `sources` say so?
- Do the `permissions` match the code?
- Does the owner's data stay in the house?
- Is a `stdio` package complete, and does it start?
- 1 to 12 `https` sources, a `license` from the allowed list, a name equal to the folder, and a version
  number that was never published before.

## Where this stops

This follows the specification as of revision 2026-07-28. The specification moves: read its changelog
before relying on a detail, and change the supported version lists when a new revision comes out. This
skill covers tools only. Resources, prompts, subscriptions, multi-round-trip requests and authorization for
remote servers are in the specification, not here.
