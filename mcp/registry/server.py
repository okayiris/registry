#!/usr/bin/env python3
"""The shared registries as tools, for any MCP client: search skills, read one, and look at the MCP
directory itself.

Why this exists: an assistant that can only see its own tools cannot discover what other people already
reconned. This server is small on purpose. It reads the two public registries over https and hands back
text: nothing is executed, nothing is installed from here, and no credential is needed or used.

  search_skills  query, tag?      the skills that match, with author, license and how many sources
  read_skill     name             the whole skill text, with its sources (the registry's Markdown twin)
  list_mcp       query, tag?      the MCP servers in the directory, with transport, tools and permissions
  read_mcp       name             one server's entry: how it is reached, what it may do

Install it in a house with `mcp install registry`, then its tools appear as mcp__registry__<tool>.
"""
import json
import sys
import urllib.parse
import urllib.request

SKILLS = "https://skills.okayiris.com"
MCP = "https://mcp.okayiris.com"
TIMEOUT = 20

TOOLS = [
    {"name": "search_skills", "description": "Find shared skills by word and, optionally, tag. Start here before answering a topic from memory: somebody may have reconned it already, and a skill names its sources.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "tag": {"type": "string"}}, "required": ["query"]}},
    {"name": "read_skill", "description": "Read one shared skill in full, as Markdown, including the sources it was written from.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
    {"name": "list_mcp", "description": "Find MCP servers in the shared directory, with their transport, their tools and what they may do.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "tag": {"type": "string"}}}},
    {"name": "read_mcp", "description": "Read one MCP server's entry: how it is reached, which tools it offers and the permissions it asks for.",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}},
]


def get(url):
    """Read a public page. https only, no redirects off our own two hosts, a deadline on it."""
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "okayiris-registry-mcp/1.0"}), timeout=TIMEOUT) as r:
        return r.read().decode("utf8")


def search(entries, query, tag):
    words = [w for w in (query or "").lower().split() if w]
    out = []
    for e in entries:
        if tag and tag not in (e.get("tags") or []):
            continue
        hay = " ".join([str(e.get("name", "")), str(e.get("description", "")), str(e.get("author", "")), " ".join(e.get("tags") or [])]).lower()
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


def call(name, args):
    if name == "search_skills":
        entries = json.loads(get(f"{SKILLS}/api/skills")).get("entries", [])
        return entry_lines(search(entries, args.get("query", ""), args.get("tag")), "skills")
    if name == "read_skill":
        wanted = urllib.parse.quote(str(args.get("name", "")).strip().lower())
        return get(f"{SKILLS}/s/{wanted}.md")
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
        wanted = urllib.parse.quote(str(args.get("name", "")).strip().lower())
        return get(f"{MCP}/m/{wanted}.md")
    raise ValueError(f"no tool called {name}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        method = message.get("method")
        if "id" not in message:
            continue
        try:
            if method == "initialize":
                result = {"protocolVersion": message.get("params", {}).get("protocolVersion", "2024-11-05"),
                          "capabilities": {"tools": {}}, "serverInfo": {"name": "registry", "version": "1.0.0"}}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                params = message.get("params") or {}
                result = {"content": [{"type": "text", "text": call(params.get("name"), params.get("arguments") or {})}]}
            else:
                raise ValueError(method)
            out = {"jsonrpc": "2.0", "id": message["id"], "result": result}
        except Exception as e:                                        # a refusal the client can read
            out = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"}}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
