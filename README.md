[![CI](https://github.com/jaeyeongyun/football-prediction-web/actions/workflows/ci.yml/badge.svg)](https://github.com/jaeyeongyun/football-prediction-web/actions/workflows/ci.yml)
# Football Match Prediction & Simulation

A Python web platform that predicts football match outcomes using a Poisson distribution model and Monte Carlo simulation.

## Features

**Match prediction**
Combines each club's attack/defence rating, Elo rating, and recent form into a Poisson distribution model, producing a full scoreline probability matrix. From that matrix the app derives win/draw/loss probabilities, Over/Under 2.5 goals, and both-teams-to-score (BTTS) probabilities.

**Interactive simulator**
Lets users set attack strength, defence strength, and recent form for two teams via sliders, then runs a 10,000-trial Monte Carlo simulation (using a Knuth-style Poisson sampler) to produce the most likely scorelines and win probabilities.

**Live fixtures**
Pulls live and upcoming fixtures for the Premier League, La Liga, Serie A, and Bundesliga from ESPN's public scoreboard API, with a 60-second local cache to avoid hammering the endpoint.

**Power rankings**
A per-club table combining the underlying ratings, recent form, and a short note on playing style.

## Data sources

- **Live scores and fixtures**: [ESPN's public site API](https://site.api.espn.com/apis/site/v2/sports/soccer/) (no API key required).
- **Team ratings** (attack, defence, Elo): manually curated by me for the 2025–26 season for ~20 top clubs across the four leagues. This is a static snapshot, not pulled from a stats provider, and it isn't updated automatically as form changes.

## Known limitations

- Only the clubs listed in `database.py` have real ratings; any other team falls back to a generic default (Elo 1650).
- Team ratings are a manual snapshot and need to be updated by hand to stay current.
- The ESPN endpoint is a public, unofficial API and could change or rate-limit without notice.

## Tech stack

- **Backend**: Python 3, Flask (REST API)
- **Frontend**: HTML5, vanilla CSS3, vanilla JavaScript
- **Statistical core**: Poisson probability distribution, Monte Carlo simulation

## Getting started

```bash
git clone https://github.com/jaeyeongyun/football-prediction-web.git
cd football-prediction-web
pip install Flask
python app.py
```

Then open `http://localhost:5000` in a browser.

## Project structure

```text
football-prediction-web/
├── app.py                 # Flask app entry point and API routes
├── prediction_engine.py   # Poisson distribution and Monte Carlo simulation logic
├── database.py             # Manually curated club ratings and sample fixtures
├── live_updater.py         # ESPN API integration and local caching
├── templates/
│   └── index.html         # Main page template
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js         # API calls and UI logic
└── .gitignore
```

## License

Open source. Free to use, modify, and distribute.
