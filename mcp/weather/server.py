#!/usr/bin/env python3
"""Current weather and the forecast for a place, by name or by coordinates, as tools for any MCP client.

Why this exists: "do I need a coat tomorrow?" deserves the forecast, not a guess. Open-Meteo combines the
open models of national weather services (KNMI, DWD, ECMWF, Météo-France and others) behind one free API
without a key, and has its own geocoding API for place names. This server reads only those two Open-Meteo
hosts, over https. Nothing is stored beyond this process; the place or coordinates asked about are sent
to Open-Meteo, which keeps web server logs (which may contain coordinates) for up to 90 days.

  find_place   name, country?, count?                       places matching a name, with coordinates
  current      place? | lat + lon, country?                  the weather now: temperature, feels-like,
                                                            wind, rain, cloud, humidity
  forecast     place? | lat + lon, country?, days?, hours?   the day-by-day forecast (up to 16 days),
                                                            optionally hour by hour for the next hours

Open-Meteo's terms: the free API is for non-commercial use only (private or non-profit apps, personal home
automation, public research, education), under 10,000 calls a day, 5,000 an hour and 600 a minute; data are
CC BY 4.0 and must be credited with a link to open-meteo.com. Commercial use needs a paid plan. There is no
weather-warnings tool: KNMI's warnings API needs an API key, and this server is keyless.
"""
import datetime
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

NAME = "weather"
VERSION = "1.0.0"
INSTRUCTIONS = ("Weather now and the forecast for a place, from Open-Meteo. Give a place name, or lat and lon. Credit "
                "\"Weather data by Open-Meteo.com\" with the link it gives. Free use is non-commercial only.")
FORECAST = "https://api.open-meteo.com/v1/forecast"
GEOCODE = "https://geocoding-api.open-meteo.com/v1/search"
HOSTS = {"api.open-meteo.com", "geocoding-api.open-meteo.com"}
TIMEOUT = 30
CREDIT = "Weather data by Open-Meteo.com (CC BY 4.0) · https://open-meteo.com/"
CODES = {0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast", 45: "fog", 48: "depositing rime fog",
         51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle", 56: "light freezing drizzle",
         57: "dense freezing drizzle", 61: "slight rain", 63: "moderate rain", 65: "heavy rain",
         66: "light freezing rain", 67: "heavy freezing rain", 71: "slight snowfall", 73: "moderate snowfall",
         75: "heavy snowfall", 77: "snow grains", 80: "slight rain showers", 81: "moderate rain showers",
         82: "violent rain showers", 85: "slight snow showers", 86: "heavy snow showers", 95: "thunderstorm",
         96: "thunderstorm with slight hail", 97: "heavy thunderstorm", 99: "thunderstorm with heavy hail"}
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
PLACE = {"place": {"type": "string", "description": "A place name, like Utrecht or \"Paris, France\". Or give lat and lon."},
         "country": {"type": "string", "description": "Two-letter country code to pick the right place, like NL."},
         "lat": {"type": "number", "minimum": -90, "maximum": 90, "description": "Latitude, WGS84."},
         "lon": {"type": "number", "minimum": -180, "maximum": 180, "description": "Longitude, WGS84."}}

TOOLS = [
    {"name": "find_place", "description": "Places in the world matching a name (or postcode), with country, region, coordinates, elevation and time zone. Use it when a name is ambiguous, then pass lat and lon to current or forecast.",
     "inputSchema": {"type": "object", "properties": {
         "name": {"type": "string", "description": "The place name; add \", country\" or \", region\" to narrow it."},
         "country": {"type": "string", "description": "Two-letter country code, like NL."},
         "count": {"type": "integer", "minimum": 1, "maximum": 20, "description": "How many places at most. Default 5."}},
         "required": ["name"]}},
    {"name": "current", "description": "The weather right now at a place: condition, temperature and feels-like, precipitation, cloud cover, humidity, wind speed, gusts and direction, with the local time it holds for.",
     "inputSchema": {"type": "object", "properties": dict(PLACE)}},
    {"name": "forecast", "description": "The forecast for a place, day by day for up to 16 days (condition, min and max temperature, precipitation and its chance, wind, sunrise and sunset), and optionally hour by hour for the next hours.",
     "inputSchema": {"type": "object", "properties": {**PLACE,
         "days": {"type": "integer", "minimum": 1, "maximum": 16, "description": "How many days, from today. Default 3."},
         "hours": {"type": "integer", "minimum": 0, "maximum": 48, "description": "Also this many hours hour by hour, from now. Default 0."}}}},
]


