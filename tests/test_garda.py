"""Garda forecast: frozen-model golden vector, window semantics, origin gate."""
import math

import pytest
from fastapi.testclient import TestClient

from garda import model
from garda.coeffs import ORA, PELER
from garda.features import ORA_FEATURES, PELER_FEATURES, PointSeries, build_day_features
from garda.i18n import TEXT
from datetime import date


def _mean_features(block) -> dict:
    return dict(zip(block["features"], block["mean"]))


def test_score_golden_at_mean():
    """At the training mean the raw logit equals the intercept; the score is
    its Platt transform — a coeffs regen (any retrain) trips this on purpose."""
    p_ora = model.score("ora", _mean_features(ORA))
    p_peler = model.score("peler", _mean_features(PELER))
    for p, b in ((p_ora, ORA), (p_peler, PELER)):
        expected = 1 / (1 + math.exp(-(b["platt_a"] * b["intercept"] + b["platt_b"])))
        assert p == pytest.approx(expected, abs=1e-9)
    # frozen values of the 2026-07-05 export; retrain => update deliberately
    assert p_ora == pytest.approx(0.3944, abs=2e-4)
    assert p_peler == pytest.approx(0.8770, abs=2e-4)


def test_verdict_thresholds():
    assert model.verdict("ora", ORA["threshold_go"] + 0.01) == "GO"
    assert model.verdict("ora", ORA["threshold_go"] - 0.01) == "MAYBE"
    assert model.verdict("ora", ORA["threshold_maybe"] - 0.01) == "NO_GO"
    assert model.verdict("peler", PELER["threshold_go"] + 0.01) == "GO"


def test_top_drivers_include_detail_metadata():
    drivers = model.top_drivers("ora", _mean_features(ORA))
    assert len(drivers) == 3
    assert all(d["value_display"] for d in drivers)
    assert all(d["explanation"] for d in drivers)
    result = model.classify("ora", _mean_features(ORA))
    assert len(result["drivers"]) == 3
    assert len(result["other_drivers"]) == len(ORA["features"]) - 3


def test_translation_catalogs_and_localized_drivers_are_complete():
    assert set(TEXT["en"]) == set(TEXT["de"])
    assert set(TEXT["it"]) == set(TEXT["de"])

    features = _mean_features(ORA)
    de = model.classify("ora", features, lang="de")
    en = model.classify("ora", features, lang="en")
    it = model.classify("ora", features, lang="it")
    assert de["drivers"][0]["label"].startswith("Druckunterschied")
    assert en["drivers"][0]["label"].startswith("Bolzano")
    assert it["drivers"][0]["label"].startswith("Differenza")
    assert "," in de["drivers"][0]["value_display"]
    assert "." in en["drivers"][0]["value_display"]


def test_window_inclusive_and_aggregations():
    hourly = {
        "time": [f"2026-07-05T{h:02d}:00" for h in range(24)],
        "wind_speed_100m": [float(h) for h in range(24)],
    }
    ps = PointSeries(hourly)
    day = date(2026, 7, 5)
    # hours 6..10 inclusive -> mean of 6,7,8,9,10
    assert ps.window("wind_speed_100m", day, 6, 10, "mean") == pytest.approx(8.0)
    assert ps.window("wind_speed_100m", day, 6, 10, "max") == pytest.approx(10.0)
    assert ps.window("wind_speed_100m", day, 6, 10, "sum") == pytest.approx(40.0)
    assert ps.window("missing_var", day, 6, 10, "mean") is None


def test_previous_day1_suffix_stripped():
    hourly = {"time": ["2026-07-05T06:00"], "pressure_msl_previous_day1": [1013.0]}
    ps = PointSeries(hourly)
    assert ps.window("pressure_msl", date(2026, 7, 5), 6, 6, "mean") == pytest.approx(1013.0)


def _synthetic_points() -> dict:
    hours = [f"2026-07-0{d}T{h:02d}:00" for d in (4, 5) for h in range(24)]
    n = len(hours)
    tor = {"time": hours, "pressure_msl": [1013.0] * n, "cloud_cover": [20.0] * n,
           "shortwave_radiation": [500.0] * n, "temperature_2m": [22.0] * n,
           "precipitation": [0.0] * n, "relative_humidity_2m": [55.0] * n,
           "wind_speed_100m": [10.0] * n, "wind_direction_100m": [180.0] * n}
    city = {"time": hours, "pressure_msl": [1013.0] * n, "temperature_2m": [24.0] * n}
    return {"torbole": PointSeries(tor), "verona": PointSeries(city),
            "bolzano": PointSeries(city), "innsbruck": PointSeries(city)}


