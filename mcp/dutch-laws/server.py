#!/usr/bin/env python3
"""Dutch legislation as tools, for any MCP client: find a law, see how it is built, read one article, each
as the text that was in force on a given date.

Why this exists: an answer about Dutch rules is only as good as the article behind it, and the article
changes. This server reads the government's own open data (the Basiswettenbestand, through the SRU search
service and the official publications repository) and hands back text with a link to wetten.overheid.nl.
Nothing is executed, nothing is stored beyond this process, and no credential is needed or used.

  search_laws   query, date?, kind?     laws and regulations whose title matches, with their BWB id
  outline       id, date?               the chapters, sections and article numbers of one law
  read_article  id, article, date?      the full text of one article, as in force on that date
"""
import datetime
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NAME = "dutch-laws"
VERSION = "1.0.0"
INSTRUCTIONS = ("Dutch legislation from the government's own open data. Find a law with search_laws, then read the "
                "article itself with read_article, for the date that matters, and cite the link it gives.")
SEARCH = "https://zoekservice.overheid.nl/sru/Search"
HOSTS = {"zoekservice.overheid.nl", "repository.officiele-overheidspublicaties.nl"}
TIMEOUT = 60
NS = {"dcterms": "http://purl.org/dc/terms/", "overheidbwb": "http://standaarden.overheid.nl/bwb/terms/",
      "sru": "http://docs.oasis-open.org/ns/search-ws/sruResponse"}
RANK = {"wet": 0, "rijkswet": 0, "AMvB": 1, "rijksAMvB": 1, "ministeriele-regeling": 2, "KB": 3}
SKIP = {"meta-data", "lidnr", "li.nr", "kop", "aanhef", "wij", "considerans"}
STRUCTURE = {"boek", "deel", "hoofdstuk", "titeldeel", "titel", "afdeling", "paragraaf", "sub-paragraaf", "artikel", "bijlage"}
LAWS = {}                                                             # (id, date) -> parsed text, for this process

TOOLS = [
    {"name": "search_laws", "description": "Find Dutch laws and regulations by words in their title (\"inkomstenbelasting\", \"huurcommissie\", \"Burgerlijk Wetboek Boek 7\"), as in force on a date. Returns each one's BWB id, which the other tools need.",
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "Words that are all in the title."},
         "date": {"type": "string", "description": "YYYY-MM-DD, the day the law must be in force. Default today."},
         "kind": {"type": "string", "description": "Only this kind: wet, AMvB, ministeriele-regeling, beleidsregel, ..."}},
         "required": ["query"]}},
    {"name": "outline", "description": "The structure of one law as in force on a date: its chapters, sections and the number and heading of every article. Use it to find the article to read.",
     "inputSchema": {"type": "object", "properties": {
         "id": {"type": "string", "description": "The BWB id, like BWBR0011353."},
         "date": {"type": "string", "description": "YYYY-MM-DD. Default today."}},
         "required": ["id"]}},
    {"name": "read_article", "description": "The full text of one article of a Dutch law, exactly as in force on a date, with its paragraphs and lists, when that version took effect, and a link to cite.",
     "inputSchema": {"type": "object", "properties": {
         "id": {"type": "string", "description": "The BWB id, like BWBR0011353."},
         "article": {"type": "string", "description": "The article number, like 3.114, 7:248 or 12a."},
         "date": {"type": "string", "description": "YYYY-MM-DD. Default today."}},
         "required": ["id", "article"]}},
]


def get(url):
    """Read from the government's own two hosts only, https, with a deadline."""
    request = urllib.request.Request(url, headers={"User-Agent": f"okayiris-dutch-laws-mcp/{VERSION}", "Accept": "application/xml"})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as r:
        where = urllib.parse.urlsplit(r.geturl())
        if where.scheme != "https" or where.hostname not in HOSTS:
            raise ValueError(f"refused to read {where.scheme}://{where.hostname}: not a government source")
        return r.read()


def day(args):
    value = str(args.get("date") or datetime.date.today().isoformat()).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"a date is YYYY-MM-DD, not {value}")
    datetime.date.fromisoformat(value)
    return value


def bwb(args):
    value = str(args.get("id", "")).strip().upper()
    if not re.fullmatch(r"BWB[RV]\d{7}", value):
        raise ValueError(f"a BWB id looks like BWBR0011353, not {value or 'nothing'}; search_laws finds it")
    return value


