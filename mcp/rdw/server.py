#!/usr/bin/env python3
"""Dutch vehicle data by licence plate as tools, for any MCP client: what the vehicle is, when it was first
admitted, until when its APK (periodic inspection) runs, its fuel and emissions, and whether a recall is open.

Why this exists: "is the APK still valid?", "what car is this plate?", "is there a recall on my car?" have
one authoritative answer, the Dutch vehicle register (kentekenregister), and the RDW publishes the
non-sensitive part of it as open data at opendata.rdw.nl (a Socrata SODA API, free, no key). This server
reads only that host, over https, and only by plate. Nothing is stored beyond this process. The open data
hold no owner and no theft status; this server cannot say who owns a vehicle.

  vehicle   plate           make, model, colour, first admission, APK expiry, insurance flag, odometer
                            judgement, fuel and emissions, and whether a recall is open
  recalls   plate           each recall on the vehicle: its status, the defect, the risk and the remedy

The RDW publishes these datasets under Creative Commons Zero, without guarantees on availability or
currency, on a fair-use basis, and asks that reuse does not use its logo or house style (Bijsluiter Open
Data). Without an app token, Socrata throttles by IP address.
"""
import datetime
import email.utils
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

NAME = "rdw"
VERSION = "1.0.0"
INSTRUCTIONS = ("Dutch vehicle data by licence plate, from the RDW's open data. Use vehicle for what a plate is and its "
                "APK expiry; use recalls when a recall is open. Give the dataset link and date it returns.")
BASE = "https://opendata.rdw.nl/resource"
HOSTS = {"opendata.rdw.nl"}
TIMEOUT = 30
VEHICLES, FUEL, STATUS, RECALL, RISK = "m9d7-ebf2", "8ys7-d773", "t49b-isb7", "j9yg-7rg9", "9ihi-jgpf"
RISKS = {"ERN": "serious", "GEM": "medium", "LG": "low", "GNR": "no risk", "NTB": "to be determined"}

TOOLS = [
    {"name": "vehicle", "description": "What a Dutch licence plate is, from the vehicle register's open data: kind, make, model, colour, body, first admission (world and NL), APK expiry date and whether it has passed, insurance (WAM) flag, export and taxi flags, odometer judgement, fuel(s) with CO2, consumption and emission class, and whether a recall is open.",
     "inputSchema": {"type": "object", "properties": {
         "plate": {"type": "string", "description": "The Dutch licence plate, with or without dashes: 16-RSL-9 or 16RSL9."}},
         "required": ["plate"]}},
    {"name": "recalls", "description": "The recalls (terugroepacties) registered for a Dutch licence plate: for each, whether it is still open or the maker reported it fixed, the defect, what can happen, the RDW risk rating and the remedy.",
     "inputSchema": {"type": "object", "properties": {
         "plate": {"type": "string", "description": "The Dutch licence plate, with or without dashes."}},
         "required": ["plate"]}},
]


def get(dataset, params):
    """Read one SODA dataset from the RDW's own host only, https, with a deadline, checked after redirects.
    Returns the rows and the day the dataset was last changed."""
    url = f"{BASE}/{dataset}.json?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": f"okayiris-rdw-mcp/{VERSION}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as r:
            where = urllib.parse.urlsplit(r.geturl())
            if where.scheme != "https" or where.hostname not in HOSTS:
                raise ValueError(f"refused to read {where.scheme}://{where.hostname}: not the RDW open data host")
            changed = r.headers.get("Last-Modified")
            day = email.utils.parsedate_to_datetime(changed).date().isoformat() if changed else "unknown"
            return json.loads(r.read()), day
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise ValueError("the RDW open data service is busy (429, too many requests); try again in a minute")
        raise ValueError(f"the RDW open data service answered {e.code} {e.reason}")


def plate(args):
    raw = str(args.get("plate", ""))
    value = re.sub(r"[\s\-.]", "", raw).upper()
    if not re.fullmatch(r"[A-Z0-9]{6}", value) or not re.search(r"\d", value) or not re.search(r"[A-Z]", value):
        raise ValueError(f"a Dutch plate is 6 letters and digits, like 16-RSL-9, not {raw or 'nothing'}")
    return value


def date(value):
    value = str(value or "")
    return f"{value[:4]}-{value[4:6]}-{value[6:8]}" if re.fullmatch(r"\d{8}", value) else (value or "not registered")


def link(dataset, value):
    return f"{BASE}/{dataset}.json?kenteken={value}"


