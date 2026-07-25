# Open wind stations around northern Lake Garda — 2026-07-24

Research note only; nothing here is integrated yet. The acceptance criterion is
not merely “visible on a website”, but an explicit licence that permits
automated retrieval and reuse.

## Licence interpretation

- **CC0** permits reuse, modification and redistribution without a legal
  attribution requirement. Limone/ARPA Lombardia falls into this category,
  although voluntary source acknowledgement is still good practice.
- **CC BY** permits the same uses, including commercial use, but requires
  attribution, a link to the licence and an indication of modifications.
  Torbole/Meteotrentino therefore needs a visible data-source credit in Garda
  Oracle.

## Current conclusion

- **Torbole T0193 remains the primary ground truth.** Meteotrentino/PAT data
  are CC BY and the station has a long 10-minute archive.
- **Limone (ARPA Lombardia station 1324)** is the strongest additional open
  lakeshore source: 10-minute wind, gust, direction, temperature, humidity and
  rain; active since 2012; station and measurement datasets are CC0.
- **Limone must not become a Torbole label source without validation.** The
  existing 2026 comparison shows much weaker Ora and barely any Peler relative
  to Torbole, but the cause is unresolved. A local wind shadow is one
  hypothesis; station siting, local flow geometry and genuine cross-lake
  differences are alternatives. Use it initially as an independent observation
  of west-shore conditions, direction and gustiness.
- **No currently active, explicitly open-licensed lakeshore station was found
  in Brenzone, Malcesine, Navene, Reamol or Pregasina.**
- A systematic road-weather sweep covered all three northern shores and their
  approach roads: PAT and A22 around Riva–Torbole–Mori–Rovereto, ANAS along
  SS45bis from Limone through Reamol/Tremosine, and Veneto Strade along SR249
  from Malcesine/Navene through Brenzone. **Road-weather infrastructure exists,
  but no current, explicitly reusable raw measurement feed suitable for Garda
  wind was found.**
- This is a public-access and licensing conclusion, not a claim that no roadside
  sensors exist. The operators may have additional stations for internal use.

## Candidate matrix

| Location / source | What exists | Licence status | Assessment |
|---|---|---|---|
| Torbole T0193, Meteotrentino | 10-minute wind and direction, archive from 2012 | CC BY (PAT) | Primary label source |
| Limone 1324, ARPA Lombardia | 10-minute mean/max wind, direction and other meteo variables | CC0 | Best second open lakeshore source; representativeness still unverified |
| Tignale Oldesio, ARPA Lombardia | Active wind station at 374 m | CC0 | Secondary regional/background signal |
| Gargnano, ARPA Lombardia | Active wind station at 984 m | CC0 | Mountain/background signal, not spot truth |
| Tremalzo T0354, Meteotrentino | Full meteo including wind at 1,560 m | CC BY (PAT) | Synoptic/mountain context only |
| Malcesine/Navene, Fraglia Vela | Live Davis station and archive UI from 2016 | No explicit data-reuse licence found | Technically useful; obtain written permission before use |
| Castelletto di Brenzone | Windfinder reports observations from Apr 2016–May 2017 | Commercial page; station no longer reporting | Not a current source |
| Historic Brenzone/Malcesine Meteogarda stations | Private Davis stations documented from about 2003 | No current accessible feed or reuse grant found | Historical lead only |
| Riva del Garda–Varone, MeteoNetwork TRN033 | Active MeteoNetwork station | CC BY 4.0 | Open, but inland/semi-urban and not a direct spot station |
| Veneto Strade SMIT | Road/air temperature, traffic and sometimes extra weather sensors | No open raw measurement feed located | Cannot currently use |
| ARPAV Veneto network | Official automatic regional network and API | Open-data access, but no Brenzone/Malcesine lakeshore station | Nearest stations are across/behind Monte Baldo and not spot truth |
| PAT CLEAN-ROADS | Six fixed RWIS stations plus thermal mapping | Historical public display is gone; no current licensed raw feed located | None of the six stations was on the Garda shore |
| PAT VERKKO / SSRS | New weather-station network and DATEX II connection to Italy's NAP | Project in progress, planned through 2028 | Promising future route, not a current feed |
| A22 winter-service network | Road-weather stations, pavement sensors and thermal mapping | Operational data not publicly exposed under a reuse licence | Nearest corridor is Rovereto/A22, not the lake |
| ANAS SS45bis / VAI | ANAS has smart-road weather capability and public traffic/weather-warning services | No public station inventory, raw measurements or reuse grant found for SS45bis | No usable west-shore road-weather source identified |

## Brenzone

The search covered Brenzone, Assenza, Castelletto and Acquafresca.

