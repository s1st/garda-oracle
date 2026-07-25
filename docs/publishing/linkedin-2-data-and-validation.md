# LinkedIn draft 2: Eine gute Rückschau ist noch keine Vorhersage

*Arbeitsfassung · Deutsch*

Im ersten Teil ging es um die Frage, ob sich die Methodik einer lokalen
Thermikvorhersage vom Walchensee auf den Gardasee übertragen lässt.

Die ersten Ergebnisse für Ora und Peler sahen sehr gut aus. Aber genau an
dieser Stelle kann ein Wettermodell leicht besser wirken, als es später im
Alltag ist.

Der Grund ist ein klassisches Problem: **Reanalyse ist keine Vorhersage.**

Reanalysedaten beschreiben das Wetter der Vergangenheit mit einem Modell, das
nachträglich alle verfügbaren Beobachtungen einbezieht. Sie sind hervorragend
für lange Trainingsreihen. Sie kennen das Wetter aber genauer als eine reale
Vorhersage vom Vortag.

Für Garda Oracle habe ich deshalb zwei getrennte Datenwelten verwendet:

- Meteotrentino T0193 in Torbole liefert die beobachteten Windregime.
- Open-Meteo/ERA5 liefert die lange historische Wetterreihe.
- Die Open-Meteo Previous Runs API liefert Felder aus alten Modellläufen –
  konkret: Was sagte der gestrige Lauf über den heutigen Tag?

Die Ground Truth ist bewusst einfach und reproduzierbar:

- Peler: gerichteter Wind zwischen 04:00 und 09:00 Uhr, im Mittel mindestens
  8 Knoten.
- Ora: gerichteter Wind zwischen 12:00 und 17:00 Uhr, ebenfalls mindestens
  8 Knoten.

Darauf werden zwei getrennte logistische Modelle trainiert. Die Merkmale
beschreiben unter anderem Druckunterschiede zwischen Alpen und Po-Ebene,
Sonneneinstrahlung, Bewölkung, Niederschlag, Feuchte und Wind in 100 Metern.

Zuerst habe ich jedes Jahr einmal vollständig zurückgehalten. Das verhindert,
dass einzelne Wetterlagen aus demselben Jahr gleichzeitig in Training und
Test landen. Auf rund 2.972 vollständigen Saisontagen erreichte die Ora einen
Peirce Score von +0,54, der Peler +0,39.

Dann kam der wichtigere Test: Das mit ERA5 trainierte Modell wurde auf 513
Tagen zweimal bewertet – einmal mit Reanalysefeldern und einmal mit den
tatsächlichen Vorhersagefeldern vom Vortag.

| Regime | ERA5-Rückschau | Vorhersage vom Vortag |
|---|---:|---:|
| Ora | +0,58 | **+0,59** |
| Peler | +0,38 | **+0,49** |

Der Übergang zur echten Vorhersage kostete also keine erkennbare
Trennschärfe. Beim Peler war das Ergebnis sogar besser. Eine plausible
Erklärung ist, dass die historischen Forecast-Felder regional höher
aufgelöst sind als ERA5 und die Druckverteilung um die Alpen besser erfassen.

Es gab trotzdem keinen Grund, nur die Erfolgsmeldung zu behalten:

- Viele Peler-Fehlalarme lagen mit 6,7–7,8 Knoten knapp unter der gewählten
  8-Knoten-Grenze.
- Es gibt Tage, an denen die Ora trotz scheinbar perfekter Voraussetzungen
  ausbleibt.
- Ein getestetes Nordföhn-Override klang physikalisch sinnvoll, verbesserte
  das Modell statistisch aber nicht belastbar und wurde deshalb nicht gebaut.
- Eine einzelne Station kann nicht den gesamten nördlichen Gardasee
  repräsentieren.

Genau diese negativen Ergebnisse gehören für mich zu einem seriösen
Hobbyprojekt dazu. Ein Modell wird nicht dadurch vertrauenswürdig, dass jede
plausible Idee eingebaut wird, sondern dadurch, dass auch gute Geschichten an
den Daten scheitern dürfen.

Im dritten Teil zeige ich, wie aus diesen Experimenten eine kleine öffentliche
Anwendung wurde – mit erklärbaren Prognosen, drei Sprachen und einem
Open-Source-Trainingspfad.

---

## Suggested media

- Hauptgrafik: Tabelle oder Balken „ERA5 vs. previous_day1“
- Zweites Bild: vereinfachter Datenfluss Station → Labels → Modell → Dashboard
- Optional: Beispiel eines knapp verfehlten Peler-Tages
