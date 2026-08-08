# Alpine thermal-wind lake candidate roster

Research snapshot: 26 July 2026.

## Objective

Identify Alpine or Alpine-edge lakes that satisfy both non-negotiable
requirements for an open-source thermal-wind predictor:

1. the lake is genuinely used for windsurfing, wingfoiling, kitesurfing or
   performance sailing; and
2. an openly reusable weather station provides enough historical wind speed
   and direction data to define and validate a local outcome.

This is deliberately stricter than "a wind graph exists." A source only
counts as open when automated historical access and reuse are supported by
the public provider. Private surf-club stations and commercial weather pages
do not count.

## Screening rules

### Minimum viable ground truth

- Wind speed and direction, preferably hourly or finer.
- At least five complete warm seasons; ten years is preferred.
- A station on the shore, lake, or in the actual wind corridor. A mountain,
  airport, or distant valley station may be a useful feature but is not
  automatically a valid outcome station.
- A stable identifier and documented station history.
- Public reuse terms compatible with publishing the code, derived labels,
  validation results, and model parameters.

### Ranking

- **A — immediate feasibility spike:** surf use, local wind regime, nearby
  station history, and open reuse path are all supported.
- **B — promising, one material question:** usually station exposure,
  continuity, or bulk-download details still need checking.
- **C — watchlist:** the lake is surfable, but the current station evidence is
  too weak or the historical reuse path is not yet proven.
- **Reject for now:** no credible open outcome station.

## Country-level data finding

Switzerland and Austria are unexpectedly strong foundations:

