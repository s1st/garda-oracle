"""Shared Ora/Peler feature builder — pure Python, no pandas/numpy.

The SAME window aggregation runs at training time (export script feeding it
the stored ERA5/previous-runs JSON) and at serve time (feeding it the live
forecast API response), so train and serve cannot drift. Window semantics
mirror the spike's pandas ``.loc[day+h1 : day+h2]``: hours h1..h2 INCLUSIVE.

Points: torbole (full variable set), verona / bolzano / innsbruck (pressure +
temperature). All series are hourly, local time (Europe/Berlin ISO strings,
as returned by Open-Meteo with ``timezone=Europe/Berlin``).
"""
from __future__ import annotations

import math
from datetime import date, datetime, time, timedelta

import httpx

POINTS: dict[str, tuple[float, float, str]] = {
    "torbole": (45.87, 10.877,
                "pressure_msl,cloud_cover,shortwave_radiation,temperature_2m,"
                "precipitation,relative_humidity_2m,wind_speed_100m,wind_direction_100m"),
    "verona": (45.44, 10.99, "pressure_msl,temperature_2m"),
    "bolzano": (46.50, 11.35, "pressure_msl,temperature_2m"),
    "innsbruck": (47.27, 11.39, "pressure_msl,temperature_2m"),
}

ORA_FEATURES = ["dp_bz_morn", "dp_ib_morn", "dp_ib_trend", "dtmax_ve_ib", "solar_morn",
                "cloud_morn", "rh_morn", "precip_day", "w100_noon", "w100_u", "w100_v", "tmax_tor"]
PELER_FEATURES = ["dp_ib_night", "dp_bz_night", "cloud_night", "precip_night", "w100_night",
                  "solar_prev_pm", "rh_night", "dp_ib_morn", "dtmax_ve_ib"]

# human-readable driver names for the dashboard (DE)
FEATURE_LABELS_DE = {
    "dp_bz_morn": "Druckunterschied Bozen−Verona (früh)",
    "dp_ib_morn": "Druckunterschied Innsbruck−Verona (früh)",
    "dp_ib_trend": "Entwicklung des Druckgefälles (früh → mittags)",
    "dtmax_ve_ib": "Erwärmungsunterschied Po-Ebene–Alpen",
    "solar_morn": "Einstrahlung am Vormittag",
    "cloud_morn": "Bewölkung am Vormittag",
    "rh_morn": "Luftfeuchte am Morgen",
    "precip_day": "Tagesniederschlag",
    "w100_noon": "Wind in 100 m Höhe (mittags)",
    "w100_u": "Westkomponente des Winds in 100 m Höhe",
    "w100_v": "Südkomponente des Winds in 100 m Höhe",
    "tmax_tor": "Tageshöchsttemperatur",
    "dp_ib_night": "Druckgefälle Innsbruck−Verona (nachts)",
    "dp_bz_night": "Druckgefälle Bozen−Verona (nachts)",
    "cloud_night": "Bewölkung in der Nacht",
    "precip_night": "Regen am Abend und in der Nacht",
    "w100_night": "Wind in 100 m Höhe (nachts)",
    "solar_prev_pm": "Einstrahlung am Vortagnachmittag",
    "rh_night": "Luftfeuchte nachts",
}

