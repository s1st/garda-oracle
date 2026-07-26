# LinkedIn draft 3: From a notebook to a small public weather application

*Working draft · English*

A model in a notebook is not yet a product.

After the Ora and Peler experiments, I wanted an application I would actually
use on my phone at the lake: fast, concise, and usable without meteorological
expertise, but transparent enough that I would not have to trust a probability
blindly.

That became [Garda Oracle](https://garda.simon-stieber.de/go/linkedin).

The home page shows two separate cards for today, tomorrow, and the day after:

- Peler in the early morning;
- Ora in the afternoon.

Each card contains a GO, MAYBE, or NO GO assessment and its probability.
Opening a card reveals the factors that move the model's score most strongly
up or down that day, such as the pressure gradient, cloud cover, solar
radiation, or precipitation.

For the linear model, these contributions are mathematically exact: they show
which standardised inputs changed the logit most. They are not proof of
causality. The site therefore explains both the physical meaning of each
factor and this limitation.

The technical setup is deliberately small:

- FastAPI and Jinja2 for the website;
- Open-Meteo for the forecast fields;
- Meteotrentino T0193 for current and historical observations;
- a 30-minute cache for forecasts and a five-minute cache for live wind;
- Cloud Run as a stateless service;
- German, English, and Italian without an external translation system.

The models are trained offline with scikit-learn. The running service,
however, includes neither scikit-learn nor pandas nor NumPy. Means, standard
deviations, coefficients, calibration parameters, and thresholds are exported
as Python data. Runtime inference is reduced to a dot product and a logistic
function.

The most important technical protection against subtle inconsistencies is
less visible: training and website use the same feature builder. Time windows
and pressure differences are not implemented independently in two places. A
golden-vector test also freezes one known model response.

I am now preparing the project for open-source release. That involves more
than adding a licence and a polished README:

- documented data licences and attribution;
- no raw datasets committed to the repository;
- a reproducible fetch, labelling, training, and export pipeline;
- a model card covering limitations and negative results;
- automated tests, linting, type checking, and package builds;
- clear notice that this is not an official weather or safety forecast.

The code relies exclusively on openly available or clearly reusable data
sources. This makes it possible to show not only the application but the
entire path from public measurements to the delivered probability.

What I am taking away from the project:

1. A precise local question is often more valuable than another general
   weather model.
2. The transfer from reanalysis to real forecast inputs must be tested
   explicitly.
3. Explainability starts with a consistent data pipeline, not with a tooltip.
4. Data licensing is part of the architecture.
5. A small model with honest validation can be surprisingly useful for a
   specific decision.

Live: <https://garda.simon-stieber.de/go/linkedin>

Repository: **Add link after public release**

---

## Suggested media

- Main image: mobile screenshot of the forecast cards
- Second image: opened factor dialog
- Third image: architecture diagram or excerpt from the model card

## Possible closing question

> Which small, local decisions would you like to derive from general weather
> data if a good measurement series were available as ground truth?
