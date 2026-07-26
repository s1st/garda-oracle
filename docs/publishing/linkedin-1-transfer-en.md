# LinkedIn draft 1: Can a local wind model be transferred to another lake?

*Working draft · English*

Some time ago, I built a small forecasting system for the Walchensee. The
question behind it was very practical: Will the local thermal wind develop
today, or will the trip to the lake be for nothing?

Global weather models provide many of the ingredients: air pressure, cloud
cover, solar radiation, and wind at different altitudes. What they do not
provide directly is the local answer for one specific spot.

At Lake Garda, this led me to a new question:

**Can this kind of method be transferred to a different thermal wind system?**

Not the actual Walchensee model. The two lakes work too differently. At the
Walchensee, the main phenomenon is a northward thermal wind driven by local
topography and heating. At the northern end of Lake Garda, there are two
characteristic regimes:

- the Peler from northerly directions in the early morning;
- the Ora from southerly directions in the afternoon.

So it was not the finished forecasting formula that transferred, but the
process:

1. First, define precisely what “the wind was there” means.
2. Then, find the longest possible local measurement series as ground truth.
3. Build physically plausible features from large-scale weather data.
4. Evaluate the model year by year, outside its training data.
5. Finally, test whether the effect still holds with real forecast data, not
   just retrospectively with reanalysis.

Torbole offers a surprisingly good foundation for this: around 14 years of
wind measurements from Meteotrentino station T0193. Direction, speed, and time
of day can be used to derive separate labels for Peler and Ora.

The first result surprised me. Both wind systems were substantially more
predictable than a simple monthly baseline. In year-wise cross-validation,
Ora achieved a Peirce Skill Score of +0.54 and Peler +0.39. Their respective
monthly climatologies reached only around +0.2.

For this particular question, Lake Garda was not harder than the Walchensee. It
was statistically clearer.

The experiment has since become a small public product:
[Garda Oracle](https://garda.simon-stieber.de/go/linkedin) shows separate
three-day probabilities for Ora and Peler and explains which weather factors
have the strongest influence on each forecast.

In the next post, I will look at the decisive test: Does the model retain its
skill when it uses yesterday's actual forecast instead of weather data
reconstructed in hindsight?

---

## Suggested media

- Hero image: screenshot of the three daily forecast cards
- Second image: a small Walchensee → method → Lake Garda diagram
- Link: live dashboard; add the repository after public release

## Possible short opener

> I wanted to know whether a local wind model could be transferred to another
> Alpine lake. The surprising answer: the model did not transfer, but the
> method did.