def cql(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def sru(query, count):
    params = {"operation": "searchRetrieve", "version": "2.0", "x-connection": "BWB", "query": query, "maximumRecords": str(count)}
    root = ET.fromstring(get(SEARCH + "?" + urllib.parse.urlencode(params)))
    problem = root.find(".//{http://docs.oasis-open.org/ns/search-ws/diagnostic}message")
    if problem is not None:
        raise ValueError(f"the search service said: {problem.text}")
    rows = []
    for record in root.iter("{http://standaarden.overheid.nl/sru}gzd"):
        def one(path):
            found = record.find(path, NS)
            return found.text.strip() if found is not None and found.text else ""
        rows.append({"id": one(".//dcterms:identifier"), "title": one(".//dcterms:title"), "kind": one(".//dcterms:type"),
                     "from": one(".//overheidbwb:geldigheidsperiode_startdatum"),
                     "until": one(".//overheidbwb:geldigheidsperiode_einddatum"),
                     "xml": one(".//overheidbwb:locatie_toestand")})
    total = root.findtext("sru:numberOfRecords", "0", NS)
    return rows, int(total or 0)


def link(law, date, article=None):
    return f"https://wetten.overheid.nl/jci1.3:c:{law}" + (f"&artikel={article}" if article else "") + f"&g={date}"


def version(law, date):
    """The text of one law as in force on one date: its record and its parsed XML."""
    if (law, date) not in LAWS:
        rows, _ = sru(f"dcterms.identifier=={law} and overheidbwb.geldigheidsdatum=={date}", 5)
        rows = [row for row in rows if row["id"] == law and row["xml"]]
        if not rows:
            raise ValueError(f"{law} has no text in force on {date}: it may not exist yet, or no longer")
        row = max(rows, key=lambda r: r["from"])
        LAWS.clear()                                                  # one law at a time: they can be large
        LAWS[(law, date)] = (row, ET.fromstring(get(row["xml"])))
    return LAWS[(law, date)]


def inline(element):
    parts = [element.text or ""]
    for child in element:
        if child.tag != "meta-data":
            parts.append(inline(child))
        parts.append(child.tail or "")
    return " ".join("".join(parts).split())


def heading(element):
    kop = element.find("kop")
    if kop is None:
        return ""
    return " ".join(t for t in (inline(kop.find(k)) if kop.find(k) is not None else "" for k in ("label", "nr", "titel")) if t)


def block(element, indent=""):
    """The readable lines of an article: its paragraphs (leden), lists, tables and editorial notes."""
    lines = []
    for child in element:
        tag = child.tag
        if tag in SKIP:
            continue
        if tag in ("lid", "li"):
            number = child.findtext("lidnr" if tag == "lid" else "li.nr") or ""
            inner = block(child, indent + ("  " if tag == "li" else ""))
            prefix = (f"{number.strip()}. " if tag == "lid" and number.strip() else f"{number.strip()} " if number.strip() else "")
            if inner:
                inner[0] = (indent + ("  " if tag == "li" else "") + prefix + inner[0].lstrip())
            lines += inner + ([""] if tag == "lid" else [])
        elif tag == "table":
            for row in child.iter("row"):
                lines.append(indent + "| " + " | ".join(inline(entry) for entry in row.iter("entry")) + " |")
        elif tag == "redactie":
            lines.append(indent + "[" + inline(child) + "]")
        elif tag in ("al", "tussenkop"):
            text = inline(child)
            if text:
                lines.append(indent + text)
        elif len(child):
            lines += block(child, indent)
        elif inline(child):
            lines.append(indent + inline(child))
    return lines


def number(text):
    return re.sub(r"^(artikel|art\.?)\s*", "", " ".join(str(text).split()).lower()).replace(" ", "")


def outline_lines(element, depth, out):
    for child in element:
        if child.tag in STRUCTURE:
            title = heading(child)
            if title:
                out.append("  " * depth + ("- " if child.tag == "artikel" else "") + title)
            if child.tag != "artikel":
                outline_lines(child, depth + (1 if title else 0), out)
        elif child.tag not in ("meta-data", "kop") and len(child):
            outline_lines(child, depth, out)


def call(name, args):
    if name == "search_laws":
        words = [w for w in str(args.get("query", "")).split() if w]
        if not words:
            raise ValueError("say which words should be in the title")
        date = day(args)
        query = " and ".join([f"overheidbwb.titel any {cql(w)}" for w in words] + [f"overheidbwb.geldigheidsdatum=={date}"])
        if args.get("kind"):
            query += f" and dcterms.type=={cql(str(args['kind']))}"
        rows, total = sru(query, 50)
        if not args.get("kind"):                                      # the laws themselves, also past the first 50
            laws, _ = sru(query + " and dcterms.type==wet", 12)
            rows += [row for row in laws if row["id"] not in {r["id"] for r in rows}]
        if not rows:
            return f"No law or regulation in force on {date} has all of these words in its title."
        wanted = " ".join(words).lower()
        rows.sort(key=lambda r: (r["title"].lower() != wanted, RANK.get(r["kind"], 9),
                                 not re.search(r"\b" + re.escape(words[0].lower()), r["title"].lower()), len(r["title"])))
        shown = rows[:12]
        lines = [f"{len(shown)} of {total} in force on {date}, laws first:"]
        for r in shown:
            lines.append(f"- {r['id']} · {r['title']} ({r['kind']}), this version since {r['from']} · {link(r['id'], date)}")
        return "\n".join(lines)
    if name == "outline":
        law, date = bwb(args), day(args)
        row, root = version(law, date)
        lines = []
        outline_lines(root, 0, lines)
        text = "\n".join(lines) or "This regulation has no chapters or numbered articles."
        if len(text) > 30000:
            text = text[:30000] + "\n(the outline goes on; read_article reads any article by its number)"
        return f"# {row['title']} ({law})\nin force on {date}, this version since {row['from']} · {link(law, date)}\n\n{text}"
    if name == "read_article":
        law, date = bwb(args), day(args)
        wanted = number(args.get("article", ""))
        if not wanted:
            raise ValueError("say which article, like 3.114")
        row, root = version(law, date)
        articles = {}
        for article in root.iter("artikel"):
            if article.find("kop") is not None:
                articles.setdefault(number(article.findtext("kop/nr") or ""), article)
        # The Civil Code is cited as 7:248, but each of its books is its own BWB id that numbers it 248.
        if wanted not in articles and row["title"].startswith("Burgerlijk Wetboek") and ":" in wanted:
            wanted = wanted.split(":", 1)[1]
        article = articles.get(wanted)
        if article is not None:
            since = article.get("inwerking") or row["from"]
            body = "\n".join(block(article)).strip() or "(this article has no text in this version)"
            status = f" · status: {article.get('status')}" if article.get("status") not in (None, "goed") else ""
            return "\n".join([f"# {heading(article)}", f"{row['title']} ({law}), in force on {date}",
                              f"this article's text since {since}{status} · {link(law, date, article.findtext('kop/nr').strip())}",
                              "", body])
        raise ValueError(f"{row['title']} has no article {args.get('article')} on {date}; outline lists the numbers")
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
