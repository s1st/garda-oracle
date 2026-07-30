# Can a local wind model be transferred to another Alpine lake?

*LinkedIn article · English · Publication copy*

## The model did not transfer. The method did.

Some time ago, I built [Walchi Thermic Oracle](https://walchensee.simon-stieber.de/), a small forecasting system for Walchensee. The question behind it was deliberately practical:

**Will the local thermal wind develop today, or will the trip to the lake be for nothing?**

Global weather models provide many of the ingredients needed to approach that question: air pressure, cloud cover, solar radiation, precipitation, humidity, and wind at different altitudes.

What they do not directly provide is the local answer for one particular place. Whether a thermal wind establishes itself at a specific lake depends on the interaction between the large-scale weather situation, the surrounding topography, and local heating.

When I started looking at Lake Garda, this led to a new question:

**Could the methodology behind a local wind forecast be transferred to a different thermal wind system?**

## Two lakes, different wind systems

Copying the finished Walchensee model was never a realistic option. The two lakes work too differently.

At Walchensee, the main phenomenon is a local northerly thermal wind driven by topography and solar heating. At the northern end of Lake Garda, two characteristic wind regimes shape the day:

- **Peler**, which blows from northerly directions in the early morning;
- **Ora**, which arrives from southerly directions in the afternoon.

The timing, direction, and physical setting differ. A formula trained for one lake should not simply be applied to the other.

What could be transferred was the process used to build and test it.

## What actually transferred

The reusable methodology consists of five steps:

1. **Define the local outcome precisely.** “There was wind” is too vague. Direction, time window, and minimum average speed need explicit definitions.

2. **Find a long local measurement series as ground truth.** A model can only learn a local phenomenon if there is a consistent record of when that phenomenon actually occurred.

3. **Build physically plausible features from large-scale weather data.** Useful signals include pressure differences, solar radiation, cloud cover, precipitation, humidity, and wind at different altitudes.

4. **Evaluate outside the training data.** Holding out complete years helps prevent individual weather situations from the same season appearing in both training and evaluation.

5. **Test the transition from hindsight to a real forecast.** Skill measured with historical reanalysis is not enough. The model must still work with the information that was genuinely available before the event.

This process is more transferable than any individual coefficient or threshold.

## Fourteen years of observations in Torbole

Lake Garda offers a surprisingly strong foundation for this experiment. Meteotrentino station T0193 in Torbole provides around 14 years of local wind measurements.

Direction, average speed, and time of day can be used to derive separate, reproducible labels for Peler and Ora. These observations form the ground truth. Large-scale historical weather fields provide the possible explanatory signals.

I trained two separate logistic models: one for Ora and one for Peler.

The goal was not to build the most complex possible machine-learning system. It was to find out whether relatively simple, explainable models could distinguish favourable from unfavourable days better than the seasonal pattern alone.

## Better than knowing only the month

As a simple baseline, I used only the historical frequency of each wind regime in a given month.

That baseline already contains useful information. Ora and Peler are seasonal, so knowing the month gives a model some predictive power. But it knows nothing about the actual pressure distribution, cloud cover, radiation, or wind situation on a particular day.

Across approximately 2,972 complete seasonal days, evaluated by holding out each year in turn, the results were:

| Regime | Base rate | Model Peirce Skill Score | Monthly baseline |
|---|---:|---:|---:|
| Ora | 69% | **+0.54** | +0.22 |
| Peler | 53% | **+0.39** | +0.20 |

A Peirce Skill Score of zero means that a model has no useful discrimination; one would be perfect. The important comparison here is not Ora against Peler, but each model against its own monthly baseline.

Both models substantially improved on simply knowing the time of year.

For this particular question, Lake Garda was therefore not harder to model than Walchensee. Statistically, the signal was clearer.

## From experiment to public application

The experiment has since become [Garda Oracle](https://garda.simon-stieber.de/go/linkedin), a small public application that shows separate three-day probabilities for Peler and Ora.

For each forecast, it also explains which weather factors move the model most strongly towards or away from a favourable outcome.

The complete project is available on [GitHub](https://github.com/s1st/garda-oracle), including the model card, validation results, training pipeline, and known limitations.

## The more important test comes next

These results answer the first question: the methodology transferred, and the models learned substantially more than monthly climatology.

But they do not yet prove that the system works as an operational forecast. Historical reanalysis describes past weather with information assembled after the event. A real forecast has access only to what was known beforehand.

The next article will therefore cover the decisive test:

**Does the model retain its skill when it uses yesterday's actual forecast instead of weather reconstructed in hindsight?**

---

## Suggested article media

- Cover image: mobile view of the Garda Oracle three-day forecast
- In-body image: Walchensee → transferable method → Lake Garda
- Optional result graphic: model scores versus the monthly baselines
