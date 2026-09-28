#!/usr/bin/env python3
"""Read one public web page as Markdown, for any MCP client.

Why this exists: the research step of a skill means reading the primary source itself, not a summary of
it. A search finds the page; this reads it. It fetches exactly the address it is given, follows at most five
redirects, and hands back text: nothing is executed, nothing is stored, and no credential is sent.

  fetch   url, start?, max_chars?   the page as Markdown, with its title, final address and date

It refuses addresses inside a network (localhost, private and link-local ranges, `.internal` and `.local`
names), on every redirect as well, so a page cannot talk it into reading something that is not public.
"""
import html
import html.parser
import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

NAME = "web-fetch"
VERSION = "1.0.0"
INSTRUCTIONS = ("Reads one public web page as Markdown. Use it to read a source yourself instead of answering from "
                "memory, and keep the address you read so it can be named as a source.")
TIMEOUT = 20
MAX_BYTES = 5 * 1024 * 1024
MAX_REDIRECTS = 5
TEXT_TYPES = ("text/plain", "text/markdown", "text/csv", "application/json", "application/xml", "text/xml")

TOOLS = [
    {"name": "fetch", "description": "Read one public web page (http or https) as Markdown: its title, the address it ended up at, and the text with headings, lists, links and tables. Long pages come in parts: ask again with `start` to read on.",
     "inputSchema": {"type": "object", "properties": {
         "url": {"type": "string", "description": "The address to read."},
         "start": {"type": "integer", "minimum": 0, "description": "Where to start in the text, from the previous answer. Default 0."},
         "max_chars": {"type": "integer", "minimum": 1000, "maximum": 100000, "description": "How much text at most. Default 20000."}},
         "required": ["url"]}},
]


