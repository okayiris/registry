#!/usr/bin/env python3
"""Dutch addresses and buildings as tools, for any MCP client: find an address, read its official form with
municipality, province, coordinates and BAG ids, and see the building it is in.

Why this exists: an address typed by a person ("Dam 1 Adam", "1012js 1") is not yet the address the
government knows. The Basisregistratie Adressen en Gebouwen (BAG) is that register, and PDOK serves it
openly: the PDOK Locatieserver to search it, and the BAG OGC API for the building behind an address
(construction year, use, floor area, status). This server reads only those two PDOK services, over https,
free and without a key. Nothing is stored beyond this process and nothing about the owner is sent except
the address or point being looked up.

  search_addresses  query, rows?                        addresses that match free text, with their ids
  address           id? | postcode + house_number, addition?, building?
                                                        the official address, its BAG ids, place and
                                                        coordinates, and the BAG building behind it
  address_at        lat, lon, rows?, distance?          the nearest addresses to a point

The BAG data are published under Public Domain Mark 1.0 (PDOK dataset page). PDOK asks every client to
identify itself; this server sends a User-Agent and Referer naming itself.
"""
import datetime
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

NAME = "pdok"
VERSION = "1.0.0"
INSTRUCTIONS = ("Dutch addresses and buildings from the BAG, read through PDOK. Find an address with search_addresses "
                "(or go straight to address with a postcode and house number), then read it with address. Cite the "
                "link it gives and say the data were read today from PDOK.")
LOCATIE = "https://api.pdok.nl/bzk/locatieserver/search/v3_1"
BAG = "https://api.pdok.nl/kadaster/bag/ogc/v2"
HOSTS = {"api.pdok.nl"}
TIMEOUT = 30
FIELDS = ("id,weergavenaam,straatnaam,huis_nlt,huisnummer,huisletter,huisnummertoevoeging,postcode,woonplaatsnaam,"
          "gemeentenaam,gemeentecode,provincienaam,provinciecode,wijknaam,buurtnaam,waterschapsnaam,centroide_ll,"
          "centroide_rd,nummeraanduiding_id,adresseerbaarobject_id,openbareruimte_id,woonplaatscode,adrestype,"
          "gekoppeld_perceel,type,bron")
SOLR = re.compile(r'[+\-&|!(){}\[\]^"~*?:\\/]')

TOOLS = [
    {"name": "search_addresses", "description": "Find Dutch addresses from free text, as a person would type it (\"Dam 1 Amsterdam\", \"Oudegracht 3 Utrecht\", \"1012JS 1\"). Returns the best matches with their PDOK id; pass an id to `address` for the details.",
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "Street and number, place, or postcode and number. 2 to 200 characters."},
         "rows": {"type": "integer", "minimum": 1, "maximum": 20, "description": "How many matches at most. Default 8."}},
         "required": ["query"]}},
    {"name": "address", "description": "The official Dutch address from the BAG: street, number, postcode, place, municipality, province, neighbourhood, coordinates (WGS84 and RD), its BAG ids and cadastral parcels, and the BAG building behind it (construction year, use, floor area, status). Give either the id from search_addresses, or a postcode with a house number.",
     "inputSchema": {"type": "object", "properties": {
         "id": {"type": "string", "description": "The PDOK id from search_addresses or address_at, like adr-2a8dc1af055da20b8bcdc8e4dbda1eaa."},
         "postcode": {"type": "string", "description": "A Dutch postcode, like 1012JS or 1012 JS."},
         "house_number": {"type": "integer", "minimum": 1, "maximum": 99999, "description": "The house number, with the postcode."},
         "addition": {"type": "string", "description": "House letter and/or addition, like A, 2 or bis. Optional."},
         "building": {"type": "boolean", "description": "Also read the BAG building and dwelling behind the address. Default true."}}}},
    {"name": "address_at", "description": "The addresses nearest to a point (reverse geocoding), with their distance in metres and their PDOK id for `address`. Only the Netherlands.",
     "inputSchema": {"type": "object", "properties": {
         "lat": {"type": "number", "minimum": 50.5, "maximum": 53.8, "description": "Latitude, WGS84, like 52.3733."},
         "lon": {"type": "number", "minimum": 3.2, "maximum": 7.3, "description": "Longitude, WGS84, like 4.8937."},
         "rows": {"type": "integer", "minimum": 1, "maximum": 20, "description": "How many addresses at most. Default 5."},
         "distance": {"type": "integer", "minimum": 1, "maximum": 5000, "description": "Search radius in metres. Default 250."}},
         "required": ["lat", "lon"]}},
]