def get(url, params):
    """Read JSON from Open-Meteo's own two hosts only, https, with a deadline, checked after any redirect."""
    request = urllib.request.Request(url + "?" + urllib.parse.urlencode(params),
                                     headers={"User-Agent": f"okayiris-weather-mcp/{VERSION}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as r:
            where = urllib.parse.urlsplit(r.geturl())
            if where.scheme != "https" or where.hostname not in HOSTS:
                raise ValueError(f"refused to read {where.scheme}://{where.hostname}: not an Open-Meteo host")
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            reason = json.loads(e.read()).get("reason", e.reason)
        except ValueError:
            reason = e.reason
        if e.code == 429:
            raise ValueError("Open-Meteo says too many requests (429); the free API allows 600 a minute and 10,000 a day")
        raise ValueError(f"Open-Meteo answered {e.code}: {reason}")


def country(args):
    value = str(args.get("country") or "").strip().upper()
    if value and not re.fullmatch(r"[A-Z]{2}", value):
        raise ValueError(f"country is a two-letter code like NL, not {value}")
    return value


def places(name, code, count):
    name = " ".join(str(name or "").split())
    if not 2 <= len(name) <= 100 or not re.fullmatch(r"[\w\s,.'()\-]+", name):
        raise ValueError("a place name is 2 to 100 letters, like Utrecht or \"Paris, France\"")
    params = {"name": name, "count": count, "language": "en", "format": "json"}
    if code:
        params["countryCode"] = code
    found = get(GEOCODE, params).get("results") or []
    if not found:
        raise ValueError(f"no place called {name}{' in ' + code if code else ''}; try the English or local name, or give lat and lon")
    return found


def label(p):
    return ", ".join(x for x in (p.get("name"), p.get("admin1"), p.get("country")) if x)


def where(args):
    """The coordinates asked for, from a place name or from lat and lon."""
    if args.get("place"):
        p = places(args["place"], country(args), 1)[0]
        return p["latitude"], p["longitude"], label(p)
    lat, lon = args.get("lat"), args.get("lon")
    for value, name, limit in ((lat, "lat", 90), (lon, "lon", 180)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not -limit <= value <= limit:
            raise ValueError(f"give a place name, or {name} as a number from -{limit} to {limit}")
    return float(lat), float(lon), f"{lat:.4f}, {lon:.4f}"


def wind(speed, degrees):
    side = COMPASS[round((degrees or 0) / 45) % 8] if degrees is not None else "?"
    return f"{speed} km/h from {side}"


def whole(args, name, default, low, high):
    value = args.get(name, default)
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{name} is a whole number from {low} to {high}, not {value!r}")
    return value


def link(lat, lon):
    return f"{FORECAST}?latitude={lat:.4f}&longitude={lon:.4f}"


def call(name, args):
    if name == "find_place":
        found = places(args.get("name"), country(args), whole(args, "count", 5, 1, 20))
        lines = [f"{len(found)} place(s):"]
        for p in found:
            lines.append(f"- {label(p)} · {p['latitude']:.4f}, {p['longitude']:.4f} · {p.get('elevation', '?')} m · "
                         f"{p.get('timezone', '?')}" + (f" · population {p['population']}" if p.get("population") else ""))
        return "\n".join(lines + ["Place names from GeoNames via the Open-Meteo geocoding API (CC BY 4.0)."])
    if name == "current":
        lat, lon, place = where(args)
        data = get(FORECAST, {"latitude": f"{lat:.4f}", "longitude": f"{lon:.4f}", "timezone": "auto",
                              "current": "temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,"
                                         "cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m"})
        c = data["current"]
        return "\n".join([f"# Weather now in {place}",
                          f"{CODES.get(c.get('weather_code'), 'code ' + str(c.get('weather_code')))}, {c['temperature_2m']} °C "
                          f"(feels like {c['apparent_temperature']} °C)",
                          f"Precipitation {c['precipitation']} mm · cloud cover {c['cloud_cover']}% · humidity {c['relative_humidity_2m']}%",
                          f"Wind {wind(c['wind_speed_10m'], c.get('wind_direction_10m'))}, gusts {c['wind_gusts_10m']} km/h",
                          f"Model data for {c['time']} local time ({data.get('timezone')}), grid point {data['latitude']:.3f}, {data['longitude']:.3f}, {data.get('elevation')} m",
                          f"{CREDIT} · {link(lat, lon)}"])
    if name == "forecast":
        lat, lon, place = where(args)
        days, hours = whole(args, "days", 3, 1, 16), whole(args, "hours", 0, 0, 48)
        params = {"latitude": f"{lat:.4f}", "longitude": f"{lon:.4f}", "timezone": "auto", "forecast_days": days,
                  "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,"
                           "wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,sunrise,sunset"}
        if hours:
            params.update({"hourly": "temperature_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m",
                           "forecast_hours": hours})
        data = get(FORECAST, params)
        d = data["daily"]
        lines = [f"# Forecast for {place} ({data.get('timezone')}, grid point {data['latitude']:.3f}, {data['longitude']:.3f})"]
        for i, day in enumerate(d["time"]):
            lines.append(f"- {day}: {CODES.get(d['weather_code'][i], 'code ' + str(d['weather_code'][i]))}, "
                         f"{d['temperature_2m_min'][i]} to {d['temperature_2m_max'][i]} °C, "
                         f"{d['precipitation_sum'][i]} mm ({d['precipitation_probability_max'][i]}% chance), "
                         f"wind up to {wind(d['wind_speed_10m_max'][i], d['wind_direction_10m_dominant'][i])}, "
                         f"gusts {d['wind_gusts_10m_max'][i]} km/h, sun {d['sunrise'][i][11:]} to {d['sunset'][i][11:]}")
        if hours:
            h = data["hourly"]
            lines.append("\nHour by hour:")
            for i, t in enumerate(h["time"]):
                lines.append(f"- {t.replace('T', ' ')}: {CODES.get(h['weather_code'][i], '?')}, {h['temperature_2m'][i]} °C, "
                             f"{h['precipitation'][i]} mm ({h['precipitation_probability'][i]}%), wind {h['wind_speed_10m'][i]} km/h")
        read = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        lines.append(f"Forecast read {read}; times are local. {CREDIT} · {link(lat, lon)}")
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