- The current ARPAV station catalogue contains no Brenzone or Malcesine
  lakeshore station. The numerically closest Veneto stations include Dolcè and
  Bardolino–Calmasino, but Dolcè is on the far side of Monte Baldo and
  Calmasino is well south of the target area. Neither represents local Ora/Peler
  at Brenzone.
- Windfinder says a Castelletto station formerly supplied observations between
  2016-04-01 and 2017-05-31, but it is no longer available/reporting.
- An older study documents private Meteogarda Davis stations at Brenzone and
  Malcesine, with Brenzone operating from about 2003. No current public feed or
  explicit reuse licence was found.
- Forecast pages and webcams were excluded: they are model output or imagery,
  not reusable measured wind.

This is a real coverage gap, not evidence that no private sensor exists. A
local club or school may have one behind a dashboard. Written permission would
be required unless the provider publishes a suitable reuse licence.

## Future work: Limone representativeness

Treat “Limone is in a wind shadow” as an untested hypothesis. Before deciding
how to use the station:

1. compare simultaneous Limone and Torbole observations by wind regime,
   direction, hour and synoptic setup over multiple seasons;
2. inspect the exact sensor position, mast height and nearby obstructions;
3. compare Limone with another west-shore or over-water station if one becomes
   available;
4. only then decide whether the difference is systematic shelter, a local
   circulation, instrumentation, or the expected spatial structure of
   Ora/Peler.

## Road-weather systems: Germany versus northern Garda

The recent Walchensee implementation uses the DWD public SWIS BUFR feed:

`https://opendata.dwd.de/weather/weather_reports/road_weather_stations/FN/`

`../walchensee-oracle/scripts/log_local_stations.py` downloads the rolling
live window, decodes stations within 20 km, and stores one deduplicated JSONL
file per station. It runs every 12 hours because DWD exposes only roughly 48
hours publicly; the complete SWIS history is in the restricted SWISinfo
system. DWD's public data are reusable under CC BY 4.0.

The deployed logger was checked on 2026-07-24:

- latest Cloud Run execution completed successfully at
  2026-07-23 22:00:59 UTC;
- it added 235 samples across P798 Kesselberg, P799 Sylvenstein, P800
  Spatzenhausen, P940 Jachenau, P980 Westried and Z926 Herzogstand;
- the latest Kesselberg sample was 2026-07-23 21:45 UTC (23:45 CEST):
  0.3 m/s from 200°, gust 0.8 m/s, 13.8 °C.

### Search perimeter

The Garda search was not limited to Brenzone. It covered:

- **Trentino:** Riva, Torbole, Arco, Nago, Mori/Loppio, Rovereto and the A22
  Lago di Garda Nord corridor;
- **Lombardy:** Limone, Reamol, Tremosine and SS45bis/Gardesana Occidentale;
- **Veneto:** Malcesine, Navene, Brenzone and SR249/Gardesana Orientale;
- **cross-region:** A22, ANAS VAI, CCISS/the Italian National Access Point and
  DATEX II publication routes.

The test was deliberately strict: an operational sensor alone is insufficient.
For integration we need a documented measurement feed and an explicit reuse
licence.

### Trentino provincial roads

The former **CLEAN-ROADS** project had six fixed RWIS stations and mobile road
thermal mapping. The published fixed locations were Cadino, Lavis, San
Michele, Rocchetta, Acquaviva/SS12 and the SP235 viaduct above the A22 at
Trento Nord. None was at Lake Garda or on the Mori–Nago–Torbole approach. Its
former public map is no longer reachable, and no current licensed raw feed was
located.

The current Viaggiare in Trentino web application was also inspected. Its
weather layer returns a regular grid of road-hazard **forecasts**, not
observations from identifiable stations, and no data-reuse licence was found
for that application feed.

The official open Meteotrentino inventory adds useful context but no missed
road-wind source:

- Mori/Loppio T0151 is close to the access road but measures temperature and
  precipitation, not wind;
- Arco T0401, Tenno T0200 and Brentonico T0443 also lack wind;
- Rovereto T0147 and Dro/Marocche T0379 do measure wind, but are ordinary
  meteorological stations in different terrain, not lakeshore RWIS stations.

PAT's new **VERKKO** project is the most promising future route. It runs from
2025 to 2028 and explicitly includes both a weather-station network for road
maintenance (SSRS) and a DATEX II interface connecting Trentino road sensors
to Italy's National Access Point. It is still in progress and therefore not a
current data source.

### A22 / Rovereto approach

Autostrada del Brennero confirms that it operates weather stations, pavement
sensors and thermal-mapping vehicles for winter maintenance. Its public site,
however, displays third-party 3BMeteo **forecasts** for broad motorway areas
such as “Rovereto–Riva del Garda”; these are not live measurements from the
operator's road stations. No public station inventory, raw observation API or
explicit reuse licence was found.