def test_build_day_features_complete():
    f = build_day_features(_synthetic_points(), date(2026, 7, 5))
    assert f is not None
    assert set(ORA_FEATURES) <= set(f) and set(PELER_FEATURES) <= set(f)
    assert f["w100_v"] == pytest.approx(10.0)  # wind FROM 180deg -> southerly component
    assert f["dp_bz_morn"] == pytest.approx(0.0)


def test_build_day_features_missing_returns_none():
    pts = _synthetic_points()
    pts["innsbruck"] = PointSeries({"time": [], "pressure_msl": []})
    assert build_day_features(pts, date(2026, 7, 5)) is None


def test_gate_blocks_without_secret(monkeypatch):
    monkeypatch.setenv("GARDA_GATE_SECRET", "s3cret")
    from garda.web import app
    client = TestClient(app)
    assert client.get("/health").status_code == 404
    ok = client.get("/health", headers={"X-Gate-Secret": "s3cret"})
    assert ok.status_code == 200
    assert "X-Robots-Tag" not in ok.headers


def test_gate_allows_exact_pseudonymous_custom_host(monkeypatch):
    monkeypatch.setenv("GARDA_GATE_SECRET", "s3cret")
    from garda.web import app

    client = TestClient(app)
    assert client.get("/health", headers={"host": "garda.s1st.de"}).status_code == 200
    assert client.get("/health", headers={"host": "garda.s1st.de.evil"}).status_code == 404


def test_server_event_only_for_origin_protected_real_name_host(monkeypatch):
    monkeypatch.setenv("GARDA_GATE_SECRET", "s3cret")
    monkeypatch.setenv("TRAFFIC_HASH_SECRET", "traffic-secret")
    from garda import web

    events = []
    monkeypatch.setattr(web, "emit_page_view", lambda **values: events.append(values))
    client = TestClient(web.app)
    browser_headers = {
        "user-agent": "Mozilla/5.0 (Macintosh) Safari/605.1.15",
    }

    real = client.get(
        "/erklaerung",
        headers={
            **browser_headers,
            "host": "garda.simon-stieber.de",
            "X-Gate-Secret": "s3cret",
            "CF-Connecting-IP": "84.151.20.7",
        },
    )
    assert real.status_code == 200
    assert len(events) == 1
    assert events[0]["client_ip"] == "84.151.20.7"
    assert events[0]["path"] == "/erklaerung"

    pseudonymous = client.get(
        "/erklaerung",
        headers={**browser_headers, "host": "garda.s1st.de"},
    )
    assert pseudonymous.status_code == 200
    assert len(events) == 1


def test_no_gate_when_unset(monkeypatch):
    monkeypatch.delenv("GARDA_GATE_SECRET", raising=False)
    from garda.web import app
    client = TestClient(app)
    assert client.get("/health").status_code == 200


@pytest.mark.parametrize("channel", ["reddit", "discord", "linkedin", "windinfo", "sca"])
def test_campaign_landing_paths_render_forecast(monkeypatch, channel):
    monkeypatch.delenv("GARDA_GATE_SECRET", raising=False)
    from garda import web

    async def no_forecast():
        return {}

    async def no_live_data():
        return None

    monkeypatch.setattr(web, "_forecast_points", no_forecast)
    monkeypatch.setattr(web, "_live_torbole", no_live_data)
    monkeypatch.setattr(web, "build_day_features", lambda points, day: None)

    r = TestClient(web.app).get(f"/go/{channel}")
    assert r.status_code == 200
    assert "Garda Oracle" in r.text
    assert '<link rel="canonical" href="https://garda.simon-stieber.de/">' in r.text


