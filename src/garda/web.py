"""Garda Oracle dashboard (FastAPI, Jinja templates).

Serve-time data: Open-Meteo forecast API (features, 30-min cache) and the
Meteotrentino T0193 live XML (Torbole wind panel, 5-min cache). Scoring is
pure Python via the frozen coeffs — no sklearn/pandas in this process.

GARDA_GATE_SECRET restricts the raw Cloud Run origin: every request must carry
the matching X-Gate-Secret header added by a Cloudflare Transform Rule. This is
origin protection, not a visitor-facing access gate.
"""
from __future__ import annotations

import copy
import os
import re
import time as time_mod
from datetime import date, datetime, timedelta
from functools import partial
from pathlib import Path
from typing import cast

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .features import PointSeries, build_day_features, fetch_forecast_points
from .i18n import DEFAULT_LANG, SUPPORTED_LANGS, format_number, language, translate
from .model import classify

app = FastAPI(title="Garda Oracle")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
# Cloudflare Web Analytics beacon token — set only in the deployed service
# (CF_BEACON_TOKEN env), so local/dev renders no third-party script. Cookieless;
# feeds the cross-site stats dashboard (stats.simon-stieber.de).
templates.env.globals["cf_beacon_token"] = os.environ.get("CF_BEACON_TOKEN", "")

_FORECAST_TTL = 1800
_LIVE_TTL = 300
_cache: dict[str, tuple[float, object]] = {}

MT_LIVE_URL = "https://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=T0193"
_WIND_RE = re.compile(
    r"<vento_al_suolo[^>]*>\s*<data>([^<]+)</data>\s*<v>([^<]+)</v>\s*"
    r"<vmax>([^<]+)</vmax>\s*<d>([^<]+)</d>", re.S)
KT = 1.94384


_LANG_COOKIE = "garda_lang"
_LANG_COOKIE_TTL = 365 * 24 * 3600
_PSEUDONYMOUS_HOST = "garda.s1st.de"
_REAL_NAME_HOST = "garda.simon-stieber.de"


def _request_host(request: Request) -> str:
    return (request.url.hostname or "").lower().rstrip(".")


def _is_pseudonymous_host(request: Request) -> bool:
    return _request_host(request) == _PSEUDONYMOUS_HOST


def _request_language(request: Request) -> str:
    query = request.query_params.get("lang")
    if query in SUPPORTED_LANGS:
        return query
    return language(request.cookies.get(_LANG_COOKIE, DEFAULT_LANG))


def _remember_language(response: Response, request: Request, lang: str) -> Response:
    if request.query_params.get("lang") in SUPPORTED_LANGS:
        response.set_cookie(
            _LANG_COOKIE,
            lang,
            max_age=_LANG_COOKIE_TTL,
            secure=request.url.scheme == "https",
            samesite="lax",
        )
    return response


def _page_context(request: Request, active: str, **values) -> dict:
    lang = _request_language(request)
    pseudonymous = _is_pseudonymous_host(request)
    return {
        "active": active,
        "lang": lang,
        "langs": SUPPORTED_LANGS,
        "current_path": request.url.path,
        "show_personal_link": not pseudonymous,
        "walchensee_url": (
            "https://walchensee.s1st.de" if pseudonymous else "https://walchensee.simon-stieber.de"
        ),
        "tr": partial(translate, lang),
        "num": partial(format_number, lang),
        **values,
    }


@app.middleware("http")
async def protect_origin_and_remember_language(request: Request, call_next):
    lang = _request_language(request)
    request.state.lang = lang
    secret = os.environ.get("GARDA_GATE_SECRET")
    # garda.s1st.de is mapped directly through Google's custom-domain frontend
    # and therefore cannot receive the Cloudflare-injected origin header.
    if secret and not _is_pseudonymous_host(request) and request.headers.get("x-gate-secret") != secret:
        return Response("Not found", status_code=404)
    response = await call_next(request)
    return _remember_language(response, request, lang)


async def _forecast_points() -> dict[str, PointSeries]:
    hit = _cache.get("forecast")
    if hit and time_mod.time() - hit[0] < _FORECAST_TTL:
        return hit[1]  # type: ignore[return-value]
    points = await fetch_forecast_points()
    _cache["forecast"] = (time_mod.time(), points)
    return points


async def _live_torbole() -> dict | None:
    hit = _cache.get("live")
    if hit and time_mod.time() - hit[0] < _LIVE_TTL:
        return hit[1]  # type: ignore[return-value]
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(MT_LIVE_URL)
            r.raise_for_status()
        samples: list[dict] = [
            {"time": m.group(1)[11:16], "avg_kt": round(float(m.group(2)) * KT, 1),
             "gust_kt": round(float(m.group(3)) * KT, 1), "dir": int(float(m.group(4)))}
            for m in _WIND_RE.finditer(r.text)
            if float(m.group(2)) >= 0
        ]
        live = samples[-1] if samples else None
        payload = {"latest": live, "recent": samples[-12:]}
    except Exception:
        payload = None  # Torbole live feed is best-effort, never blocks the page
    _cache["live"] = (time_mod.time(), payload)
    return payload