def call(name, args):
    if name == "vehicle":
        value = plate(args)
        rows, day = get(VEHICLES, {"kenteken": value})
        if not rows:
            raise ValueError(f"no vehicle with plate {value} in the RDW open data; check the plate (0 and O, 1 and I)")
        v = rows[0]
        today = datetime.date.today().isoformat()
        apk = date(v.get("vervaldatum_apk"))
        state = "" if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", apk) else (" (passed)" if apk < today else " (still valid today)")
        colour = v.get("eerste_kleur", "?") + ("" if v.get("tweede_kleur") in (None, "Niet geregistreerd") else f" / {v['tweede_kleur']}")
        lines = [f"# {value}: {v.get('merk', '?')} {v.get('handelsbenaming', '')}".rstrip(),
                 f"Kind: {v.get('voertuigsoort')} · body {v.get('inrichting', '?')} · EU category {v.get('europese_voertuigcategorie', '?')} · colour {colour}",
                 f"First admission: {date(v.get('datum_eerste_toelating'))} · first registered in NL {date(v.get('datum_eerste_tenaamstelling_in_nederland'))} · last change of holder {date(v.get('datum_tenaamstelling'))}",
                 f"APK expiry: {apk}{state}",
                 f"Insured (WAM) registered: {v.get('wam_verzekerd', '?')} · export: {v.get('export_indicator', '?')} · taxi: {v.get('taxi_indicator', '?')}",
                 f"Open recall: {v.get('openstaande_terugroepactie_indicator', '?')}"]
        if v.get("tellerstandoordeel"):
            lines.append(f"Odometer judgement: {v['tellerstandoordeel']} (last reading registered in {v.get('jaar_laatste_registratie_tellerstand', '?')})")
        specs = [f"{v[k]} {unit}" for k, unit in (("cilinderinhoud", "cc"), ("massa_rijklaar", "kg ready to drive"),
                                                   ("aantal_zitplaatsen", "seats"), ("catalogusprijs", "EUR list price")) if v.get(k)]
        if specs:
            lines.append("Specs: " + " · ".join(specs))
        fuels, fuel_day = get(FUEL, {"kenteken": value})
        for f in sorted(fuels, key=lambda f: f.get("brandstof_volgnummer", "")):
            parts = [f.get("brandstof_omschrijving", "?")]
            co2 = f.get("co2_uitstoot_gecombineerd") or f.get("emissie_co2_gecombineerd_wltp")
            use = f.get("brandstofverbruik_gecombineerd") or f.get("brandstof_verbruik_gecombineerd_wltp")
            if co2:
                parts.append(f"CO2 {co2} g/km")
            if use:
                parts.append(f"{use} l/100 km combined")
            if f.get("elektriciteitsverbruik_volledig_elektrisch") or f.get("elektrisch_verbruik_enkel_elektrisch_wltp"):
                parts.append(f"{f.get('elektriciteitsverbruik_volledig_elektrisch') or f.get('elektrisch_verbruik_enkel_elektrisch_wltp')} Wh/km electric")
            if f.get("actieradius") or f.get("actie_radius_enkel_elektrisch_wltp"):
                parts.append(f"range {f.get('actieradius') or f.get('actie_radius_enkel_elektrisch_wltp')} km")
            if f.get("uitlaatemissieniveau"):
                parts.append(f"emission level {f['uitlaatemissieniveau']}")
            if f.get("nettomaximumvermogen"):
                parts.append(f"{f['nettomaximumvermogen']} kW")
            lines.append("Fuel: " + " · ".join(parts))
        if v.get("zuinigheidsclassificatie"):
            lines.append(f"Energy label: {v['zuinigheidsclassificatie']}")
        lines += ["",
                  "The APK date is the latest the register holds and can lie in the past; for a vehicle never inspected it is "
                  "the date the APK duty starts. The insurance flag is supplied to the RDW by third parties.",
                  f"Open data, opendata.rdw.nl (CC0), register as of {day} · {link(VEHICLES, value)}",
                  f"Fuel and emissions as of {fuel_day} · {link(FUEL, value)}"]
        return "\n".join(lines)
    if name == "recalls":
        value = plate(args)
        rows, day = get(STATUS, {"kenteken": value})
        if not rows:
            return (f"No recall is registered for {value} in the open recall register (as of {day}). "
                    f"{link(STATUS, value)}")
        rows.sort(key=lambda r: (r.get("code_status") != "O", r.get("referentiecode_rdw", "")))
        codes = [r["referentiecode_rdw"] for r in rows[:10] if re.fullmatch(r"[A-Z0-9]{3,20}", r.get("referentiecode_rdw", ""))]
        where = {"$where": "referentiecode_rdw in(" + ",".join(f"'{c}'" for c in codes) + ")", "$limit": 100}
        details = {d.get("referentiecode_rdw"): d for d in get(RECALL, where)[0]} if codes else {}
        risks = {}
        for x in (get(RISK, where)[0] if codes else []):
            risks.setdefault(x.get("referentiecode_rdw"), []).append(x.get("mogelijk_gevaar", ""))
        lines = [f"# Recalls for {value}: {len(rows)}, of which {sum(r.get('code_status') == 'O' for r in rows)} open"]
        for code in codes:
            r = next(r for r in rows if r.get("referentiecode_rdw") == code)
            d = details.get(code, {})
            lines += ["", f"## {code} · {r.get('status')}",
                      f"Published by the RDW {date(d.get('publicatiedatum_rdw'))} · reported by {d.get('meldende_producent_distributeur', '?')} "
                      f"(their code {d.get('referentiecode_producent', '?')})",
                      f"Defect: {d.get('omschrijving_defect', '?')}",
                      f"What can happen: {d.get('materi_le_gevolgen', '?')}",
                      f"RDW risk rating: {RISKS.get(d.get('risicobeoordeling_rdw'), d.get('risicobeoordeling_rdw', '?'))}"
                      + ("; possible danger: " + "; ".join(risks[code]) if risks.get(code) else ""),
                      f"Remedy: {d.get('beschrijving_van_het_herstel', '?')}"]
            if d.get("meer_informatie_via_telefoonnummer"):
                lines.append(f"More information by phone: {d['meer_informatie_via_telefoonnummer']}")
        if len(rows) > 10:
            lines.append(f"\n(and {len(rows) - 10} more; the status list is at the link below)")
        lines += ["", f"Open data, opendata.rdw.nl (CC0), recall register as of {day} · {link(STATUS, value)}"]
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