# Longer explanations and display units for the forecast-detail dialog.
# These describe the physical signal represented by each model feature. The
# sign of its effect for a particular forecast comes from the fitted model and
# is shown separately in the UI.
FEATURE_DETAILS_DE = {
    "dp_bz_morn": (
        "hPa",
        "Das Druckgefälle zwischen Bozen und Verona bildet die Luftdruckverteilung "
        "zwischen Alpenraum und Po-Ebene ab. Diese beeinflusst den thermischen Sog durch das Sarcatal.",
    ),
    "dp_ib_morn": (
        "hPa",
        "Das Druckgefälle Innsbruck−Verona beschreibt die großräumige Druckverteilung "
        "zwischen Alpen und Po-Ebene. Ein sehr starkes Gefälle aus Norden kann die Ora "
        "unterdrücken; bei einer passenden Druckverteilung kann sie sich ungestörter entwickeln.",
    ),
    "dp_ib_trend": (
        "hPa",
        "Dieser Wert zeigt, wie sich das Druckgefälle Innsbruck−Verona vom frühen "
        "Morgen bis Mittag verändert.",
    ),
    "dtmax_ve_ib": (
        "°C",
        "Der Temperaturkontrast zwischen Verona und Innsbruck steht für die "
        "unterschiedliche Erwärmung von Po-Ebene und Alpenraum und damit für den thermischen Antrieb.",
    ),
    "solar_morn": (
        "W/m²",
        "Kräftige Vormittagssonne erwärmt Hänge und Täler. Diese Erwärmung baut den "
        "Druckunterschied auf, der die Ora in Richtung Nordufer zieht.",
    ),
    "cloud_morn": (
        "%",
        "Bewölkung am Vormittag reduziert die Sonneneinstrahlung und damit die Energie "
        "für den thermischen Aufbau der Ora.",
    ),
    "rh_morn": (
        "%",
        "Hohe Luftfeuchte geht häufig mit gedämpfter Erwärmung, Dunst oder Wolken einher. "
        "Bei trockenerer Luft kann sich die Thermik meist ungestörter entwickeln.",
    ),
    "precip_day": (
        "mm",
        "Regen und Schauer begrenzen die Erwärmung und können die lokale Zirkulation "
        "unterbrechen. Niederschlag tagsüber spricht daher meist gegen Ora.",
    ),
    "w100_noon": (
        "km/h",
        "Der Wind in 100 Metern Höhe beschreibt die großräumige Strömung über dem See. "
        "Je nach Richtung kann sie das lokale Windsystem stützen oder überlagern.",
    ),
    "w100_u": (
        "km/h",
        "Die West-Ost-Komponente des Winds in 100 Metern Höhe hilft dem Modell, die Richtung der "
        "großräumigen Strömung getrennt von ihrer Gesamtstärke zu bewerten.",
    ),
    "w100_v": (
        "km/h",
        "Die Süd-Nord-Komponente des Winds zeigt, ob die großräumige Strömung mit "
        "der Ora gleichgerichtet ist oder ihr entgegenwirkt.",
    ),
    "tmax_tor": (
        "°C",
        "Die erwartete Höchsttemperatur in Torbole ist ein Maß für das Ausmaß der "
        "Erwärmung und die verfügbare thermische Energie.",
    ),
    "dp_ib_night": (
        "hPa",
        "Der nächtliche Innsbruck−Verona-Gradient beschreibt den großräumigen "
        "Druckantrieb über den Alpen, während sich der Peler aufbaut.",
    ),
    "dp_bz_night": (
        "hPa",
        "Das nächtliche Druckgefälle Bozen−Verona ist der stärkste Drucktreiber im "
        "Peler-Modell: Es zeigt, ob Luft aus dem nördlichen Seeteil nach Süden gedrückt wird.",
    ),
    "cloud_night": (
        "%",
        "Wolken bremsen die nächtliche Auskühlung. Eine klare Nacht unterstützt die "
        "Temperatur- und Druckunterschiede, aus denen sich der Peler entwickelt.",
    ),
    "precip_night": (
        "mm",
        "Regen am Abend oder in der Nacht beeinflusst die Auskühlung, verändert die "
        "Luftmasse und stört häufig den ungestörten Aufbau des morgendlichen Peler.",
    ),
    "w100_night": (
        "km/h",
        "Der nächtliche Wind in 100 Metern Höhe zeigt, ob eine großräumige Strömung "
        "den Peler unterstützt, überlagert oder die Luftschichtung durchmischt.",
    ),
    "solar_prev_pm": (
        "W/m²",
        "Die Einstrahlung am Vortag beeinflusst, wie stark sich Land und Bergflanken "
        "aufgeheizt haben und unter welchen Bedingungen die nächtliche Zirkulation einsetzt.",
    ),
    "rh_night": (
        "%",
        "Die nächtliche Luftfeuchte beschreibt die Luftmasse und zeigt, ob sich "
        "Wolken oder Nebel bilden können, die den Aufbau des Peler verändern.",
    ),
}