def get(url):
    """Read JSON from PDOK's own host only, https, with a deadline, checked again after any redirect."""
    if urllib.parse.urlsplit(url).hostname not in HOSTS:
        raise ValueError(f"refused to read {url}: not a PDOK address")
    request = urllib.request.Request(url, headers={"User-Agent": f"okayiris-pdok-mcp/{VERSION}", "Accept": "application/json",
                                                   "Referer": "https://mcp.okayiris.com/m/pdok.md"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as r:
            where = urllib.parse.urlsplit(r.geturl())
            if where.scheme != "https" or where.hostname not in HOSTS:
                raise ValueError(f"refused to read {where.scheme}://{where.hostname}: not a PDOK source")
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise ValueError(f"PDOK answered {e.code} {e.reason} for {url}")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def plain(value):
    """A number sent as text ("3", "52.37") is read as that number; clients often send them that way."""
    if isinstance(value, str) and re.fullmatch(r"\s*-?\d+(\.\d+)?\s*", value):
        return float(value) if "." in value else int(value)
    return value


def count(args, key, default, low, high):
    value = plain(args.get(key, default))
    if isinstance(value, bool) or not isinstance(value, (int, float)) or int(value) != value or not low <= value <= high:
        raise ValueError(f"{key} is a whole number from {low} to {high}, not {value!r}")
    return int(value)


def number(args, key, low, high):
    value = plain(args.get(key))
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= value <= high:
        raise ValueError(f"{key} is a number from {low} to {high} (the Netherlands), not {value!r}")
    return float(value)


def search(endpoint, params):
    return get(f"{LOCATIE}/{endpoint}?" + urllib.parse.urlencode(params))["response"]


def point(wkt):
    found = re.fullmatch(r"POINT\(([-\d.]+) ([-\d.]+)\)", wkt or "")
    return (found.group(1), found.group(2)) if found else (None, None)


def building(vbo):
    """The BAG dwelling (verblijfsobject) with this id and the building(s) (panden) it lies in."""
    if not re.fullmatch(r"\d{16}", vbo or ""):
        return ["Building: this address has no BAG dwelling id (it may be a berth or a site)."]
    found = get(f"{BAG}/collections/verblijfsobject/items?" + urllib.parse.urlencode({"f": "json", "identificatie": vbo}))
    if not found.get("features"):
        return [f"Building: BAG dwelling {vbo} is not in the PDOK BAG API."]
    p = found["features"][0]["properties"]
    lines = [f"Dwelling (verblijfsobject) {vbo}: {p.get('status')}; use: {p.get('gebruiksdoel')}; floor area {p.get('oppervlakte')} m²"]
    for href in (p.get("pand.href") or [])[:3]:
        parts = urllib.parse.urlsplit(href)
        if parts.hostname not in HOSTS or not re.fullmatch(r"/kadaster/bag/ogc/v2/collections/pand/items/[0-9a-f-]{36}", parts.path):
            continue
        q = get(f"https://{parts.hostname}{parts.path}?f=json")["properties"]
        lines.append(f"Building (pand) {q.get('identificatie')}: built {q.get('bouwjaar')}; {q.get('status')}; "
                     f"use: {q.get('gebruiksdoel')}; {q.get('aantal_verblijfsobjecten')} dwelling(s) in it")
    lines.append(f"BAG via PDOK, read {found.get('timeStamp', now())} · {BAG}/collections/verblijfsobject/items?f=html&identificatie={vbo}")
    return lines


def describe(d, with_building):
    lon, lat = point(d.get("centroide_ll"))
    x, y = point(d.get("centroide_rd"))
    lines = [f"# {d.get('weergavenaam')}",
             f"Street: {d.get('straatnaam')} {d.get('huis_nlt')} · postcode {d.get('postcode')} · place {d.get('woonplaatsnaam')}",
             f"Municipality: {d.get('gemeentenaam')} (GM{d.get('gemeentecode')}) · province {d.get('provincienaam')}",
             f"Neighbourhood: {d.get('buurtnaam')}, district {d.get('wijknaam')} · water board {d.get('waterschapsnaam')}",
             f"Coordinates: {lat}, {lon} (WGS84) · RD {x}, {y}",
             f"BAG ids: nummeraanduiding {d.get('nummeraanduiding_id')} · verblijfsobject {d.get('adresseerbaarobject_id')} · "
             f"openbare ruimte {d.get('openbareruimte_id')} · woonplaats {d.get('woonplaatscode')}",
             f"Address type: {d.get('adrestype') or 'unknown'}"]
    if d.get("gekoppeld_perceel"):
        lines.append("Cadastral parcels: " + ", ".join(d["gekoppeld_perceel"][:6]))
    lines.append(f"PDOK Locatieserver (BAG), read {now()} · {LOCATIE}/lookup?id={d.get('id')}")
    if with_building:
        lines += [""] + building(d.get("adresseerbaarobject_id"))
    return "\n".join(lines)


def call(name, args):
    if name == "search_addresses":
        query = " ".join(SOLR.sub(" ", str(args.get("query", ""))).split())
        if not 2 <= len(query) <= 200:
            raise ValueError("say the address in 2 to 200 characters, like \"Dam 1 Amsterdam\"")
        rows = count(args, "rows", 8, 1, 20)
        found = search("suggest", {"q": query, "fq": "type:adres", "rows": rows, "fl": "id,weergavenaam"})
        if not found["docs"]:
            return f"No Dutch address matches \"{query}\". Try the street and number with the place, or a postcode and number."
        lines = [f"{len(found['docs'])} of {found['numFound']} addresses matching \"{query}\" (PDOK Locatieserver, read {now()}):"]
        lines += [f"- {d['weergavenaam']} · id {d['id']}" for d in found["docs"]]
        return "\n".join(lines + ["Pass an id to `address` for the official details."])
    if name == "address":
        with_building = args.get("building", True) is not False
        ident = str(args.get("id") or "").strip()
        if ident:
            if not re.fullmatch(r"adr-[0-9a-f]{32}", ident):
                raise ValueError(f"an address id looks like adr-2a8dc1af055da20b8bcdc8e4dbda1eaa, not {ident}; search_addresses finds it")
            docs = search("lookup", {"id": ident, "fl": FIELDS})["docs"]
            if not docs:
                raise ValueError(f"PDOK has no address with id {ident}; it may have been withdrawn, search again")
            return describe(docs[0], with_building)
        postcode = re.sub(r"\s", "", str(args.get("postcode") or "")).upper()
        if not re.fullmatch(r"[1-9]\d{3}[A-Z]{2}", postcode):
            raise ValueError(f"give an id, or a postcode like 1012JS with a house_number; {postcode or 'nothing'} is not a postcode")
        house = count(args, "house_number", None, 1, 99999)
        addition = re.sub(r"[\s-]", "", str(args.get("addition") or "")).upper()
        if not re.fullmatch(r"[A-Z0-9]{0,6}", addition):
            raise ValueError(f"an addition is letters and digits, like A or 2, not {args.get('addition')}")
        docs = search("free", {"q": f"postcode:{postcode} and huisnummer:{house}", "fq": "type:adres", "rows": 50, "fl": FIELDS})["docs"]
        docs = [d for d in docs if d.get("postcode") == postcode and d.get("huisnummer") == house]
        if addition:
            docs = [d for d in docs if str(d.get("huis_nlt", "")).upper().replace("-", "") == f"{house}{addition}"]
        if not docs:
            raise ValueError(f"no address {postcode} {house}{addition} in the BAG; check the number, or use search_addresses")
        if len(docs) > 1:
            lines = [f"{postcode} {house} has {len(docs)} addresses; say which with `addition`, or pass an id:"]
            return "\n".join(lines + [f"- {d['weergavenaam']} · id {d['id']}" for d in docs[:30]])
        return describe(docs[0], with_building)
    if name == "address_at":
        lat, lon = number(args, "lat", 50.5, 53.8), number(args, "lon", 3.2, 7.3)
        rows, distance = count(args, "rows", 5, 1, 20), count(args, "distance", 250, 1, 5000)
        found = search("reverse", {"lat": f"{lat:.6f}", "lon": f"{lon:.6f}", "type": "adres", "rows": rows, "distance": distance,
                                   "fl": "id,weergavenaam,afstand"})
        if not found["docs"]:
            return f"No address within {distance} m of {lat:.5f}, {lon:.5f}. Try a larger distance."
        lines = [f"Addresses nearest to {lat:.5f}, {lon:.5f} (within {distance} m; PDOK Locatieserver, read {now()}):"]
        lines += [f"- {d['weergavenaam']} · {d.get('afstand')} m · id {d['id']}" for d in found["docs"]]
        return "\n".join(lines)
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