def test_pseudonymous_host_does_not_render_real_name_identity(monkeypatch):
    monkeypatch.setenv("GARDA_GATE_SECRET", "s3cret")
    from garda import web

    async def no_forecast():
        return {}

    async def no_live_data():
        return None

    monkeypatch.setattr(web, "_forecast_points", no_forecast)
    monkeypatch.setattr(web, "_live_torbole", no_live_data)
    monkeypatch.setattr(web, "build_day_features", lambda points, day: None)
    monkeypatch.setitem(web.templates.env.globals, "cf_beacon_token", "test-site-token")

    client = TestClient(web.app)
    r = client.get("/go/reddit", headers={"host": "garda.s1st.de"})
    assert r.status_code == 200
    assert '<link rel="canonical" href="https://garda.s1st.de/">' in r.text
    assert "https://walchensee.s1st.de/" in r.text
    assert "Simon Stieber" not in r.text
    assert "simon-stieber.de" not in r.text
    assert "https://static.cloudflareinsights.com/beacon.min.js" in r.text
    assert '"token": "test-site-token"' in r.text

    model_page = client.get("/modell", headers={"host": "garda.s1st.de"})
    assert model_page.status_code == 200
    assert "https://walchensee.s1st.de/stats" in model_page.text
    assert "simon-stieber.de" not in model_page.text

    real_name_page = client.get(
        "/",
        headers={"host": "garda.simon-stieber.de", "X-Gate-Secret": "s3cret"},
    )
    assert real_name_page.status_code == 200
    assert "https://static.cloudflareinsights.com/beacon.min.js" not in real_name_page.text
    assert "test-site-token" not in real_name_page.text


def test_unknown_campaign_landing_path_is_not_found(monkeypatch):
    monkeypatch.delenv("GARDA_GATE_SECRET", raising=False)
    from garda.web import app

    assert TestClient(app).get("/go/unknown").status_code == 404


def test_language_selector_persists_and_translates_static_pages(monkeypatch):
    monkeypatch.delenv("GARDA_GATE_SECRET", raising=False)
    from garda.web import app

    client = TestClient(app)
    r = client.get("/modell?lang=en")
    assert r.status_code == 200
    assert '<html lang="en">' in r.text
    assert "Model &amp; performance" in r.text
    assert "garda_lang=en" in r.headers.get("set-cookie", "")
    assert all(flag in r.text for flag in ("🇩🇪", "🇬🇧", "🇮🇹"))
    assert 'aria-label="Deutsch"' in r.text
    assert 'aria-label="English"' in r.text
    assert 'aria-label="Italiano"' in r.text
    assert 'aria-label="Source code on GitHub"' in r.text
    assert "Source code published on" in r.text
    assert "AGPL 3.0 license" in r.text
    assert "https://github.com/s1st/garda-oracle/blob/main/LICENSE" in r.text

    # The language cookie carries the selection to the next route.
    r = client.get("/erklaerung")
    assert "What Ora and Peler are" in r.text

    r = client.get("/erklaerung?lang=it")
    assert '<html lang="it">' in r.text
    assert "Cosa sono Ora e Peler" in r.text
    assert "La pioggia indebolisce l’Ora" in r.text
    assert 'aria-label="Codice sorgente su GitHub"' in r.text
    assert "Codice sorgente pubblicato su" in r.text


def test_legacy_beta_code_does_not_gate_public_site(monkeypatch):
    monkeypatch.delenv("GARDA_GATE_SECRET", raising=False)
    monkeypatch.setenv("GARDA_BETA_CODE", "ora4ever")
    from garda.web import app
    client = TestClient(app)

    r = client.get("/modell")
    assert r.status_code == 200
    assert "Zugangscode" not in r.text
    assert "X-Robots-Tag" not in r.headers


def test_label_day_matches_training_definition():
    from datetime import datetime
    from garda.history import label_day
    # 10-min samples all day: NE 10 kt in the peler window, S 12 kt at noon
    samples = []
    for h in range(24):
        for m in range(0, 60, 10):
            ts = datetime(2026, 7, 1, h, m)
            if 4 <= h < 9:
                samples.append((ts, 10.0, 60.0))    # NE, 10 kt
            elif 12 <= h < 17:
                samples.append((ts, 12.0, 190.0))   # S, 12 kt
            else:
                samples.append((ts, 2.0, 300.0))
    out = label_day(samples)
    assert out == {"ora": 1, "peler": 1}
    # too few samples -> None
    assert label_day(samples[:50]) == {"ora": None, "peler": None}
