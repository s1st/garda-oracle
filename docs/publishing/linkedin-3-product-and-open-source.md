# LinkedIn draft 3: Vom Notebook zur kleinen öffentlichen Wetteranwendung

*Arbeitsfassung · Deutsch*

Ein Modell im Notebook ist noch kein Produkt.

Nach den Experimenten mit Ora und Peler wollte ich eine Anwendung, die ich am
See tatsächlich auf dem Smartphone benutzen würde: schnell, knapp und ohne
meteorologisches Vorwissen – aber mit genug Transparenz, um einer
Wahrscheinlichkeit nicht blind vertrauen zu müssen.

Daraus entstand [Garda Oracle](https://garda.simon-stieber.de/go/linkedin).

Die Startseite zeigt für heute, morgen und übermorgen jeweils zwei getrennte
Karten:

- Peler am frühen Morgen;
- Ora am Nachmittag.

Jede Karte enthält ein GO, MAYBE oder NO GO und die zugehörige
Wahrscheinlichkeit. Ein Klick öffnet die Faktoren, die den Modellwert an
diesem Tag am stärksten nach oben oder unten bewegen – zum Beispiel
Druckgefälle, Bewölkung, Sonneneinstrahlung oder Niederschlag.

Diese Beiträge sind mathematisch exakt für das lineare Modell: Sie zeigen,
welche standardisierten Eingaben den Logit am stärksten verändert haben. Sie
sind trotzdem kein Kausalitätsbeweis. Deshalb erklärt die Seite sowohl die
physikalische Bedeutung eines Faktors als auch diese Grenze.

Technisch ist das Projekt bewusst klein:

- FastAPI und Jinja2 für die Website;
- Open-Meteo für die Vorhersagefelder;
- Meteotrentino T0193 für aktuelle und historische Beobachtungen;
- ein 30-Minuten-Cache für Forecasts und fünf Minuten für Live-Wind;
- Cloud Run als stateless Service;
- Deutsch, Englisch und Italienisch ohne externes Übersetzungssystem.

Die Modelle werden offline mit scikit-learn trainiert. Im laufenden Service
gibt es aber weder scikit-learn noch pandas oder NumPy. Mittelwerte,
Standardabweichungen, Koeffizienten, Kalibrierungsparameter und Schwellenwerte
werden als Python-Daten exportiert. Die Laufzeitberechnung ist nur noch ein
Skalarprodukt plus logistische Funktion.

Der wichtigste technische Schutz gegen schleichende Fehler ist weniger
sichtbar: Training und Website verwenden denselben Feature Builder. Zeitfenster
und Druckdifferenzen werden also nicht zweimal unabhängig implementiert. Ein
Golden-Vector-Test friert zusätzlich eine bekannte Modellantwort ein.

Ich bereite das Projekt nun als Open Source vor. Dazu gehören nicht nur eine
Lizenz und ein hübsches README, sondern vor allem:

- dokumentierte Datenlizenzen und Attribution;
- keine eingecheckten Rohdaten;
- ein reproduzierbarer Fetch-, Label-, Trainings- und Exportpfad;
- eine Modellkarte mit Grenzen und negativen Ergebnissen;
- automatisierte Tests, Linting, Typprüfung und Paket-Build;
- klare Hinweise, dass dies keine amtliche Wetter- oder
  Sicherheitsvorhersage ist.

Der Code basiert ausschließlich auf offen zugänglichen beziehungsweise klar
wiederverwendbaren Datenquellen. Damit lässt sich nicht nur die Anwendung
zeigen, sondern auch der komplette Weg von öffentlichen Messungen bis zur
ausgelieferten Wahrscheinlichkeit nachvollziehen.

Was ich aus dem Projekt mitnehme:

1. Eine präzise lokale Zielfrage ist oft wertvoller als noch ein weiteres
   allgemeines Wettermodell.
2. Der Transfer von Reanalyse auf echte Forecast-Eingaben muss explizit
   getestet werden.
3. Erklärbarkeit beginnt bei einer konsistenten Datenpipeline, nicht erst bei
   einem Tooltip.
4. Datenlizenzierung ist Teil der Architektur.
5. Ein kleines Modell mit ehrlicher Validierung kann für einen konkreten
   Anwendungsfall erstaunlich nützlich sein.

Live: <https://garda.simon-stieber.de/go/linkedin>

Repository: **Link nach öffentlicher Freigabe ergänzen**

---

## Suggested media

- Hauptbild: Mobile Screenshot der Vorhersagekarten
- Zweites Bild: geöffneter Faktor-Dialog
- Drittes Bild: Architekturdiagramm oder Ausschnitt aus der Modellkarte

## Possible closing question

> Welche kleinen, lokalen Entscheidungen würdet ihr gern aus allgemeinen
> Wetterdaten ableiten – wenn eine gute Messreihe als Ground Truth verfügbar
> wäre?