Even if access were granted, an A22 station near Rovereto would describe the
Adige valley and motorway corridor. It might be useful as a synoptic/context
feature, but not as ground truth for wind on the lake.

### Lombardy west shore: SS45bis

ANAS manages the relevant SS45bis/Gardesana Occidentale corridor. ANAS
documents weather and environmental sensors in its wider smart-road systems,
and its VAI services expose traffic conditions, cameras and weather warnings.
The public weather page distributes Civil Protection warnings rather than raw
station measurements.

No public ANAS station inventory or licensed measurement feed was found for
Limone, Reamol or Tremosine. This does not exclude internal tunnel, road or
maintenance sensors; it means there is presently nothing we can integrate.
The open ARPA Lombardia Limone 1324 station therefore remains the only
identified legally reusable lakeshore wind source on this shore, and it is a
meteorological rather than road-safety station.

### Veneto east shore: SR249

Veneto Strade does operate **SMIT** roadside monitoring stations. Its own
material describes cameras plus sensor units measuring traffic, road
temperature and air temperature; the modular system may add atmospheric
pressure and other winter-safety sensors. The current public Veneto Strade
weather page redirects users to ARPAV rather than exposing SMIT measurements.

- the Veneto Strade public site exposes road information and webcams, not an
  identified open raw station feed;
- no station on SR249 around Brenzone/Malcesine was found with public wind
  readings and a reuse licence.

### National Access Point and practical conclusion

DATEX II can represent measurement sites and measured weather values, but that
technical capability is not evidence that a particular operator publishes
those values. The public CCISS material located during this search covers
traffic locations/events and warnings; it did not reveal an open Garda
weather-station stream or applicable reuse terms.

Therefore the SWIS forward logger cannot simply be ported to Garda. The only
current open lakeshore wind measurements identified remain Meteotrentino
T0193 at Torbole and ARPA Lombardia 1324 at Limone, neither of which is a road
station.

If we pursue road data, send the same precise access request to PAT, A22, ANAS
and Veneto Strade:

1. station inventory and coordinates for the northern Garda perimeter;
2. available variables, especially mean wind, gust and direction;
3. sampling interval and historical retention;
4. API or bulk-download method;
5. licence/reuse terms.

PAT/VERKKO is worth rechecking as the project approaches its scheduled end in
2028.

## Source links

- ARPA Lombardia station inventory:
  <https://www.dati.lombardia.it/Ambiente/Stazioni-Idro-Nivo-Meteorologiche/nf78-nj6b>
- ARPA Lombardia current sensor data:
  <https://www.dati.lombardia.it/Ambiente/Dati-sensori-meteo/647i-nhxk>
- Meteotrentino open dataset:
  <https://dati.trentino.it/dataset/meteo-data>
- Meteotrentino open-data licence statement:
  <https://www.meteotrentino.it/contatti-e-informazioni/servizi-per-il-pubblico/opendata/>
- CLEAN-ROADS six-station inventory:
  <https://clean-roads.eu/secondo-sondaggio.html>
- PAT VERKKO project:
  <https://www.provincia.tn.it/en/Administration/Projects/VERKKO>
- Viaggiare in Trentino:
  <https://www.viaggiareintrentino.it/>
- A22 winter-service monitoring:
  <https://www.autobrennero.it/it/sicurezza/servizio-invernale/>
- ANAS smart-road systems:
  <https://www.stradeanas.it/it/smart-road-smart-mobility>
- ANAS VAI services:
  <https://www.stradeanas.it/it/le-app>
- Fraglia Vela Malcesine/Navene station:
  <https://stazioni.meteoproject.it/dati/malcesine/>
- ARPAV station API documentation:
  <https://clima.arpa.veneto.it/api/v2/docs>
- ARPAV regional telemetry network:
  <https://www.arpa.veneto.it/temi-ambientali/meteo/monitoraggio/rete-di-telemisura-1>
- Windfinder Castelletto history:
  <https://it.windfinder.com/windstatistics/lake_garda_castelletto_di_brenzone>
- MeteoNetwork Riva–Varone station:
  <https://www.meteonetwork.eu/it/weather-station/trn033-stazione-meteorologica-di-riva-del-garda-varone/details>
- Veneto Strade:
  <https://www.venetostrade.it/>
- Veneto Strade SMIT description (2019 management report, pp. 14–15):
  <https://www.venetostrade.it/myportal/VSSPA/api/content/download?id=627a35952fc6e0008ec7118e>
- CCISS RDS-TMC database:
  <https://www.cciss.it/web/cciss/database-rds-tmc>
- DATEX II measured-data documentation:
  <https://docs.datex2.eu/v3.4/roadtrafficdata/>