FEATURE_LABELS_EN = {
    "dp_bz_morn": "Bolzano−Verona pressure difference (morning)",
    "dp_ib_morn": "Innsbruck−Verona pressure difference (morning)",
    "dp_ib_trend": "Pressure-gradient trend (morning → midday)",
    "dtmax_ve_ib": "Po Valley–Alps heating contrast",
    "solar_morn": "Morning solar radiation",
    "cloud_morn": "Morning cloud cover",
    "rh_morn": "Morning humidity",
    "precip_day": "Daytime precipitation",
    "w100_noon": "Wind at 100 m (midday)",
    "w100_u": "West–east wind component at 100 m",
    "w100_v": "South–north wind component at 100 m",
    "tmax_tor": "Daily maximum temperature",
    "dp_ib_night": "Innsbruck−Verona pressure gradient (overnight)",
    "dp_bz_night": "Bolzano−Verona pressure gradient (overnight)",
    "cloud_night": "Overnight cloud cover",
    "precip_night": "Evening and overnight rain",
    "w100_night": "Wind at 100 m (overnight)",
    "solar_prev_pm": "Previous-afternoon solar radiation",
    "rh_night": "Overnight humidity",
}

FEATURE_DETAILS_EN = {
    "dp_bz_morn": (
        "hPa",
        "The pressure gradient between Bolzano and Verona represents the pressure "
        "distribution between the Alps and Po Valley. This affects the thermal draw through the Sarca Valley.",
    ),
    "dp_ib_morn": (
        "hPa",
        "The Innsbruck−Verona gradient describes the broad pressure distribution "
        "between the Alps and Po Valley. A very strong northerly gradient can suppress "
        "Ora; a favourable distribution lets it develop more freely.",
    ),
    "dp_ib_trend": (
        "hPa",
        "This value shows how the Innsbruck−Verona pressure gradient changes from "
        "early morning to midday.",
    ),
    "dtmax_ve_ib": (
        "°C",
        "The temperature contrast between Verona and Innsbruck represents the different "
        "rates of heating in the Po Valley and Alpine region, and therefore the thermal drive.",
    ),
    "solar_morn": (
        "W/m²",
        "Strong morning sunshine heats slopes and valleys. This builds the pressure "
        "difference that draws Ora towards the northern end of the lake.",
    ),
    "cloud_morn": (
        "%",
        "Morning cloud reduces solar radiation and therefore the energy available "
        "for Ora’s thermal development.",
    ),
    "rh_morn": (
        "%",
        "High humidity often accompanies weaker heating, haze or cloud. In drier air, "
        "the thermal circulation can usually develop more freely.",
    ),
    "precip_day": (
        "mm",
        "Rain and showers limit heating and can interrupt the local circulation. "
        "Daytime precipitation therefore usually works against Ora.",
    ),
    "w100_noon": (
        "km/h",
        "Wind at 100 metres represents the broad flow over the lake. Depending on its "
        "direction, it can support or override the local wind system.",
    ),
    "w100_u": (
        "km/h",
        "The west–east component of the wind at 100 metres lets the model assess the "
        "direction of the broad flow separately from its overall speed.",
    ),
    "w100_v": (
        "km/h",
        "The south–north wind component shows whether the broad flow is aligned with "
        "Ora or works against it.",
    ),
    "tmax_tor": (
        "°C",
        "The expected maximum temperature in Torbole represents the amount of daytime "
        "heating and the thermal energy available.",
    ),
    "dp_ib_night": (
        "hPa",
        "The overnight Innsbruck−Verona gradient describes the broad pressure drive "
        "across the Alps while Peler is developing.",
    ),
    "dp_bz_night": (
        "hPa",
        "The overnight Bolzano−Verona pressure difference is the strongest pressure "
        "driver in the Peler model: it indicates whether air is being pushed south along the lake.",
    ),
    "cloud_night": (
        "%",
        "Cloud slows overnight cooling. A clear night supports the temperature and "
        "pressure differences from which Peler develops.",
    ),
    "precip_night": (
        "mm",
        "Evening or overnight rain affects cooling, changes the air mass and often "
        "disrupts Peler’s development.",
    ),
    "w100_night": (
        "km/h",
        "Overnight wind at 100 metres shows whether the broad flow supports Peler, "
        "overrides it or mixes the lower atmosphere.",
    ),
    "solar_prev_pm": (
        "W/m²",
        "Previous-afternoon sunshine affects how strongly the land and mountain slopes "
        "heated up and the conditions in which the overnight circulation begins.",
    ),
    "rh_night": (
        "%",
        "Overnight humidity describes the air mass and indicates whether cloud or fog "
        "may form and alter Peler’s development.",
    ),
}

