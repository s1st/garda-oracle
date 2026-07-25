"""Small, dependency-free translation catalog for the dashboard."""
from __future__ import annotations

from typing import Any

SUPPORTED_LANGS = ("de", "en", "it")
DEFAULT_LANG = "de"


TEXT: dict[str, dict[str, str]] = {
    "de": {
        "nav_forecast": "Vorhersage",
        "nav_history": "Verlauf",
        "nav_model": "Modell",
        "nav_explanation": "Erklärung",
        "github_repo": "Quellcode auf GitHub",
        "footer_measurements": "Messdaten aus Torbole: Station T0193 von",
        "footer_models": "Wettermodelle & Reanalyse:",
        "footer_processed": "Von Garda Oracle aufbereitet.",
        "footer_sister": "Schwesterprojekt:",
        "footer_project": "Ein Projekt von",
        "footer_source_prefix": "Quellcode auf",
        "footer_license_prefix": "veröffentlicht unter der",
        "footer_license_name": "AGPL-3.0-Lizenz",
        "footer_analytics": (
            "Anonyme Reichweitenmessung mit Cloudflare Web Analytics — "
            "ohne Cookies und ohne personenbezogene Daten."
        ),
        "day_today": "Heute",
        "day_tomorrow": "Morgen",
        "day_after": "Übermorgen",
        "index_lead": "Vorhersage für Ora und Peler in Torbole",
        "live_title": "Torbole jetzt · Meteotrentino T0193",
        "live_gusts": "Böen {value} kt",
        "live_updated": "{time} Uhr",
        "live_unavailable": "Live-Daten gerade nicht verfügbar.",
        "forecast_missing": "Für diesen Tag fehlen Vorhersagedaten.",
        "peler_card_time": "Peler · früh (ca. 4–9 Uhr)",
        "ora_card_time": "Ora · mittags (Beginn meist 10:40–12:20)",
        "past_today": " · heute bereits vorbei",
        "probability": "{value} % Wahrscheinlichkeit",
        "peler_dialog_time": "früh · ca. 4–9 Uhr",
        "ora_dialog_time": "mittags · Beginn meist 10:40–12:20",
        "dialog_intro": (
            "Diese drei Wetterfaktoren beeinflussen die heutige Vorhersage im "
            "Vergleich zu einem durchschnittlichen Saisontag am stärksten."
        ),
        "supports_ora": "Spricht für Ora",
        "opposes_ora": "Spricht gegen Ora",
        "supports_peler": "Spricht für Peler",
        "opposes_peler": "Spricht gegen Peler",
        "other_factors": "Alle weiteren Faktoren anzeigen ({count})",
        "dialog_caveat": (
            "Ob ein Faktor die Wahrscheinlichkeit erhöht oder senkt, ergibt sich "
            "aus dem statistischen Modell. Das zeigt einen statistischen Zusammenhang, "
            "belegt aber keine einzelne physikalische Ursache. In die Vorhersage "
            "fließen alle aufgeführten Faktoren ein; die drei wichtigsten sind hervorgehoben."
        ),
        "close": "Schließen",
        "model_quality_link": "Wie gut ist das Modell?",
        "how_link": "Wie funktioniert das?",
        "history_title": "Verlauf",
        "history_lead": (
            "Die letzten 30 Tage: Was das Modell am Vorabend vorhergesagt hätte — "
            "im Vergleich mit den Messungen aus Torbole."
        ),
        "history_unavailable": (
            "Die Verlaufsdaten sind gerade nicht verfügbar. Bitte später noch einmal versuchen."
        ),
        "ora_midday": "Ora (mittags)",
        "peler_early": "Peler (früh)",
        "model_previous_day": "Modell (Vortagesprognose)",
        "measured_ora": "Gemessen (≥ 8 kt aus Süd, 12–17 Uhr)",
        "measured_peler": "Gemessen (≥ 8 kt aus NO–O, 4–9 Uhr)",
        "model_label": "Modell",
        "fired": "gefeuert",
        "not_fired": "nicht gefeuert",
        "no_data": "keine Daten",
        "history_summary": (
            "Das Modell lag an {correct} von {decided} Tagen mit eindeutiger Prognose "
            "richtig ({percent} %; MAYBE-Tage zählen nicht als Entscheidung)."
        ),
        "legend_fired": "GO / gefeuert",
        "legend_maybe": "MAYBE",
        "legend_not_fired": "NO GO / nicht gefeuert",
        "legend_no_data": "keine Daten",
        "history_method": (
            "Die Modellzeile zeigt eine echte Nachvorhersage: Sie wurde ausschließlich "
            "aus den archivierten Modellläufen des jeweiligen Vortags und mit denselben "
            "Koeffizienten wie die Live-Prognose berechnet. Die Messzeile basiert direkt "
            "auf den 10-Minuten-Daten der Station Torbole (unvalidierte Telemetrie)."
        ),
        "model_title": "Modell & Treffsicherheit",
        "model_lead": (
            "Ergebnisse der Rückrechnungen — die Live-Bilanz wächst mit jeder Saison."
        ),
        "model_2026_heading": "Rückblick auf die Saison 2026 (April–Juli, 94 Tage)",
        "model_2026_note": (
            "Das Modell wurde ausschließlich mit Daten aus den Jahren 2012–2025 "
            "trainiert und anschließend Tag für Tag an den Messungen aus Torbole "
            "für 2026 geprüft."
        ),
        "ora_correct": "Ora-Prognosen richtig",
        "peler_correct": "Peler-Prognosen richtig",
        "ora_correct_note": "nur 3 Feuertage verpasst",
        "peler_correct_note": "Fehler meist knapp an der 8-kt-Grenze",
        "cv_heading": "Vorhersagegüte über 14 Jahre (jährliche Kreuzvalidierung)",
        "cv_note": (
            "Ein Peirce Skill Score von 0 bedeutet kein Unterscheidungsvermögen, "
            "1 steht für eine perfekte Unterscheidung. Für jedes Testjahr wurde "
            "das Modell ohne die Daten dieses Jahres trainiert."
        ),
        "regime": "Regime",
        "base_rate": "Basisrate",
        "model_peirce": "Modell (Peirce)",
        "climatology_only": "Nur Klimatologie",
        "base_rate_note": (
            "Zum Vergleich: Weil die Ora im Hochsommer an rund 80 % der Tage feuert, "
            "hätte auch eine pauschale „Immer GO“-Prognose eine hohe Trefferquote. "
            "Der Skill Score misst deshalb die tatsächliche Unterscheidungsleistung "
            "statt nur die Basisrate."
        ),
        "real_forecasts_heading": "Mit echten Tagesprognosen statt Rückanalysedaten",
        "real_forecasts_note": (
            "Getestet mit archivierten Vortagesprognosen aus den Jahren 2024–2026 "
            "(513 Tage): Der Wechsel von Rückanalysedaten zur echten Prognosekette "
            "kostet kaum Vorhersagegüte. Die Entscheidungsschwellen des Modells sind "
            "genau darauf kalibriert."
        ),
        "reanalysis": "Rückanalyse (ERA5)",
        "previous_day_forecast": "Vortagesprognose",
        "limits_heading": "Ehrliche Grenzen",
        "dead_ora_title": "„Perfektes Setup, See bleibt tot“",
        "dead_ora_desc": (
            "Rund 11 Tage der Saison 2026 sahen nach Lehrbuch-Ora aus und blieben "
            "windstill. An etwa einem Fünftel dieser Tage unterdrückte Nordföhn die "
            "Ora; der Rest ist offen — daran wird gearbeitet."
        ),
        "peler_boundary_title": "Peler-Stärke an der Grenze",
        "peler_boundary_desc": (
            "Viele Peler-„Fehler“ liegen bei 6,7–7,8 kt — das Regime war richtig "
            "erkannt, nur die 8-kt-Schwelle knapp verfehlt. Für die Brotzeit-Session "
            "reicht’s oft trotzdem."
        ),
        "one_station_title": "Ein Messpunkt",
        "one_station_desc": (
            "Als Referenz dient die Station Torbole (Belvedere). Was in Malcesine "
            "oder am südlichen Gardasee passiert, kann davon abweichen."
        ),
        "method_prefix": "Die Auswertung folgt denselben Grundsätzen wie beim",
        "walchensee_project": "Walchensee-Projekt",
        "method_suffix": (
            "(Peirce Skill Score statt bloßer Trefferquote, jährliche "
            "Kreuzvalidierung, kalibrierte Schwellen)."
        ),
        "explanation_title": "Erklärung",
        "explanation_lead": "Was Ora und Peler sind und wie die Vorhersage entsteht.",
        "explanation_intro_1": (
            "Der nördliche Gardasee hat zwei tägliche Windsysteme: den <strong>Peler</strong>, "
            "einen Nordwind, der nachts einsetzt und bis in den Vormittag bläst, und die "
            "<strong>Ora</strong>, den thermischen Südwind, der an guten Tagen gegen Mittag "
            "einsetzt und den Nachmittag trägt. Beide entstehen aus dem Druck- und "
            "Temperaturgefälle zwischen der Po-Ebene und den Alpen — und genau dieses "
            "Gefälle lässt sich aus Wettermodellen vorhersagen."
        ),
        "explanation_intro_2": (
            "Für jedes Regime gibt es ein eigenes statistisches Modell (logistische "
            "Regression), trainiert mit <strong>Messdaten aus 14 Jahren</strong> von der "
            "Meteotrentino-Station Torbole (2012–2026, 10-Minuten-Auflösung) und den "
            "zugehörigen Wetterlagen. Die Seite ruft aktuelle Vorhersagedaten von "
            "Open-Meteo ab und berechnet daraus die Wahrscheinlichkeit, dass das Regime "
            "mit rund 8 kt Mittelwind oder mehr feuert."
        ),
        "main_drivers": "Die wichtigsten Treiber",
        "pressure_title": "Druckgradient Alpen ↔ Po-Ebene",
        "pressure_desc": (
            "Der Kern beider Regime. Nachts treibt ein positives Bozen−Verona-Gefälle "
            "den Peler; tagsüber erzeugt die Erwärmung der Berge ein Hitzetief, das die "
            "Ora ansaugt. Ein zu starkes Druckgefälle aus Norden (> 8 hPa) kann die Ora "
            "allerdings unterdrücken."
        ),
        "sun_title": "Einstrahlung & Bewölkung am Vormittag",
        "sun_desc": (
            "Ohne Sonne keine Thermik: Vormittagssonne über dem Sarcatal und der Po-Ebene "
            "verstärkt den thermischen Antrieb der Ora, dichte Bewölkung dämpft ihn."
        ),
        "flow_title": "Höhenströmung (100 m / synoptisch)",
        "flow_desc": (
            "Eine großräumige Südkomponente verstärkt die Ora, nördliche Überströmung "
            "stützt den Peler. Der stärkste Einzeltreiber im Ora-Modell."
        ),
        "rain_title": "Niederschlag & Luftfeuchte",
        "rain_desc": (
            "Regen schwächt die Ora oder beendet sie komplett; Regen und hohe Feuchte "
            "in der Nacht schwächen den Peler-Antrieb."
        ),
        "heating_title": "Erwärmungsunterschied Verona ↔ Innsbruck",
        "heating_desc": (
            "Je stärker sich die Po-Ebene gegenüber dem Alpenraum erwärmt, desto "
            "stärker der thermische Sog nach Norden."
        ),
        "glossary": "Glossar",
        "ora_desc": (
            "Thermischer Talwind aus Süd am Nordufer des Gardasees. Setzt an guten "
            "Tagen zwischen ca. 10:40 und 12:20 ein (Median 11:30) und trägt den "
            "Nachmittag. In der Hochsaison feuert sie an rund drei von vier Tagen."
        ),
        "peler_term": "Peler (auch Vento)",
        "peler_desc": (
            "Nächtlicher bis vormittäglicher Nordwind. In Torbole misst ihn die Station "
            "aufgrund der Ablenkung durch den Monte Brione als Wind aus Nordost bis Ost. "
            "Gute Peler-Morgen gibt es an etwa der Hälfte der Saisontage."
        ),
        "verdicts_desc": (
            "Die Wahrscheinlichkeit des Modells, übersetzt in eine Empfehlung. Die "
            "Schwellen wurden an archivierten Vortagesprognosen aus drei Jahren "
            "kalibriert. MAYBE heißt: Grenzfall — Live-Daten am Morgen anschauen."
        ),
        "drivers_term": "Treiber (+/−)",
        "drivers_desc": (
            "Die drei zuerst angezeigten Faktoren verändern die heutige Wahrscheinlichkeit "
            "am stärksten nach oben (+, grün) oder unten (−, rot). Ihre Rangfolge ergibt "
            "sich aus den Modellbeiträgen und wurde nicht redaktionell ausgewählt."
        ),
        "onset_term": "Beginn der Ora",
        "onset_desc": (
            "Zeitpunkt, ab dem der Südwind mindestens 8 kt Mittelwind erreicht. Aus "
            "14 Jahren Messdaten: Median 11:30 Uhr, die Hälfte aller Tage zwischen "
            "10:40 und 12:20."
        ),
        "quality_link": "Mehr zur Modellgüte und Treffsicherheit",
    },
    "en": {
        "nav_forecast": "Forecast",
        "nav_history": "History",
        "nav_model": "Model",
        "nav_explanation": "How it works",
        "github_repo": "Source code on GitHub",
        "footer_measurements": "Torbole observations: T0193 station operated by",
        "footer_models": "Weather models & reanalysis:",
        "footer_processed": "Processed by Garda Oracle.",
        "footer_sister": "Sister project:",
        "footer_project": "A project by",
        "footer_source_prefix": "Source code published on",
        "footer_license_prefix": "under the",
        "footer_license_name": "AGPL 3.0 license",
        "footer_analytics": (
            "Anonymous audience measurement with Cloudflare Web Analytics — "
            "no cookies and no personal data."
        ),
        "day_today": "Today",
        "day_tomorrow": "Tomorrow",
        "day_after": "Day after tomorrow",
        "index_lead": "Ora and Peler forecast for Torbole",
        "live_title": "Torbole now · Meteotrentino T0193",
        "live_gusts": "Gusts {value} kt",
        "live_updated": "Updated {time} local time",
        "live_unavailable": "Live observations are currently unavailable.",
        "forecast_missing": "Forecast data is missing for this day.",
        "peler_card_time": "Peler · early (approx. 04:00–09:00)",
        "ora_card_time": "Ora · midday (usually starts 10:40–12:20)",
        "past_today": " · already over for today",
        "probability": "{value}% probability",
        "peler_dialog_time": "early · approx. 04:00–09:00",
        "ora_dialog_time": "midday · usually starts 10:40–12:20",
        "dialog_intro": (
            "These three weather factors have the strongest influence on today’s "
            "forecast compared with an average day in the season."
        ),
        "supports_ora": "Supports Ora",
        "opposes_ora": "Works against Ora",
        "supports_peler": "Supports Peler",
        "opposes_peler": "Works against Peler",
        "other_factors": "Show all other factors ({count})",
        "dialog_caveat": (
            "Whether a factor raises or lowers the probability comes from the statistical "
            "model. This shows a statistical relationship, not proof of a single physical "
            "cause. All listed factors feed into the forecast; the three strongest are highlighted."
        ),
        "close": "Close",
        "model_quality_link": "How good is the model?",
        "how_link": "How does it work?",
        "history_title": "History",
        "history_lead": (
            "The past 30 days: what the model would have forecast the evening before, "
            "compared with the Torbole observations."
        ),
        "history_unavailable": (
            "History data is currently unavailable. Please try again later."
        ),
        "ora_midday": "Ora (midday)",
        "peler_early": "Peler (early)",
        "model_previous_day": "Model (previous-day forecast)",
        "measured_ora": "Observed (≥ 8 kt from the south, 12:00–17:00)",
        "measured_peler": "Observed (≥ 8 kt from NE–E, 04:00–09:00)",
        "model_label": "Model",
        "fired": "fired",
        "not_fired": "did not fire",
        "no_data": "no data",
        "history_summary": (
            "The model was correct on {correct} of {decided} days with a definite "
            "forecast ({percent}%; MAYBE days are not counted as decisions)."
        ),
        "legend_fired": "GO / fired",
        "legend_maybe": "MAYBE",
        "legend_not_fired": "NO GO / did not fire",
        "legend_no_data": "no data",
        "history_method": (
            "The model row is a genuine hindcast: it was calculated exclusively from "
            "the archived model run issued the previous day, using the same coefficients "
            "as the live forecast. The observed row comes directly from the Torbole "
            "station’s 10-minute data (unvalidated telemetry)."
        ),
        "model_title": "Model & performance",
        "model_lead": (
            "Results from retrospective tests — the live record grows with every season."
        ),
        "model_2026_heading": "Retrospective test of the 2026 season (April–July, 94 days)",
        "model_2026_note": (
            "The model was trained exclusively on data from 2012–2025 and then tested "
            "day by day against the 2026 Torbole observations."
        ),
        "ora_correct": "Ora forecasts correct",
        "peler_correct": "Peler forecasts correct",
        "ora_correct_note": "only 3 firing days missed",
        "peler_correct_note": "most errors were close to the 8 kt threshold",
        "cv_heading": "Performance across 14 years (leave-one-year-out validation)",
        "cv_note": (
            "A Peirce Skill Score of 0 means no discrimination; 1 is perfect "
            "discrimination. For each test year, the model was trained without "
            "that year’s data."
        ),
        "regime": "Regime",
        "base_rate": "Base rate",
        "model_peirce": "Model (Peirce)",
        "climatology_only": "Climatology only",
        "base_rate_note": (
            "For context, Ora fires on roughly 80% of midsummer days, so a blanket "
            "“always GO” forecast would also achieve high accuracy. The skill score "
            "therefore measures actual discrimination rather than just the base rate."
        ),
        "real_forecasts_heading": "Real day-ahead forecasts rather than reanalysis data",
        "real_forecasts_note": (
            "Tested on archived previous-day forecasts from 2024–2026 (513 days): "
            "switching from reanalysis data to the real forecast chain costs almost "
            "no forecast skill. The model’s decision thresholds are calibrated on "
            "exactly this data."
        ),
        "reanalysis": "Reanalysis (ERA5)",
        "previous_day_forecast": "Previous-day forecast",
        "limits_heading": "Honest limitations",
        "dead_ora_title": "“Perfect setup, dead lake”",
        "dead_ora_desc": (
            "Around 11 days in the 2026 season looked like textbook Ora days but "
            "remained calm. North foehn suppressed Ora on roughly one fifth of them; "
            "the rest remain unexplained and are being investigated."
        ),
        "peler_boundary_title": "Borderline Peler strength",
        "peler_boundary_desc": (
            "Many Peler “errors” fall between 6.7 and 7.8 kt: the regime was identified "
            "correctly, but narrowly missed the 8 kt threshold. That is often still "
            "enough for a short session."
        ),
        "one_station_title": "One observation point",
        "one_station_desc": (
            "The Torbole (Belvedere) station is the reference. Conditions in Malcesine "
            "or at the southern end of the lake may differ."
        ),
        "method_prefix": "The evaluation follows the same principles as the",
        "walchensee_project": "Walchensee project",
        "method_suffix": (
            "(Peirce Skill Score rather than raw accuracy, yearly cross-validation, "
            "and calibrated thresholds)."
        ),
        "explanation_title": "How it works",
        "explanation_lead": "What Ora and Peler are and how the forecast is produced.",
        "explanation_intro_1": (
            "The northern end of Lake Garda has two daily wind systems: the "
            "<strong>Peler</strong>, a northerly that starts overnight and continues "
            "into the morning, and the <strong>Ora</strong>, a thermal southerly that "
            "usually starts around midday and carries the afternoon. Both arise from "
            "pressure and temperature differences between the Po Valley and the Alps — "
            "and weather models can forecast those differences."
        ),
        "explanation_intro_2": (
            "Each regime has its own statistical model (logistic regression), trained "
            "on <strong>14 years of observations</strong> from Meteotrentino’s Torbole "
            "station (2012–2026, 10-minute resolution) and the corresponding weather "
            "patterns. The site retrieves current Open-Meteo forecast data and calculates "
            "the probability that the regime will fire with a mean wind of roughly "
            "8 kt or more."
        ),
        "main_drivers": "The main drivers",
        "pressure_title": "Pressure gradient: Alps ↔ Po Valley",
        "pressure_desc": (
            "The core driver of both regimes. At night, a positive Bolzano−Verona "
            "gradient drives Peler; during the day, mountain heating creates a thermal "
            "low that draws in Ora. An excessively strong northerly gradient (> 8 hPa) "
            "can suppress Ora."
        ),
        "sun_title": "Morning sunshine & cloud",
        "sun_desc": (
            "No sun, no thermal: morning sunshine over the Sarca Valley and Po Valley "
            "strengthens Ora’s thermal drive, while dense cloud weakens it."
        ),
        "flow_title": "Flow aloft (100 m / synoptic)",
        "flow_desc": (
            "A broad southerly component strengthens Ora, while northerly flow supports "
            "Peler. It is the strongest individual driver in the Ora model."
        ),
        "rain_title": "Precipitation & humidity",
        "rain_desc": (
            "Rain weakens Ora or shuts it down completely; rain and high humidity "
            "overnight weaken Peler’s driving mechanism."
        ),
        "heating_title": "Heating contrast: Verona ↔ Innsbruck",
        "heating_desc": (
            "The more strongly the Po Valley warms relative to the Alpine region, "
            "the stronger the thermal draw towards the north."
        ),
        "glossary": "Glossary",
        "ora_desc": (
            "A thermal valley wind from the south at the northern end of Lake Garda. "
            "On good days it starts between roughly 10:40 and 12:20 (median 11:30) "
            "and carries the afternoon. In peak season it fires on around three out "
            "of four days."
        ),
        "peler_term": "Peler (also Vento)",
        "peler_desc": (
            "A northerly wind from overnight into the morning. At Torbole, deflection "
            "around Monte Brione means the station records it as a north-easterly to "
            "easterly. A good Peler morning occurs on roughly half of all seasonal days."
        ),
        "verdicts_desc": (
            "The model probability translated into a recommendation. The thresholds "
            "were calibrated on three years of archived previous-day forecasts. MAYBE "
            "means borderline: check the live observations in the morning."
        ),
        "drivers_term": "Drivers (+/−)",
        "drivers_desc": (
            "The first three factors shown have the strongest upward (+, green) or "
            "downward (−, red) effect on today’s probability. Their ranking comes "
            "directly from the model contributions and is not editorially selected."
        ),
        "onset_term": "Ora onset",
        "onset_desc": (
            "The point when the southerly reaches a mean wind of at least 8 kt. Across "
            "14 years of observations, the median is 11:30 and half of all days fall "
            "between 10:40 and 12:20."
        ),
        "quality_link": "More about model skill and performance",
    },
    "it": {
        "nav_forecast": "Previsione",
        "nav_history": "Andamento",
        "nav_model": "Modello",
        "nav_explanation": "Come funziona",
        "github_repo": "Codice sorgente su GitHub",
        "footer_measurements": "Dati misurati a Torbole: stazione T0193 di",
        "footer_models": "Modelli meteo e rianalisi:",
        "footer_processed": "Dati elaborati da Garda Oracle.",
        "footer_sister": "Progetto gemello:",
        "footer_project": "Un progetto di",
        "footer_source_prefix": "Codice sorgente pubblicato su",
        "footer_license_prefix": "con",
        "footer_license_name": "licenza AGPL 3.0",
        "footer_analytics": (
            "Misurazione anonima del traffico con Cloudflare Web Analytics — "
            "senza cookie e senza dati personali."
        ),
        "day_today": "Oggi",
        "day_tomorrow": "Domani",
        "day_after": "Dopodomani",
        "index_lead": "Previsione di Ora e Peler per Torbole",
        "live_title": "Torbole adesso · Meteotrentino T0193",
        "live_gusts": "Raffiche {value} kt",
        "live_updated": "Aggiornato alle {time}",
        "live_unavailable": "I dati in tempo reale non sono disponibili.",
        "forecast_missing": "Mancano dati previsionali per questo giorno.",
        "peler_card_time": "Peler · mattino presto (circa 04–09)",
        "ora_card_time": "Ora · mezzogiorno (inizio di solito 10:40–12:20)",
        "past_today": " · per oggi è già passato",
        "probability": "{value}% di probabilità",
        "peler_dialog_time": "mattino presto · circa 04–09",
        "ora_dialog_time": "mezzogiorno · inizio di solito 10:40–12:20",
        "dialog_intro": (
            "Questi tre fattori meteorologici hanno l’influenza maggiore sulla "
            "previsione di oggi rispetto a una giornata media della stagione."
        ),
        "supports_ora": "Favorisce l’Ora",
        "opposes_ora": "Contrasta l’Ora",
        "supports_peler": "Favorisce il Peler",
        "opposes_peler": "Contrasta il Peler",
        "other_factors": "Mostra tutti gli altri fattori ({count})",
        "dialog_caveat": (
            "L’aumento o la diminuzione della probabilità deriva dal modello statistico. "
            "Indica una relazione statistica, non dimostra una singola causa fisica. "
            "Tutti i fattori elencati contribuiscono alla previsione; i tre più forti "
            "sono evidenziati."
        ),
        "close": "Chiudi",
        "model_quality_link": "Quanto è affidabile il modello?",
        "how_link": "Come funziona?",
        "history_title": "Andamento",
        "history_lead": (
            "Gli ultimi 30 giorni: ciò che il modello avrebbe previsto la sera prima, "
            "confrontato con le misurazioni di Torbole."
        ),
        "history_unavailable": (
            "I dati storici non sono disponibili al momento. Riprova più tardi."
        ),
        "ora_midday": "Ora (mezzogiorno)",
        "peler_early": "Peler (mattino)",
        "model_previous_day": "Modello (previsione del giorno prima)",
        "measured_ora": "Misurato (≥ 8 kt da sud, 12–17)",
        "measured_peler": "Misurato (≥ 8 kt da NE–E, 04–09)",
        "model_label": "Modello",
        "fired": "si è attivata",
        "not_fired": "non si è attivata",
        "no_data": "nessun dato",
        "history_summary": (
            "Il modello è risultato corretto in {correct} dei {decided} giorni con "
            "una previsione netta ({percent}%; i giorni MAYBE non contano come decisioni)."
        ),
        "legend_fired": "GO / attivato",
        "legend_maybe": "MAYBE",
        "legend_not_fired": "NO GO / non attivato",
        "legend_no_data": "nessun dato",
        "history_method": (
            "La riga del modello mostra una vera ricostruzione previsionale: è stata "
            "calcolata esclusivamente con la corsa del modello archiviata il giorno "
            "precedente e con gli stessi coefficienti della previsione in tempo reale. "
            "La riga delle misurazioni deriva direttamente dai dati a 10 minuti della "
            "stazione di Torbole (telemetria non validata)."
        ),
        "model_title": "Modello e prestazioni",
        "model_lead": (
            "Risultati delle ricostruzioni — la verifica in tempo reale cresce a ogni stagione."
        ),
        "model_2026_heading": "Verifica retrospettiva della stagione 2026 (aprile–luglio, 94 giorni)",
        "model_2026_note": (
            "Il modello è stato addestrato esclusivamente con dati del 2012–2025 e poi "
            "verificato giorno per giorno sulle misurazioni di Torbole del 2026."
        ),
        "ora_correct": "Previsioni Ora corrette",
        "peler_correct": "Previsioni Peler corrette",
        "ora_correct_note": "solo 3 giornate di Ora mancate",
        "peler_correct_note": "la maggior parte degli errori è vicina alla soglia di 8 kt",
        "cv_heading": "Prestazioni su 14 anni (validazione annuale incrociata)",
        "cv_note": (
            "Un Peirce Skill Score pari a 0 indica nessuna capacità discriminante; "
            "1 indica una discriminazione perfetta. Per ogni anno di test, il modello "
            "è stato addestrato senza i dati di quell’anno."
        ),
        "regime": "Regime",
        "base_rate": "Frequenza di base",
        "model_peirce": "Modello (Peirce)",
        "climatology_only": "Solo climatologia",
        "base_rate_note": (
            "Per confronto, in piena estate l’Ora si attiva in circa l’80% dei giorni: "
            "anche una previsione fissa “sempre GO” avrebbe quindi un’alta percentuale "
            "di successi. Lo skill score misura la reale capacità discriminante, non "
            "soltanto la frequenza di base."
        ),
        "real_forecasts_heading": "Previsioni giornaliere reali invece dei dati di rianalisi",
        "real_forecasts_note": (
            "Testato su previsioni archiviate del giorno precedente dal 2024 al 2026 "
            "(513 giorni): il passaggio dai dati di rianalisi alla catena previsionale "
            "reale costa pochissima abilità previsionale. Le soglie decisionali del "
            "modello sono calibrate proprio su questi dati."
        ),
        "reanalysis": "Rianalisi (ERA5)",
        "previous_day_forecast": "Previsione del giorno prima",
        "limits_heading": "Limiti dichiarati",
        "dead_ora_title": "«Condizioni perfette, lago fermo»",
        "dead_ora_desc": (
            "Circa 11 giorni della stagione 2026 sembravano giornate da manuale per "
            "l’Ora, ma sono rimasti senza vento. In circa un quinto dei casi il föhn "
            "da nord ha soppresso l’Ora; gli altri casi restano da spiegare."
        ),
        "peler_boundary_title": "Intensità del Peler al limite",
        "peler_boundary_desc": (
            "Molti “errori” del Peler sono compresi tra 6,7 e 7,8 kt: il regime era "
            "stato riconosciuto correttamente, ma ha mancato di poco la soglia di 8 kt. "
            "Spesso è comunque sufficiente per una breve sessione."
        ),
        "one_station_title": "Un solo punto di misura",
        "one_station_desc": (
            "La stazione di Torbole (Belvedere) è il riferimento. Le condizioni a "
            "Malcesine o nella parte meridionale del lago possono essere diverse."
        ),
        "method_prefix": "La valutazione segue gli stessi principi del",
        "walchensee_project": "progetto Walchensee",
        "method_suffix": (
            "(Peirce Skill Score invece della sola percentuale di successi, validazione "
            "annuale incrociata e soglie calibrate)."
        ),
        "explanation_title": "Come funziona",
        "explanation_lead": "Cosa sono Ora e Peler e come nasce la previsione.",
        "explanation_intro_1": (
            "L’Alto Garda ha due sistemi di vento giornalieri: il <strong>Peler</strong>, "
            "un vento da nord che inizia durante la notte e continua fino al mattino, "
            "e l’<strong>Ora</strong>, il vento termico da sud che nelle giornate buone "
            "inizia verso mezzogiorno e accompagna il pomeriggio. Entrambi nascono dalle "
            "differenze di pressione e temperatura tra la Pianura Padana e le Alpi — "
            "differenze che i modelli meteorologici possono prevedere."
        ),
        "explanation_intro_2": (
            "Ogni regime ha un proprio modello statistico (regressione logistica), "
            "addestrato con <strong>14 anni di misurazioni</strong> della stazione "
            "Meteotrentino di Torbole (2012–2026, risoluzione di 10 minuti) e con le "
            "relative situazioni meteorologiche. Il sito recupera le previsioni attuali "
            "da Open-Meteo e calcola la probabilità che il regime si attivi con un vento "
            "medio di circa 8 kt o più."
        ),
        "main_drivers": "I fattori principali",
        "pressure_title": "Gradiente di pressione: Alpi ↔ Pianura Padana",
        "pressure_desc": (
            "È il motore principale di entrambi i regimi. Di notte un gradiente positivo "
            "Bolzano−Verona alimenta il Peler; di giorno il riscaldamento delle montagne "
            "crea una bassa pressione termica che richiama l’Ora. Un gradiente da nord "
            "troppo forte (> 8 hPa) può però sopprimere l’Ora."
        ),
        "sun_title": "Sole e nuvolosità del mattino",
        "sun_desc": (
            "Senza sole non c’è termica: il sole del mattino sulla valle del Sarca e "
            "sulla Pianura Padana rafforza il motore termico dell’Ora, mentre una "
            "nuvolosità compatta lo indebolisce."
        ),
        "flow_title": "Flusso in quota (100 m / sinottico)",
        "flow_desc": (
            "Una componente meridionale su larga scala rafforza l’Ora, mentre un flusso "
            "settentrionale favorisce il Peler. È il singolo fattore più importante nel "
            "modello dell’Ora."
        ),
        "rain_title": "Precipitazioni e umidità",
        "rain_desc": (
            "La pioggia indebolisce l’Ora o la interrompe del tutto; pioggia e umidità "
            "elevata durante la notte indeboliscono il meccanismo del Peler."
        ),
        "heating_title": "Differenza di riscaldamento: Verona ↔ Innsbruck",
        "heating_desc": (
            "Più la Pianura Padana si riscalda rispetto alla regione alpina, più forte "
            "diventa il richiamo termico verso nord."
        ),
        "glossary": "Glossario",
        "ora_desc": (
            "Vento termico di valle da sud nell’Alto Garda. Nelle giornate buone inizia "
            "tra le 10:40 e le 12:20 circa (mediana 11:30) e accompagna il pomeriggio. "
            "In alta stagione si attiva circa tre giorni su quattro."
        ),
        "peler_term": "Peler (anche Vento)",
        "peler_desc": (
            "Vento da nord attivo dalla notte fino al mattino. A Torbole, la deviazione "
            "causata dal Monte Brione fa sì che la stazione lo misuri da nord-est a est. "
            "Un buon Peler si verifica in circa metà dei giorni della stagione."
        ),
        "verdicts_desc": (
            "La probabilità del modello tradotta in una raccomandazione. Le soglie sono "
            "state calibrate su tre anni di previsioni archiviate del giorno precedente. "
            "MAYBE indica una situazione al limite: controlla i dati in tempo reale al mattino."
        ),
        "drivers_term": "Fattori (+/−)",
        "drivers_desc": (
            "I primi tre fattori mostrati aumentano (+, verde) o diminuiscono (−, rosso) "
            "più di tutti la probabilità odierna. L’ordine deriva direttamente dai "
            "contributi del modello e non da una scelta redazionale."
        ),
        "onset_term": "Inizio dell’Ora",
        "onset_desc": (
            "Il momento in cui il vento da sud raggiunge una media di almeno 8 kt. "
            "Su 14 anni di misurazioni, la mediana è 11:30 e metà dei giorni cade "
            "tra le 10:40 e le 12:20."
        ),
        "quality_link": "Maggiori dettagli sulle prestazioni del modello",
    },
}


def language(value: str | None) -> str:
    """Return a supported language code, defaulting to German."""
    return value if value in SUPPORTED_LANGS else DEFAULT_LANG


def translate(lang: str, key: str, **values: Any) -> str:
    """Look up and optionally format one translated string."""
    text = TEXT[language(lang)][key]
    return text.format(**values) if values else text


def format_number(lang: str, value: float, decimals: int = 0, *, signed: bool = False) -> str:
    """Format a number with the selected language's decimal separator."""
    sign = "+" if signed else ""
    text = f"{value:{sign}.{decimals}f}"
    return text.replace(".", ",") if language(lang) in ("de", "it") else text
