#!/usr/bin/env python3
"""The shared registries as tools, for any MCP client: search skills, read one, look at the MCP directory
and at the plugin marketplace.

Why this exists: an assistant that can only see its own tools cannot discover what other people already
reconned or built. This server is small on purpose. It reads the three public registries over https and
hands back text: nothing is executed, nothing is installed from here, and no credential is needed or used.

  search_skills  query, tag?      the skills that match, with author, license and how many sources
  read_skill     name             the whole skill text, with its sources (the registry's Markdown twin)
  list_mcp       query, tag?      the MCP servers in the directory, with transport, tools and permissions
  read_mcp       name             one server's entry: how it is reached, what it may do
  list_plugins   query, category? the plugins in the marketplace, with their commands and permissions
  read_plugin    name             one plugin's manifest and README: what it does, what it needs

Install it in a house with `mcp install registry`, then its tools appear as mcp__registry__<tool>.
"""
import base64
import json
import sys
import urllib.parse
import urllib.request

SKILLS = "https://skills.okayiris.com"
MCP = "https://mcp.okayiris.com"
PLUGINS = "https://plugins.okayiris.com"
HOSTS = {urllib.parse.urlsplit(u).hostname for u in (SKILLS, MCP, PLUGINS)}
TIMEOUT = 20
VERSION = "1.1.0"

class UnknownTool(Exception):
    pass


TOOLS = [
    {"name": "search_skills", "description": "Find shared skills by word and, optionally, tag. Start here before answering a topic from memory: somebody may have reconned it already, and a skill names its sources.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "tag": {"type": "string"}}, "required": ["query"]}},
    {"name": "read_skill", "description": "Read one shared skill in full, as Markdown, including the sources it was written from.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "list_mcp", "description": "Find MCP servers in the shared directory, with their transport, their tools and what they may do.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "tag": {"type": "string"}}}},
    {"name": "read_mcp", "description": "Read one MCP server's entry: how it is reached, which tools it offers and the permissions it asks for.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "list_plugins", "description": "Find plugins in the Iris marketplace, with their commands and permissions. Look here before building a connection: a service may already be a plugin.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "category": {"type": "string"}}}},
    {"name": "read_plugin", "description": "Read one plugin's manifest and README: what it does, which commands it adds, what it needs from the owner and the permissions it asks for.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
]


def get(url):
    """Read a public page. https only, never off our own three hosts (also not by a redirect), a deadline on it."""
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": f"okayiris-registry-mcp/{VERSION}"}), timeout=TIMEOUT) as r:
        where = urllib.parse.urlsplit(r.geturl())
        if where.scheme != "https" or where.hostname not in HOSTS:
            raise ValueError(f"refused to read {where.scheme}://{where.hostname}: not one of the registries")
        return r.read().decode("utf8")


def search(entries, query, tag, field="tags"):
    words = [w for w in (query or "").lower().split() if w]
    out = []
    for e in entries:
        wanted = e.get(field) or []
        if tag and tag not in (wanted if isinstance(wanted, list) else [wanted]):
            continue
        hay = " ".join([str(e.get("name", "")), str(e.get("description", "")), str(e.get("author", "")), " ".join(e.get("tags") or []),
                        str(e.get("category", "")), " ".join(e.get("commands") or {})]).lower()
        if all(w in hay for w in words):
            out.append(e)
    return out


def entry_lines(entries, kind):
    if not entries:
        return f"Nothing in the {kind} registry matches that."
    rows = []
    for e in entries:
        rows.append("\n".join([
            f"- {e.get('name')} {e.get('versions', [''])[0]}",
            f"  {e.get('description')}",
            f"  by {e.get('author')} · {e.get('license')} · tags: {', '.join(e.get('tags') or []) or 'none'} · {len(e.get('sources') or [])} source(s)",
        ]))
    return "\n".join(rows)


def slug(args):
    return urllib.parse.quote(str(args.get("name", "")).strip().lower())


def call(name, args):
    if name == "search_skills":
        entries = json.loads(get(f"{SKILLS}/api/skills")).get("entries", [])
        return entry_lines(search(entries, args.get("query", ""), args.get("tag")), "skills")
    if name == "read_skill":
        return get(f"{SKILLS}/s/{slug(args)}.md")
    if name == "list_mcp":
        entries = json.loads(get(f"{MCP}/api/mcp")).get("entries", [])
        found = search(entries, args.get("query", ""), args.get("tag"))
        if not found:
            return "Nothing in the MCP directory matches that."
        return "\n\n".join("\n".join([
            f"- {e.get('name')} {e.get('versions', [''])[0]} [{e.get('transport')}]",
            f"  {e.get('description')}",
            f"  tools: {', '.join(t.get('name', '') for t in (e.get('tools') or [])[:8]) or 'see the server'}",
            f"  may: {', '.join(e.get('permissions') or []) or 'nothing'} · by {e.get('author')} · {e.get('license')}",
        ]) for e in found)
    if name == "read_mcp":
        return get(f"{MCP}/m/{slug(args)}.md")
    if name == "list_plugins":
        entries = json.loads(get(f"{PLUGINS}/api/plugins")).get("plugins", [])
        found = search(entries, args.get("query", ""), args.get("category"), field="category")
        if not found:
            return "Nothing in the plugin marketplace matches that."
        return "\n\n".join("\n".join([
            f"- {e.get('name')} {e.get('version')} [{e.get('category') or 'other'}]",
            f"  {e.get('description')}",
            f"  commands: {', '.join(e.get('commands') or {}) or 'none'}",
            f"  may: {', '.join(e.get('permissions') or []) or 'nothing'} · by {e.get('author')}",
        ]) for e in found)
    if name == "read_plugin":
        package = json.loads(get(f"{PLUGINS}/api/plugins/{slug(args)}"))
        readme = (package.get("files") or {}).get("README.md")
        return "\n\n".join([
            "plugin.json:\n" + json.dumps(package.get("manifest"), indent=2, ensure_ascii=False),
            f"hash: {package.get('hash')}",
            base64.b64decode(readme).decode("utf8") if readme else "This plugin has no README.",
        ])
    raise UnknownTool(f"no tool called {name}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        method = message.get("method")
        if "id" not in message:                                       # a notification: nothing to answer
            continue
        try:
            if method == "initialize":
                result = {"protocolVersion": message.get("params", {}).get("protocolVersion", "2024-11-05"),
                          "capabilities": {"tools": {}}, "serverInfo": {"name": "registry", "version": VERSION}}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                params = message.get("params") or {}
                try:
                    result = {"content": [{"type": "text", "text": call(params.get("name"), params.get("arguments") or {})}]}
                except UnknownTool:
                    raise
                except Exception as e:                                # the tool failed: the model reads why
                    result = {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True}
            else:
                raise NotImplementedError(method)
            out = {"jsonrpc": "2.0", "id": message["id"], "result": result}
        except NotImplementedError as e:                              # a method this server does not speak
            out = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": f"no method {e}"}}
        except UnknownTool as e:                                      # an unknown tool is a bad request
            out = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32602, "message": str(e)}}
        except Exception as e:                                        # a refusal the client can read
            out = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"}}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