FEATURE_LABELS_IT = {
    "dp_bz_morn": "Differenza di pressione Bolzano−Verona (mattino)",
    "dp_ib_morn": "Differenza di pressione Innsbruck−Verona (mattino)",
    "dp_ib_trend": "Evoluzione del gradiente (mattino → mezzogiorno)",
    "dtmax_ve_ib": "Differenza di riscaldamento Pianura Padana–Alpi",
    "solar_morn": "Irraggiamento del mattino",
    "cloud_morn": "Nuvolosità del mattino",
    "rh_morn": "Umidità del mattino",
    "precip_day": "Precipitazioni diurne",
    "w100_noon": "Vento a 100 m (mezzogiorno)",
    "w100_u": "Componente ovest–est del vento a 100 m",
    "w100_v": "Componente sud–nord del vento a 100 m",
    "tmax_tor": "Temperatura massima giornaliera",
    "dp_ib_night": "Gradiente Innsbruck−Verona (notte)",
    "dp_bz_night": "Gradiente Bolzano−Verona (notte)",
    "cloud_night": "Nuvolosità notturna",
    "precip_night": "Pioggia serale e notturna",
    "w100_night": "Vento a 100 m (notte)",
    "solar_prev_pm": "Irraggiamento del pomeriggio precedente",
    "rh_night": "Umidità notturna",
}