def public(url):
    """Refuse anything that is not a public http(s) address, before any byte is sent to it."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError(f"only http and https addresses, not {url}")
    if parts.username or parts.password:
        raise ValueError("no credentials in the address")
    host = parts.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith((".localhost", ".internal", ".local", ".home.arpa")):
        raise ValueError(f"{host} is not a public address")
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(host, parts.port or (443 if parts.scheme == "https" else 80))}
    except socket.gaierror:
        raise ValueError(f"{host} does not exist")
    for address in addresses:
        if not ipaddress.ip_address(address.split("%")[0]).is_global:
            raise ValueError(f"{host} points inside a network ({address})")
    return url


class Checked(urllib.request.HTTPRedirectHandler):
    """Every redirect is checked like the first address, and there are at most a few of them."""
    max_redirections = MAX_REDIRECTS

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req, fp, code, msg, headers, public(urllib.parse.urljoin(req.full_url, newurl)))


OPENER = urllib.request.build_opener(Checked)


class Markdown(html.parser.HTMLParser):
    """Just enough HTML to Markdown for reading: headings, paragraphs, lists, links, code and tables. When the
    page marks its content with <main>, only that is kept, without the menus around it."""
    SKIP = {"script", "style", "noscript", "svg", "template", "iframe", "form", "button", "select", "nav", "footer", "head"}
    BLOCK = {"p", "div", "section", "article", "main", "header", "aside", "figure", "figcaption", "dl", "dt", "dd",
             "blockquote", "address", "details", "summary"}

    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.out, self.title, self.skip, self.pre = base, [], "", 0, 0
        self.lists, self.href, self.in_title, self.row = [], None, False, None
        self.main, self.depth = None, 0                                    # where <main> starts and ends in out

    def emit(self, text):
        self.out.append(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "main":
            self.depth += 1
            if self.main is None:
                self.main = [len(self.out), None]
        if self.skip or tag in self.SKIP:
            self.skip += tag in self.SKIP and tag not in {"br", "img"}
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in self.BLOCK:
            self.emit("\n\n" + ("> " if tag == "blockquote" else ""))
        elif tag == "br":
            self.emit("\n")
        elif tag in ("ul", "ol"):
            self.lists.append([tag, 0])
            self.emit("\n")
        elif tag == "li":
            kind = self.lists[-1] if self.lists else ["ul", 0]
            kind[1] += 1
            self.emit("\n" + "  " * max(len(self.lists) - 1, 0) + (f"{kind[1]}. " if kind[0] == "ol" else "- "))
        elif tag == "pre":
            self.pre += 1
            self.emit("\n\n```\n")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "a" and attrs.get("href") and not attrs["href"].startswith(("javascript:", "#")):
            self.href = urllib.parse.urljoin(self.base, attrs["href"])
            self.emit("[")
        elif tag == "img" and attrs.get("alt"):
            self.emit(f"[image: {attrs['alt']}]")
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.row.append("")
        elif tag == "hr":
            self.emit("\n\n---\n\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "main" and self.depth:
            self.depth -= 1
            if not self.depth and self.main and self.main[1] is None:
                self.main[1] = len(self.out)
        if self.skip:
            self.skip -= tag in self.SKIP
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") or tag in self.BLOCK:
            self.emit("\n\n")
        elif tag in ("ul", "ol") and self.lists:
            self.lists.pop()
            self.emit("\n")
        elif tag == "pre" and self.pre:
            self.pre -= 1
            self.emit("\n```\n\n")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "a" and self.href:
            self.emit(f"]({self.href})")
            self.href = None
        elif tag == "tr" and self.row is not None:
            if any(cell.strip() for cell in self.row):
                self.emit("\n| " + " | ".join(" ".join(cell.split()) for cell in self.row) + " |")
            self.row = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.skip:
            return
        if self.row is not None and self.row:
            self.row[-1] += data
        elif self.pre:
            self.emit(data)
        else:
            self.emit(re.sub(r"\s+", " ", data))

    def text(self):
        whole = "".join(self.out)
        if self.main:                                                     # the page says where its content is
            content = "".join(self.out[self.main[0]:self.main[1]])
            whole = content if len(content.strip()) > 200 else whole
        joined = re.sub("[\u200b\u200c\u200d\ufeff]", "", whole)             # zero-width characters
        joined = re.sub(r"\[\s+", "[", re.sub(r"\s+\]\(", "](", joined))            # block tags inside a link
        joined = re.sub(r"(?m)^(#+)\s*\n+\s*(?=\S)", r"\1 ", joined)                  # a heading around an anchor
        joined = re.sub(r"(\*\*|\*)\s*\1", "", joined)                                 # empty bold or italic
        joined = re.sub(r"[ \t]+\n", "\n", joined)
        joined = re.sub(r"\n[ \t]+(?![-\d])", "\n", joined)
        return re.sub(r"\n{3,}", "\n\n", joined).strip()


def read(url):
    request = urllib.request.Request(public(url), headers={
        "User-Agent": f"okayiris-web-fetch/{VERSION} (+https://mcp.okayiris.com/m/web-fetch.md)",
        "Accept": "text/html, text/markdown;q=0.9, text/plain;q=0.8, application/json;q=0.5, */*;q=0.1"})
    try:
        response = OPENER.open(request, timeout=TIMEOUT)
    except urllib.error.HTTPError as e:
        raise ValueError(f"the page answered {e.code} {e.reason}")
    with response:
        body = response.read(MAX_BYTES + 1)
        kind = (response.headers.get_content_type() or "").lower()
        charset = response.headers.get_content_charset()
        return response.geturl(), response.status, kind, charset, response.headers.get("Last-Modified"), body


def fetch(args):
    url = str(args.get("url", "")).strip()
    start = max(int(args.get("start") or 0), 0)
    size = min(max(int(args.get("max_chars") or 20000), 1000), 100000)
    final, status, kind, charset, modified, body = read(url)
    cut = len(body) > MAX_BYTES
    if kind == "text/html" or kind == "application/xhtml+xml":
        if not charset:
            found = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
            charset = found.group(1).decode() if found else "utf-8"
        parser = Markdown(final)
        parser.feed(body.decode(charset, "replace"))
        parser.close()
        title, text = " ".join(html.unescape(parser.title).split()), parser.text()
    elif kind.startswith("text/") or kind in TEXT_TYPES or kind.endswith(("+json", "+xml")):
        title, text = "", body.decode(charset or "utf-8", "replace")
    else:
        raise ValueError(f"{final} is {kind or 'of an unknown type'}, not a page with text this tool can read")
    part = text[start:start + size]
    head = [f"# {title}" if title else None, f"address: {final}", f"status: {status} · type: {kind}",
            f"last modified: {modified}" if modified else None,
            f"part: characters {start} to {start + len(part)} of {len(text)}" if start or len(text) > start + size else None]
    tail = []
    if start + size < len(text):
        tail.append(f"(more: ask again with start={start + size})")
    if cut:
        tail.append(f"(the page is larger than {MAX_BYTES // (1024 * 1024)} MB; only the first part was read)")
    return "\n".join(line for line in head if line) + "\n\n" + (part or "(no text on this page)") + ("\n\n" + "\n".join(tail) if tail else "")


def call(name, args):
    if name == "fetch":
        return fetch(args)
    raise ValueError(f"no tool called {name}")

# The protocol, for both eras of MCP. A modern client (2026-07-28 and later) sends its version in every
# request's _meta and may ask `server/discover` first; a legacy client (2025-11-25 and earlier) opens with
# `initialize`. This server is stateless either way, so it simply answers both.
MODERN = ["2026-07-28"]
LEGACY = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]


class ProtocolError(Exception):
    def __init__(self, code, message, data=None):
        super().__init__(message)
        self.code, self.data = code, data


def answer(message):
    method = message.get("method")
    params = message.get("params") or {}
    meta = params.get("_meta") or {}
    info = {"name": NAME, "version": VERSION}
    if method == "initialize":                                        # legacy: the handshake, nothing to keep
        asked = params.get("protocolVersion")
        return {"protocolVersion": asked if asked in LEGACY else LEGACY[0], "capabilities": {"tools": {}},
                "serverInfo": info, "instructions": INSTRUCTIONS}
    asked = meta.get("io.modelcontextprotocol/protocolVersion")
    if asked is not None and asked not in MODERN + LEGACY:
        raise ProtocolError(-32022, "Unsupported protocol version", {"supported": MODERN + LEGACY, "requested": asked})
    done = {"resultType": "complete", "_meta": {"io.modelcontextprotocol/serverInfo": info}}
    if method == "server/discover":
        return {**done, "supportedVersions": MODERN + LEGACY, "capabilities": {"tools": {}},
                "instructions": INSTRUCTIONS, "ttlMs": 3600000, "cacheScope": "public"}
    if method == "ping":                                              # legacy only, harmless to answer
        return {}
    if method == "tools/list":
        return {**done, "tools": TOOLS, "ttlMs": 3600000, "cacheScope": "public"}
    if method == "tools/call":
        if params.get("name") not in {t["name"] for t in TOOLS}:
            raise ProtocolError(-32602, f"no tool called {params.get('name')}")
        try:
            return {**done, "content": [{"type": "text", "text": call(params["name"], params.get("arguments") or {})}]}
        except Exception as e:                                        # the tool failed: the model reads why
            return {**done, "content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True}
    raise ProtocolError(-32601, f"no method {method}")


def main():
    for line in sys.stdin:                                            # ends when the client closes stdin
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except ValueError:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "not JSON"}}
        else:
            if "id" not in message:                                   # a notification: nothing to answer
                continue
            try:
                out = {"jsonrpc": "2.0", "id": message["id"], "result": answer(message)}
            except ProtocolError as e:
                error = {"code": e.code, "message": str(e)}
                if e.data is not None:
                    error["data"] = e.data
                out = {"jsonrpc": "2.0", "id": message["id"], "error": error}
            except Exception as e:                                    # a refusal the client can read
                out = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"}}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
