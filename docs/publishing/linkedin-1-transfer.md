# LinkedIn draft 1: Lässt sich ein lokales Windmodell auf einen anderen See übertragen?

*Arbeitsfassung · Deutsch*

Vor einiger Zeit habe ich für den Walchensee ein kleines Vorhersagesystem
gebaut. Die Ausgangsfrage war sehr praktisch: Entsteht heute die lokale
Thermik – oder fährt man umsonst an den See?

Globale Wettermodelle liefern dafür viele Zutaten: Luftdruck, Bewölkung,
Sonneneinstrahlung, Wind in verschiedenen Höhen. Was sie nicht direkt liefern,
ist die lokale Antwort für einen bestimmten Spot.

Am Gardasee stellte sich mir deshalb eine neue Frage:

**Lässt sich so eine Methode auf ein anderes thermisches Windsystem
übertragen?**

Nicht das konkrete Walchensee-Modell. Die Seen funktionieren zu
unterschiedlich. Am Walchensee geht es vor allem um eine nordgerichtete
Thermik, die durch die lokale Topografie und Erwärmung entsteht. Am nördlichen
Gardasee gibt es dagegen zwei charakteristische Regime:

- den Peler am frühen Morgen aus nördlichen Richtungen;
- die Ora am Nachmittag aus südlichen Richtungen.

Übertragbar war also nicht die fertige Vorhersageformel, sondern der
Arbeitsprozess:

1. Zuerst muss präzise definiert werden, was „Wind war da“ bedeutet.
2. Danach braucht es eine möglichst lange lokale Messreihe als Ground Truth.
3. Aus großräumigen Wetterdaten werden physikalisch plausible Merkmale gebaut.
4. Das Modell wird jahresweise außerhalb seiner Trainingsdaten geprüft.
5. Schließlich muss getestet werden, ob der Effekt auch mit echten
   Vorhersagedaten funktioniert – nicht nur rückblickend mit Reanalyse.

Für Torbole gibt es dafür eine erstaunlich gute Grundlage: rund 14 Jahre
Windmessungen der Meteotrentino-Station T0193. Aus Richtung, Geschwindigkeit
und Tageszeit lassen sich getrennte Labels für Peler und Ora ableiten.

Das erste Ergebnis hat mich überrascht. Beide Windsysteme waren deutlich
besser vorhersagbar als eine reine Monatsstatistik. Die Ora erreichte in der
jahresweisen Kreuzvalidierung einen Peirce Skill Score von +0,54, der Peler
+0,39. Die jeweilige Monatsklimatologie lag nur bei etwa +0,2.

Der Gardasee war für diese Fragestellung damit nicht schwieriger als der
Walchensee, sondern statistisch sogar klarer.

Aus dem Experiment ist inzwischen ein kleines öffentliches Produkt geworden:
[Garda Oracle](https://garda.simon-stieber.de/go/linkedin) zeigt für drei Tage getrennte
Wahrscheinlichkeiten für Ora und Peler und erklärt, welche Wetterfaktoren die
Vorhersage am stärksten beeinflussen.

Im nächsten Beitrag geht es um den entscheidenden Test: Bleibt die Güte
erhalten, wenn das Modell nicht mit Wetterdaten aus der Rückschau, sondern mit
der tatsächlichen Vorhersage vom Vortag arbeitet?

---

## Suggested media

- Hero: Screenshot der drei Tageskarten
- Zweites Bild: kleine Skizze Walchensee → Methode → Gardasee
- Link: Live-Dashboard; Repository erst nach öffentlicher Freigabe ergänzen

## Possible short opener

> Ich wollte wissen, ob sich ein lokales Windmodell auf einen anderen Alpensee
> übertragen lässt. Die überraschende Antwort: Nicht das Modell war
> übertragbar – aber die Methode.