FEATURE_DETAILS_IT = {
    "dp_bz_morn": (
        "hPa",
        "Il gradiente tra Bolzano e Verona rappresenta la distribuzione della pressione "
        "tra le Alpi e la Pianura Padana. Questa influenza il richiamo termico attraverso la valle del Sarca.",
    ),
    "dp_ib_morn": (
        "hPa",
        "Il gradiente Innsbruck−Verona descrive la distribuzione della pressione tra "
        "le Alpi e la Pianura Padana. Un gradiente da nord molto forte può sopprimere "
        "l’Ora; una distribuzione favorevole le permette di svilupparsi meglio.",
    ),
    "dp_ib_trend": (
        "hPa",
        "Questo valore mostra come cambia il gradiente Innsbruck−Verona dal primo "
        "mattino a mezzogiorno.",
    ),
    "dtmax_ve_ib": (
        "°C",
        "Il contrasto termico tra Verona e Innsbruck rappresenta il diverso "
        "riscaldamento della Pianura Padana e della regione alpina, quindi il motore termico.",
    ),
    "solar_morn": (
        "W/m²",
        "Un forte irraggiamento mattutino riscalda pendii e valli. Questo crea la "
        "differenza di pressione che richiama l’Ora verso l’Alto Garda.",
    ),
    "cloud_morn": (
        "%",
        "La nuvolosità del mattino riduce l’irraggiamento solare e quindi l’energia "
        "disponibile per lo sviluppo termico dell’Ora.",
    ),
    "rh_morn": (
        "%",
        "Un’umidità elevata è spesso associata a minore riscaldamento, foschia o nubi. "
        "Con aria più secca la circolazione termica può svilupparsi più liberamente.",
    ),
    "precip_day": (
        "mm",
        "Pioggia e rovesci limitano il riscaldamento e possono interrompere la "
        "circolazione locale. Le precipitazioni diurne sfavoriscono quindi l’Ora.",
    ),
    "w100_noon": (
        "km/h",
        "Il vento a 100 metri rappresenta il flusso su larga scala sopra il lago. "
        "A seconda della direzione può sostenere o prevalere sul sistema locale.",
    ),
    "w100_u": (
        "km/h",
        "La componente ovest–est del vento a 100 metri permette al modello di valutare "
        "la direzione del flusso separatamente dalla sua velocità complessiva.",
    ),
    "w100_v": (
        "km/h",
        "La componente sud–nord indica se il flusso su larga scala è allineato con "
        "l’Ora oppure la contrasta.",
    ),
    "tmax_tor": (
        "°C",
        "La temperatura massima prevista a Torbole rappresenta l’entità del "
        "riscaldamento diurno e l’energia termica disponibile.",
    ),
    "dp_ib_night": (
        "hPa",
        "Il gradiente notturno Innsbruck−Verona descrive la spinta barica su larga "
        "scala attraverso le Alpi mentre si forma il Peler.",
    ),
    "dp_bz_night": (
        "hPa",
        "La differenza di pressione notturna Bolzano−Verona è il principale fattore "
        "barico del modello Peler: indica se l’aria viene spinta verso sud lungo il lago.",
    ),
    "cloud_night": (
        "%",
        "Le nubi rallentano il raffreddamento notturno. Una notte serena favorisce le "
        "differenze di temperatura e pressione da cui si sviluppa il Peler.",
    ),
    "precip_night": (
        "mm",
        "La pioggia serale o notturna influenza il raffreddamento, modifica la massa "
        "d’aria e spesso disturba lo sviluppo del Peler.",
    ),
    "w100_night": (
        "km/h",
        "Il vento notturno a 100 metri mostra se il flusso generale sostiene il Peler, "
        "lo sovrasta oppure rimescola gli strati più bassi.",
    ),
    "solar_prev_pm": (
        "W/m²",
        "L’irraggiamento del pomeriggio precedente influenza il riscaldamento del "
        "terreno e dei pendii e le condizioni iniziali della circolazione notturna.",
    ),
    "rh_night": (
        "%",
        "L’umidità notturna descrive la massa d’aria e indica se possono formarsi nubi "
        "o nebbia capaci di modificare lo sviluppo del Peler.",
    ),
}

FEATURE_LABELS = {
    "de": FEATURE_LABELS_DE,
    "en": FEATURE_LABELS_EN,
    "it": FEATURE_LABELS_IT,
}
FEATURE_DETAILS = {
    "de": FEATURE_DETAILS_DE,
    "en": FEATURE_DETAILS_EN,
    "it": FEATURE_DETAILS_IT,
}


class PointSeries:
    """Hourly series for one point: {'2026-07-05T14:00' -> value} per variable."""

    def __init__(self, hourly: dict) -> None:
        times = hourly["time"]
        self.vars: dict[str, dict[str, float]] = {}
        for name, values in hourly.items():
            if name == "time":
                continue
            base = name.removesuffix("_previous_day1")
            self.vars[base] = {t[:13]: v for t, v in zip(times, values) if v is not None}

    def window(self, var: str, day: date, h1: int, h2: int, agg: str) -> float | None:
        series = self.vars.get(var, {})
        vals = []
        for h in range(h1, h2 + 1):
            v = series.get(_key(day, h))
            if v is not None:
                vals.append(v)
        if not vals:
            return None
        if agg == "mean":
            return sum(vals) / len(vals)
        if agg == "max":
            return max(vals)
        if agg == "sum":
            return sum(vals)
        raise ValueError(agg)


def _key(day: date, hour: int) -> str:
    ts = datetime.combine(day, time()) + timedelta(hours=hour)
    return ts.isoformat()[:13]