- MeteoSwiss's automatic-station collection is CC BY and exposes current and
  historical 10-minute, hourly, daily, monthly and annual data. The inventory
  gives parameter-level start dates. Wind direction is `dkl010h0` and scalar
  wind speed is `fkl010h0`.
  [Documentation](https://opendatadocs.meteoswiss.ch/en/a-data-groundbased/a1-automatic-weather-stations) ·
  [STAC collection](https://data.geo.admin.ch/api/stac/v1/collections/ch.meteoschweiz.ogd-smn)
- GeoSphere Austria exposes quality-controlled hourly and 10-minute station
  histories under CC BY 4.0 without authentication. Hourly wind parameters
  are `ff` and `dd`.
  [Resources](https://dataset.api.hub.geosphere.at/v1/docs/user-guide/resource.html) ·
  [Licence](https://dataset.api.hub.geosphere.at/v1/docs/user-guide/license.html)
- ARPA Lombardia provides free station downloads and permits independent
  analysis with attribution. Its sensor registry exposes coordinates,
  variables, and start dates.
  [Access guidance](https://www.arpalombardia.it/temi-ambientali/meteo-e-clima/guida-richiesta-dati/) ·
  [Sensor registry](https://www.dati.lombardia.it/d/nf78-nj6b)
- ARPAV provides CC BY 4.0 hourly meteorological histories from 2010,
  including wind speed and prevailing direction. Delivery currently uses an
  email request form rather than a clean public API.
  [Hourly data](https://www.arpa.veneto.it/dati-ambientali/dati-storici/meteo-idro-nivo/dispenser-meteo-orari) ·
  [CC BY climate catalogue](https://www.dati.gov.it/node/view-dataset/dataset?id=1e3bce25-7d42-4821-a74c-6ae96d39b37e)
- South Tyrol states that its station data are free for any purpose, including
  commercial use, and have been historised since the open-data launch in
  March 2016.
  [Open-data announcement](https://news.provinz.bz.it/de/news-archive/537204) ·
  [Measurement download](https://meteo.provincia.bz.it/it/download-dati)
- Météo-France publishes controlled hourly station histories from station
  opening under France's Open Licence 2.0. The API and exact parameter
  inventory still need to be tested per station.
  [Météo-France catalogue](https://www.data.gouv.fr/organizations/meteo-france/datasets?page=1&page_size=20)

## Ranked roster

Distances below are straight-line approximations from a representative
surfing basin, not distances to a municipal centroid. Start dates refer to
hourly wind where the parameter inventory was available; otherwise the row
explicitly says what remains to verify.

### Tier A — best first feasibility spikes

| Rank | Lake | Wind product | Open outcome station | History | Why it ranks here | Remaining check |
|---:|---|---|---|---|---|---|
| 1 | **Lake Silvaplana, CH** | Maloja afternoon thermal, commonly 3–6 Bft | Segl-Maria (SIA), about 3.2 km; Corvatsch is a valuable elevated feature | SIA hourly speed+direction since 2014; Corvatsch since 1981 | One of Europe's canonical thermal-wind lakes; clean Swiss data stack | Confirm that SIA exposure separates the lake session from the wider Engadin valley flow |
| 2 | **Lake Maggiore, CH/IT — northern basin** | Morning Tramontana and afternoon Inverna | Locarno/Monti (OTL), about 1 km; Magadino/Cadenazzo as a second lowland station | Hourly speed+direction since 1981 | Two named daily regimes, long open history, natural two-verdict product | Compare Locarno exposure with the actual Ascona/Magadino riding areas |
| 3 | **Achensee, AT** | Regular north–south lake/valley wind used by sailors and surfers | Achenkirch composite station, essentially on the north shore | Quality-controlled hourly speed+direction verified in 2000; composite runs 1998–present across a 2016 move | On-shore station, 28-year open series, established surf destination | Quantify the station move and choose a fixed outcome definition |
| 4 | **Lake Como, IT — upper lake** | Morning Tivano and afternoon Breva | Vercana, about 4 km; Colico, about 6.7 km | Vercana speed history from 2012 and direction from 2005; Colico current speed sensor from 2013 | Strong local wind identity, large rider population, two daily regimes | Download the full ARPA series and check sensor-replacement continuity and whether Vercana captures water-level wind |
| 5 | **Urnersee, CH** | Föhn and local lake/valley winds; serious windsurfing and sailing venue | Altdorf (ALT), about 6.1 km from the southern basin | Hourly speed+direction since 1981 | Exceptionally long, clean, open record and a well-studied local wind system | Decide whether the product predicts thermal lake wind, Föhn, or separate regimes; the latter may be more honest |
| 6 | **Walensee, CH** | Föhn-driven windsurfing with strong topographic channeling | Quinten (QUI), about 1 km from mid-lake | Hourly speed+direction since February 1993 | Probably the best station-to-lake geometry in the roster | This is more a local Föhn/channel forecast than a classic fair-weather thermal predictor |
| 7 | **Lago di Resia / Reschensee, IT** | Reliable Alpine north/south wind and established wind sports | S. Valentino alla Muta (02200MS), on the lakeshore at 1,500 m | Open data historised since March 2016; live station has speed, direction, gust, pressure, radiation and humidity | Excellent station location and a decade of explicitly free data | Prove bulk historical retrieval for all wind parameters and measure completeness before modelling |
| 8 | **Serre-Ponçon, FR** | Very regular 15–20 kt afternoon thermal, reinforced by the Durance valley | Embrun (05046001), at the head of the lake; Chadenas live station may provide a second signal | Embrun has a long anemometer history; Météo-France hourly histories are Open Licence 2.0 | Perhaps the strongest unbuilt product story after Silvaplana | Verify actual hourly wind availability and whether Embrun represents the main Crots/Savines riding basin |

Surf evidence:

- Silvaplana tourism describes a dependable afternoon thermal and Maloja wind
  of 3–6 Bft.
  [Silvaplana water sports](https://silvaplana.ch/lake-silvaplana)
- Lake Maggiore tourism names the morning Tramontana and afternoon Inverna
  and explicitly connects them to windsurfing.
  [Ascona-Locarno](https://www.ascona-locarno.com/en/what-s-on/lake-maggiore)
- Achensee has a first-class sailing and surfing reputation.
  [Austria tourism](https://www.austria.info/en-us/locations/lake-achensee/)
- Lombardy tourism names Como's morning Tivano and afternoon Breva and calls
  the upper lake the preferred sailing-sport area.
  [In Lombardia](https://www.in-lombardia.it/it/visitare-la-lombardia/vacanza-al-lago/lago-di-como-manzoni-ma-non-solo)
- Switzerland Tourism describes Walensee as a windsurfing venue in Föhn.
  [Walensee](https://www.myswitzerland.com/en-us/destinations/walensee/)
- Serre-Ponçon tourism describes its 15–20 kt thermal and windsurfing,
  wingfoiling, kitesurfing and sailing use.
  [Thermal breeze](https://www.serreponcon.com/en/lac-de-serre-poncon/activites-nautiques/kitesurf-wingfoil-brise-thermique/)

### Tier B — promising, but validate one important assumption

| Lake | Open station evidence | Surf/wind evidence | Main uncertainty |
|---|---|---|---|
| **Traunsee, AT** | Altmünster about 4.5 km, 2014–present; Gmunden composite has verified hourly wind in 2000 and runs to 2016; Feuerkogel gives a long elevated series | Tourism calls it one of the Alps' best sailing areas and attributes windsurfing/kitesurfing to its special thermals | The best long series changes site; determine whether a stitched Gmunden–Altmünster label is defensible |
| **Lago di Santa Croce, IT** | ARPAV hourly histories include wind from 2010 under CC BY 4.0; S. Martino d'Alpago appears in the regional network | Well-established windsurf/kite lake with a thermal accelerated through the Fadalto constriction | Confirm that a specific ARPAV station near the lake has both hourly speed and direction for most of 2010–present |
| **Lake Geneva / Léman, east basin, CH** | Bouveret (BOU), about 0.9 km, hourly speed+direction since September 1993 | Large established sailing/windsurfing lake | Product may be dominated by Bise, Föhn and synoptic regimes rather than one clean thermal |
| **Lake Brienz, CH** | Brienz (BRZ), about 7.8 km, speed+direction since March 1993; Interlaken since 1981 | Surfable Alpine lake | Establish a repeatable, rider-relevant local wind regime and show BRZ exposure matches it |
| **Lake Thun, CH** | Interlaken and Thun bracket the lake; Interlaken speed+direction since 1981 | Windsurfing is explicitly offered at Merligen | No station is directly in the central water corridor; outcome definition may be noisy |
| **Wolfgangsee, AT** | St. Wolfgang about 3.1 km; station composite begins in 1964 and current TAWES site in 1990 | Official tourism supports windsurfing | Tourism itself says the lake is not known for consistent strong wind; may be a poor prediction product despite excellent data |
| **Mondsee, AT** | Mondsee about 3.6 km; composite begins in 1964 and current site in 2009 | Salzkammergut identifies local and thermal winds and wing use | Confirm actual wind-parameter start and whether sessions occur often enough for useful classification |
| **Millstätter See, AT** | Millstatt about 2.4 km; composite station from 1982 | Surfing/sailing occur | Need credible evidence of a recurring predictable wind regime, not merely occasional surfability |
| **Lake Iseo, IT** | Tavernola/Gallinarga about 2.7 km since November 2018; Sarnico since June 2016 | Vello is described as having constant wind and is used for windsurfing and kitesurfing | Shorter series and station may sit outside the strongest Vello corridor |
| **Lake Idro, IT** | Nearest complete ARPA wind station found is Bagolino, about 9.5 km, from 2012 | Tourism describes regular wind and established windsurf/kitesurf schools | No confirmed shore-level outcome station; Bagolino may be a predictor rather than a label |
| **Lake Maggiore, IT — western/central basin** | Laveno-Mombello shore stations have speed+direction since 1999 | Major sailing/windsurfing lake | Decide whether to treat this as the same Inverna product as the Swiss north basin or a separate spatial regime |
| **Attersee, AT** | Unterach is about 10.9 km and only from 2019; longer stations are 14–15 km away | Official tourism calls its winds mostly thermal and promotes wingfoiling | Outcome station geometry and history are notably weaker than Achensee or Mondsee |
| **Ossiacher See, AT** | Kanzelhöhe about 5.3 km is elevated; Villach about 9.3 km has a long series | Reliable afternoon breeze supports sailing/windsurfing | No confirmed shore-level long-series station |
| **Lake Annecy, FR** | Météo-France offers open hourly station histories; exact local station inventory not yet audited | Official tourism lists windsurfing, kitesurfing and wingfoil | Surfable does not yet establish a strong, recurring forecast target |
| **Lac de Monteynard, FR** | French open-data framework is suitable; nearest station still needs identification | Tourism calls it a famous windsurf/kite spot because of regular thermal wind | Station audit is the missing piece |

Traunsee evidence:
[tourism description](https://traunsee-almtal.salzkammergut.at/fileadmin/user_upload/traunsee-almtal/Bilder/Kataloge_557_800/Prospekte/WEB_GGV_2021-22_D-E_GESAMT-KLEIN.pdf).

Lake Iseo evidence:
[Vello wind](https://visitlakeiseo.info/en/places/marone/).

Lake Idro evidence:
[Visit Brescia](https://www.visitbrescia.it/en/activity/water-sports-on-the-lakes-in-the-brescia-province/).

Monteynard evidence:
[Trièves tourism](https://www.trieves-vercors.fr/en/activities/277604_lake-monteynard-nautical-base/).

### Tier C — useful watchlist

| Lake | Why it remains on the list | Why it is not ready |
|---|---|---|
| **Lake Bohinj, SI** | Official tourism permits surfing and describes alternating fair-weather valley winds | ARSO has automatic wind stations, but an open, long, nearby hourly history and explicit reuse terms were not proven in this pass |
| **Weissensee, AT** | GeoSphere station about 2.8 km, composite from 1992 | Need to prove both consistent surf use and that local rules/protected areas permit a meaningful rider product |
| **Plansee, AT** | Reutte station about 7.3 km with a long open series | Surf community and recurring wind regime are not established strongly enough |
| **Faaker See, AT** | Surfable and close to the Austrian open network | Nearest long station is Villach rather than the lake corridor |
| **Wörthersee, AT** | Pörtschach station about 2.3 km, composite from 1996 | More a general sailing lake; thermal-wind prediction value is unclear |
| **Fuschlsee, AT** | Included in Salzkammergut wingfoiling material | Nearest open station is about 8 km away and the lake is small |
| **Lago di Lugano, CH/IT** | Lugano station about 0.9 km with hourly wind since 1981 | Establish whether there is a sufficiently strong, regular surf regime and accessible launch community |

## Recommended order

### 1. Silvaplana

Best clean-room successor to Garda. The Maloja wind is iconic, the user
question is simple, and Swiss open data now removes the historical obstacle.
The first spike should compare Segl-Maria observations with pressure and
temperature contrasts along Maloja–Engadin plus cloud/radiation fields.

### 2. Lake Maggiore north

The closest product analogue to Garda: two named daily wind regimes, long
station history, and a large lake community. It also offers a useful
cross-border test while keeping the core data source Swiss and open.

### 3. Achensee

Probably the lowest-risk data exercise. Achenkirch has a continuous composite
hourly record from 1998 with verified wind values, and GeoSphere's access and
licence are exemplary.

### 4. Lake Como

Highest likely audience after Garda, with obvious Breva/Tivano product
language. It ranks below the first three only because the ARPA sensor history
needs a careful continuity and siting audit.

### 5. Reschensee or Serre-Ponçon

Both extend the platform into a distinct climate:

- Reschensee tests a high Alpine pass/lake system with a station on the shore.
- Serre-Ponçon tests a sunny southern-Alpine reservoir with a very dependable
  afternoon thermal and France's newly open meteorological archive.

## Immediate validation tasks

Before writing any model code:

1. Download one complete summer and one complete historical year for the
   leading station.
2. Plot diurnal wind roses by month and calculate data completeness.
3. Check station relocations and sensor changes.
4. Define a rider outcome using both speed and direction, then inspect at
   least 30 randomly selected positive and negative days.
5. Confirm the exact attribution text and archive the licence evidence.
6. Only proceed if the station distinguishes the surfable local regime from
   unrelated synoptic wind.

The decisive next experiment is therefore not another model. It is a
standardised **station fitness report** run on Silvaplana, Maggiore, Achensee,
Como, Reschensee, and Serre-Ponçon.

## Important exclusions

- Surf-club graphs, hotel stations, and private webcam/anemometer feeds are
  discovery aids only.
- Open-Meteo/ERA5 can supply predictors but does not replace observed
  ground truth at the lake.
- A long mountain-station series does not count as an outcome station merely
  because it is geographically close.
- "Available on request" is acceptable only when reuse terms are clear and
  the process is repeatable; it is inferior to a stable download API.

