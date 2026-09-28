#!/usr/bin/env python3
"""Figures from CBS (Statistics Netherlands) StatLine as tools, for any MCP client: find a table, see what is
in it, and read its latest values, or go straight to a few well-known figures such as inflation.

Why this exists: a Dutch figure (inflation, unemployment, population) is only worth quoting with its table,
its period and whether it is still provisional. CBS publishes every StatLine table as open data, free and
without a key. This server reads only opendata.cbs.nl over https: the OData 3 Catalog service and the
standard OData API, which CBS names as the service every dataset is published through. CBS is introducing
OData 4 (datasets.cbs.nl) and says so; this server moves when CBS does. Nothing is stored beyond this
process.

  search_tables   query, include_stopped?, rows?            tables whose title has all the words
  describe_table  id, dimension?, match?                    what a table holds: period, topics, dimensions
                                                            and their category keys
  read_table      id, topic?, filters?, periods?, period_type?
                                                            the latest values of one topic
  key_figure      name                                      inflation, unemployment or population, latest

CBS content is licensed CC BY 4.0: reuse is allowed with CBS named as the source, and without suggesting
that CBS endorses the reuse (cbs.nl copyright page). The standard API returns at most 10,000 cells per call.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

NAME = "cbs"
VERSION = "1.0.0"
INSTRUCTIONS = ("Figures from CBS StatLine open data. For inflation, unemployment or population use key_figure. For "
                "anything else: search_tables, then describe_table for its topics and keys, then read_table. Name CBS "
                "as the source with the table id, period and status (provisional or final) it gives.")
API = "https://opendata.cbs.nl/ODataApi/odata"
CATALOG = "https://opendata.cbs.nl/ODataCatalog/Tables"
HOSTS = {"opendata.cbs.nl"}
TIMEOUT = 60
DIMENSIONS = ("Dimension", "GeoDimension")
FIGURES = {
    "inflation": ("86141NED", "JaarmutatieCPI_5", {"Bestedingscategorieen": "T001112"}, 6,
                  "Consumer price inflation (CPI, change on the same month a year earlier), all spending"),
    "unemployment": ("80590ned", "Seizoengecorrigeerd_8", {"Geslacht": "T001038", "Leeftijd": "52052"}, 6,
                     "Unemployment rate, seasonally adjusted, all persons 15 to 75"),
    "population": ("83474NED", "BevolkingAanHetEindVanDePeriode_8", {}, 3,
                   "Population of the Netherlands at the end of the period"),
}

TOOLS = [
    {"name": "search_tables", "description": "Find CBS StatLine tables by words in their title, in Dutch (\"consumentenprijzen\", \"werkloosheid\", \"bevolking gemeente\") or English for the English tables. Returns each table's id, period, how often it is updated and when it last changed. Discontinued tables are left out unless asked.",
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "Words that are all in the title."},
         "include_stopped": {"type": "boolean", "description": "Also show discontinued (stopgezet) tables. Default false."},
         "rows": {"type": "integer", "minimum": 1, "maximum": 30, "description": "How many tables at most. Default 15."}},
         "required": ["query"]}},
    {"name": "describe_table", "description": "What one CBS table holds: its title, summary, period, update frequency, last change, its topics (the measured values, with key and unit) and its dimensions with their category keys. Give `dimension` and `match` to find the key of one category, like a municipality.",
     "inputSchema": {"type": "object", "properties": {
         "id": {"type": "string", "description": "The table id, like 86141NED or 80590ned."},
         "dimension": {"type": "string", "description": "One dimension key, to list its categories."},
         "match": {"type": "string", "description": "Only categories whose title contains this word, with `dimension`."}},
         "required": ["id"]}},
    {"name": "read_table", "description": "The latest values of one topic in a CBS table, for one category of each dimension (the table's own default, or what `filters` says), with each period's status (provisional or final).",
     "inputSchema": {"type": "object", "properties": {
         "id": {"type": "string", "description": "The table id, like 86141NED."},
         "topic": {"type": "string", "description": "The topic key from describe_table, like JaarmutatieCPI_5. Default the table's first shown topic."},
         "filters": {"type": "object", "additionalProperties": {"type": "string"}, "description": "Dimension key to category key, like {\"Bestedingscategorieen\": \"CPI010000\"}. Unnamed dimensions use the table's default."},
         "periods": {"type": "integer", "minimum": 1, "maximum": 24, "description": "How many of the latest periods. Default 3."},
         "period_type": {"type": "string", "enum": ["month", "quarter", "year"], "description": "Which kind of period. Default the finest the table has."}},
         "required": ["id"]}},
    {"name": "key_figure", "description": "The latest value of a well-known Dutch figure from CBS, with its last few periods: inflation (CPI year-on-year change), unemployment (seasonally adjusted rate) or population.",
     "inputSchema": {"type": "object", "properties": {
         "name": {"type": "string", "enum": sorted(FIGURES), "description": "Which figure."}},
         "required": ["name"]}},
]


def get(url):
    """Read JSON from the CBS open data host only, https, with a deadline, checked after any redirect."""
    request = urllib.request.Request(url, headers={"User-Agent": f"okayiris-cbs-mcp/{VERSION}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as r:
            where = urllib.parse.urlsplit(r.geturl())
            if where.scheme != "https" or where.hostname not in HOSTS:
                raise ValueError(f"refused to read {where.scheme}://{where.hostname}: not the CBS open data host")
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError("CBS has no such table or item (404); search_tables finds the id")
        raise ValueError(f"CBS open data answered {e.code} {e.reason}")


def odata(url, **params):
    params["$format"] = "json"
    return get(url + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))["value"]


def quoted(text):
    return "'" + str(text).replace("'", "''") + "'"


def table_id(args):
    value = str(args.get("id", "")).strip()
    if not re.fullmatch(r"\d{5}[A-Za-z]{0,3}", value):
        raise ValueError(f"a CBS table id looks like 86141NED or 80590ned, not {value or 'nothing'}; search_tables finds it")
    return value


def key(text):
    value = str(text or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_]{1,80}", value):
        raise ValueError(f"a key is letters, digits and _, like JaarmutatieCPI_5, not {value or 'nothing'}")
    return value


def info(table):
    rows = odata(f"{API}/{table}/TableInfos")
    if not rows:
        raise ValueError(f"CBS has no table {table}")
    return rows[0]


def defaults(selection):
    """The category the table itself shows first, per dimension, and the topics it shows first."""
    chosen = {dim: k.strip() for dim, k in re.findall(r"\((\w+) eq '([^']*)'\)", selection or "")}
    topics = re.search(r"\$select=([^&]*)", selection or "")
    return chosen, [t.strip() for t in topics.group(1).split(",")] if topics else []


def period_kind(k):
    return {"MM": "month", "KW": "quarter", "JJ": "year"}.get(k[4:6], "other")


def read(table, topic=None, filters=None, periods=3, kind=None, label=None):
    about = info(table)
    props = odata(f"{API}/{table}/DataProperties")
    topics = {p["Key"]: p for p in props if p["Type"] == "Topic"}
    groups = {p["ID"]: p["Title"] for p in props if p["Type"] == "TopicGroup"}
    dims = [p for p in props if p["Type"] in DIMENSIONS]
    time = next((p for p in props if p["Type"] == "TimeDimension"), None)
    chosen, shown = defaults(about.get("DefaultSelection"))
    topic = key(topic) if topic else next((t for t in shown if t in topics), next(iter(topics), None))
    if topic not in topics:
        raise ValueError(f"{table} has no topic {topic}; describe_table lists them")
    filters = {key(k): str(v) for k, v in (filters or {}).items()}
    unknown = set(filters) - {d["Key"] for d in dims}
    if unknown:
        raise ValueError(f"{table} has no dimension {', '.join(sorted(unknown))}; describe_table lists them")
    where, picked = [], []
    for d in dims:
        cats = odata(f"{API}/{table}/{d['Key']}", **{"$select": "Key,Title"})
        wanted = filters.get(d["Key"], chosen.get(d["Key"]))
        cat = next((c for c in cats if c["Key"].strip() == str(wanted or "").strip()), None)
        if d["Key"] in filters and cat is None:
            raise ValueError(f"{d['Key']} has no category {filters[d['Key']]}; describe_table with dimension={d['Key']} lists them")
        cat = cat or next((c for c in cats if c["Key"].startswith("T00")), cats[0] if cats else None)
        if cat:
            where.append(f"{d['Key']} eq {quoted(cat['Key'])}")
            picked.append(f"{d['Title']}: {cat['Title']}")
    shown_periods = []
    if time:
        all_periods = odata(f"{API}/{table}/{time['Key']}")
        kinds = {period_kind(p["Key"]) for p in all_periods}
        kind = kind or next((k for k in ("month", "quarter", "year") if k in kinds), None)
        if kind not in kinds:
            raise ValueError(f"{table} has no {kind} figures; it has {', '.join(sorted(kinds))}")
        shown_periods = sorted((p for p in all_periods if period_kind(p["Key"]) == kind), key=lambda p: p["Key"])
    rows = []
    # Newest first; step back past periods that have no figure yet, a few at a time.
    for start in range(0, 48, max(periods, 6)):
        batch = list(reversed(shown_periods))[start:start + max(periods, 6)] if time else [None]
        if not batch:
            break
        clause = list(where)
        if time:
            clause.append("(" + " or ".join(f"{time['Key']} eq {quoted(p['Key'])}" for p in batch) + ")")
        params = {"$select": ",".join(([time["Key"]] if time else []) + [topic])}
        if clause:
            params["$filter"] = " and ".join(clause)
        values = {r.get(time["Key"]) if time else None: r.get(topic) for r in odata(f"{API}/{table}/TypedDataSet", **params)}
        for p in batch:
            value = values.get(p["Key"] if p else None)
            if value is not None:
                rows.append((p, value))
        if len(rows) >= periods or not time:
            break
    unit = topics[topic].get("Unit") or ""
    title = (groups[topics[topic]["ParentID"]] + ": " if topics[topic].get("ParentID") in groups else "") + topics[topic]["Title"]
    lines = [f"# {label or title}", f"{about['Title'].strip()} ({table})", f"Topic: {title} [{topic}], unit {unit or 'none'}"]
    if picked:
        lines.append("Selection: " + " · ".join(picked))
    if not rows:
        lines.append("No figures found for this selection.")
    for p, value in rows[:periods]:
        when = f"{p['Title']} ({p.get('Status', '').lower()})" if p else "value"
        lines.append(f"- {when}: {value} {unit}".rstrip())
    lines.append(f"Source: CBS StatLine, table {table}, last changed {about.get('Modified', '?')[:10]}, "
                 f"{about.get('Frequency', '')} · {API}/{table}")
    if about.get("Frequency") == "Stopgezet":
        lines.append("This table is discontinued (stopgezet); search_tables finds its successor.")
    return "\n".join(lines)


def call(name, args):
    if name == "search_tables":
        words = str(args.get("query", "")).lower().split()
        if not words or len(words) > 8 or not all(re.fullmatch(r"[\w\-.,;%=']{1,40}", w) for w in words):
            raise ValueError("say one to eight plain words that are in the title, like \"consumentenprijzen\"")
        rows = args.get("rows", 15)
        if isinstance(rows, bool) or not isinstance(rows, int) or not 1 <= rows <= 30:
            raise ValueError(f"rows is a whole number from 1 to 30, not {rows!r}")
        clause = " and ".join(f"substringof({quoted(w)},tolower(Title))" for w in words)
        if not args.get("include_stopped"):
            clause += " and Frequency ne 'Stopgezet'"
        found = odata(CATALOG, **{"$filter": clause, "$select": "Identifier,Title,Period,Frequency,Modified",
                                   "$orderby": "Modified desc", "$top": str(rows)})
        if not found:
            return f"No {'' if args.get('include_stopped') else 'current '}CBS table has all of these words in its title. Try fewer or other words, or include_stopped."
        lines = [f"{len(found)} CBS tables, most recently changed first:"]
        lines += [f"- {t['Identifier']} · {t['Title'].strip()} · {t['Period']} · {t['Frequency']} · changed {t['Modified'][:10]}" for t in found]
        return "\n".join(lines + ["describe_table shows what one of them holds."])
    if name == "describe_table":
        table = table_id(args)
        about = info(table)
        props = odata(f"{API}/{table}/DataProperties")
        if args.get("dimension"):
            dim = key(args["dimension"])
            if dim not in {p["Key"] for p in props if p["Type"] in DIMENSIONS + ("TimeDimension",)}:
                raise ValueError(f"{table} has no dimension {dim}; describe_table without dimension lists them")
            match = str(args.get("match") or "").strip()
            params = {"$select": "Key,Title"}
            if match:
                if not re.fullmatch(r"[\w\s\-.,'()]{1,60}", match):
                    raise ValueError("match is a plain word or two, like Utrecht")
                params["$filter"] = f"substringof({quoted(match.lower())},tolower(Title))"
            cats = odata(f"{API}/{table}/{dim}", **params)
            if not cats:
                return f"No category of {dim} in {table} has \"{match}\" in its title."
            lines = [f"{len(cats)} categories of {dim} in {table}" + (f" matching \"{match}\"" if match else "") + ":"]
            lines += [f"- {c['Key'].strip()} · {c['Title']}" for c in cats[:60]]
            if len(cats) > 60:
                lines.append(f"(and {len(cats) - 60} more; narrow with match)")
            return "\n".join(lines)
        chosen, _ = defaults(about.get("DefaultSelection"))
        lines = [f"# {about['Title']} ({table})", f"Period: {about.get('Period')} · {about.get('Frequency')} · last changed "
                 f"{about.get('Modified', '?')[:10]} · status {about.get('OutputStatus', '?')}", "",
                 " ".join((about.get("ShortDescription") or about.get("Summary") or "").split())[:900], "", "Topics (key, unit):"]
        group = None
        for p in props:
            if p["Type"] == "TopicGroup":
                group = p["Title"]
            elif p["Type"] == "Topic":
                lines.append(f"- {p['Key']} · {(group + ': ') if group and p.get('ParentID') is not None else ''}{p['Title']} · {p.get('Unit') or ''}".rstrip(" ·"))
        lines.append("")
        lines.append("Dimensions:")
        for p in props:
            if p["Type"] in DIMENSIONS + ("TimeDimension",):
                cats = odata(f"{API}/{table}/{p['Key']}", **{"$select": "Key,Title"})
                sample = ", ".join(f"{c['Key'].strip()} ({c['Title']})" for c in (cats[-3:] if p["Type"] == "TimeDimension" else cats[:5]))
                default = f"; default {chosen[p['Key']]}" if p["Key"] in chosen else ""
                lines.append(f"- {p['Key']} · {p['Title']} · {len(cats)} categories{default}; e.g. {sample}")
        lines.append(f"\nSource: CBS StatLine · {API}/{table}")
        return "\n".join(lines)
    if name == "read_table":
        table = table_id(args)
        periods = args.get("periods", 3)
        if isinstance(periods, bool) or not isinstance(periods, int) or not 1 <= periods <= 24:
            raise ValueError(f"periods is a whole number from 1 to 24, not {periods!r}")
        kind = args.get("period_type")
        if kind not in (None, "month", "quarter", "year"):
            raise ValueError("period_type is month, quarter or year")
        filters = args.get("filters") or {}
        if not isinstance(filters, dict):
            raise ValueError("filters is an object of dimension key to category key")
        return read(table, args.get("topic"), filters, periods, kind)
    if name == "key_figure":
        figure = FIGURES.get(str(args.get("name", "")).lower())
        if not figure:
            raise ValueError(f"key_figure knows {', '.join(sorted(FIGURES))}; for anything else use search_tables")
        table, topic, filters, periods, label = figure
        return read(table, topic, filters, periods, None, label)
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