def _delta_window(a: PointSeries, b: PointSeries, var: str, day: date,
                  h1: int, h2: int) -> float | None:
    vals = []
    for h in range(h1, h2 + 1):
        k = _key(day, h)
        va, vb = a.vars.get(var, {}).get(k), b.vars.get(var, {}).get(k)
        if va is not None and vb is not None:
            vals.append(va - vb)
    return sum(vals) / len(vals) if vals else None


def build_day_features(points: dict[str, PointSeries], day: date) -> dict[str, float] | None:
    """All Ora+Peler features for one target day; None if anything is missing."""
    tor, ver, bz, ib = points["torbole"], points["verona"], points["bolzano"], points["innsbruck"]
    prev = day - timedelta(days=1)

    dp_ib_11_13 = _delta_window(ib, ver, "pressure_msl", day, 11, 13)
    dp_ib_5_7 = _delta_window(ib, ver, "pressure_msl", day, 5, 7)
    tmax_ve = ver.window("temperature_2m", day, 6, 16, "max")
    tmax_ib = ib.window("temperature_2m", day, 6, 16, "max")
    f: dict[str, float | None] = {
        "dp_bz_morn": _delta_window(bz, ver, "pressure_msl", day, 6, 10),
        "dp_ib_morn": _delta_window(ib, ver, "pressure_msl", day, 6, 10),
        "dp_ib_trend": (dp_ib_11_13 - dp_ib_5_7)
                       if dp_ib_11_13 is not None and dp_ib_5_7 is not None else None,
        "dtmax_ve_ib": (tmax_ve - tmax_ib) if tmax_ve is not None and tmax_ib is not None else None,
        "solar_morn": tor.window("shortwave_radiation", day, 8, 12, "max"),
        "cloud_morn": tor.window("cloud_cover", day, 6, 12, "mean"),
        "rh_morn": tor.window("relative_humidity_2m", day, 6, 10, "mean"),
        "precip_day": tor.window("precipitation", day, 6, 18, "sum"),
        "w100_noon": tor.window("wind_speed_100m", day, 11, 15, "mean"),
        "tmax_tor": tor.window("temperature_2m", day, 6, 18, "max"),
        "dp_ib_night": _delta_window(ib, ver, "pressure_msl", day, 1, 5),
        "dp_bz_night": _delta_window(bz, ver, "pressure_msl", day, 1, 5),
        "cloud_night": tor.window("cloud_cover", day, 0, 6, "mean"),
        "w100_night": tor.window("wind_speed_100m", day, 1, 5, "mean"),
        "solar_prev_pm": tor.window("shortwave_radiation", prev, 12, 18, "max"),
        "rh_night": tor.window("relative_humidity_2m", day, 0, 5, "mean"),
    }
    precip_eve = tor.window("precipitation", prev, 18, 23, "sum")
    precip_early = tor.window("precipitation", day, 0, 4, "sum")
    f["precip_night"] = (precip_eve or 0.0) + (precip_early or 0.0)

    wd = tor.window("wind_direction_100m", day, 11, 15, "mean")
    ws = f["w100_noon"]
    if wd is not None and ws is not None:
        f["w100_u"] = -ws * math.sin(math.radians(wd))
        f["w100_v"] = -ws * math.cos(math.radians(wd))
    else:
        f["w100_u"] = f["w100_v"] = None

    if any(v is None for v in f.values()):
        return None
    return f  # type: ignore[return-value]


async def fetch_forecast_points(client: httpx.AsyncClient | None = None) -> dict[str, PointSeries]:
    """Live forecast for all 4 points (past 1 day for the prev-day windows, +4 days)."""
    own = client is None
    client = client or httpx.AsyncClient(timeout=60)
    try:
        out = {}
        for name, (lat, lon, hourly) in POINTS.items():
            r = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={"latitude": lat, "longitude": lon, "hourly": hourly,
                        "past_days": 1, "forecast_days": 4, "timezone": "Europe/Berlin"},
            )
            r.raise_for_status()
            out[name] = PointSeries(r.json()["hourly"])
        return out
    finally:
        if own:
            await client.aclose()