def _sector(deg: int, lang: str) -> str:
    names = {
        "de": ["N", "NO", "O", "SO", "S", "SW", "W", "NW"],
        "en": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
        "it": ["N", "NE", "E", "SE", "S", "SO", "O", "NO"],
    }[language(lang)]
    return names[int((deg + 22.5) % 360 // 45)]


def _date_label(day: date, lang: str) -> str:
    weekdays = {
        "de": ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."],
        "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "it": ["lun", "mar", "mer", "gio", "ven", "sab", "dom"],
    }[language(lang)]
    if lang == "en":
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return f"{weekdays[day.weekday()]} {day.day} {months[day.month - 1]}"
    return f"{weekdays[day.weekday()]} {day:%d.%m.}" if lang == "de" else (
        f"{weekdays[day.weekday()]} {day:%d/%m}"
    )


def _date_long(day: date, lang: str) -> str:
    if lang == "en":
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        return f"{day.day} {months[day.month - 1]} {day.year}"
    return f"{day:%d.%m.%Y}" if lang == "de" else f"{day:%d/%m/%Y}"


def _date_short(day: date, lang: str) -> str:
    if lang == "en":
        return f"{day.day}/{day.month}"
    return f"{day:%d.%m.}" if lang == "de" else f"{day:%d/%m}"


@app.get("/go/reddit", response_class=HTMLResponse, include_in_schema=False)
@app.get("/go/discord", response_class=HTMLResponse, include_in_schema=False)
@app.get("/go/linkedin", response_class=HTMLResponse, include_in_schema=False)
@app.get("/go/windinfo", response_class=HTMLResponse, include_in_schema=False)
@app.get("/go/sca", response_class=HTMLResponse, include_in_schema=False)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    lang = _request_language(request)
    points = await _forecast_points()
    now = datetime.now()
    days = []
    for offset in range(3):
        day = date.today() + timedelta(days=offset)
        day_context = {
            "date": day,
            "label": [
                translate(lang, "day_today"),
                translate(lang, "day_tomorrow"),
                translate(lang, "day_after"),
            ][offset],
            "date_label": _date_label(day, lang),
            "date_long": _date_long(day, lang),
        }
        f = build_day_features(points, day)
        if f is None:
            days.append({**day_context, "error": True})
            continue
        peler = classify("peler", f, lang=lang)
        ora = classify("ora", f, lang=lang)
        days.append({
            **day_context,
            "peler": peler,
            "ora": ora,
            "peler_past": offset == 0 and now.hour >= 10,
            "error": False,
        })
    live = await _live_torbole()
    if live and live.get("latest"):
        live = {
            "latest": {
                **live["latest"],
                "sector": _sector(live["latest"]["dir"], lang),
            },
            "recent": live["recent"],
        }
    return templates.TemplateResponse(
        request,
        "index.html",
        _page_context(
            request,
            "index",
            days=days,
            live=live,
            canonical_url=(
                f"https://{_PSEUDONYMOUS_HOST}/"
                if _is_pseudonymous_host(request)
                else f"https://{_REAL_NAME_HOST}/"
            ),
        ),
    )


_HISTORY_TTL = 6 * 3600


@app.get("/verlauf", response_class=HTMLResponse)
async def verlauf(request: Request):
    from .history import build_strip, hindcast_verdicts, observed_labels

    lang = _request_language(request)
    hit = _cache.get("verlauf")
    strip: dict | None
    if hit and time_mod.time() - hit[0] < _HISTORY_TTL:
        strip = cast(dict, hit[1])
    else:
        try:
            observed = await observed_labels(30)
            hindcast = await hindcast_verdicts(30)
            strip = build_strip(30, observed, hindcast)
            _cache["verlauf"] = (time_mod.time(), strip)
        except Exception:
            strip = None  # upstream hiccup: render the page with a notice
    if strip is not None:
        strip = copy.deepcopy(strip)
        for cell in strip["cells"]:
            cell["label"] = _date_short(cell["date"], lang)
    return templates.TemplateResponse(
        request, "verlauf.html", _page_context(request, "verlauf", strip=strip)
    )


@app.get("/erklaerung", response_class=HTMLResponse)
async def erklaerung(request: Request):
    return templates.TemplateResponse(
        request, "erklaerung.html", _page_context(request, "erklaerung")
    )


@app.get("/modell", response_class=HTMLResponse)
async def modell(request: Request):
    return templates.TemplateResponse(
        request, "modell.html", _page_context(request, "modell")
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
