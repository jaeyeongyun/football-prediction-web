"""Integration tests for the Flask routes in app.py.

Uses Flask's test client, so no real server or network access is needed
(the one route that hits the live ESPN API -- /api/fixtures -- is
intentionally not covered here for that reason).
"""
import pytest

from app import app as flask_app
from database import LEAGUE_DATA


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as client:
        yield client


def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_leagues_endpoint_returns_the_full_league_table(client):
    response = client.get("/api/leagues")
    assert response.status_code == 200
    assert response.get_json() == LEAGUE_DATA


def test_predict_requires_all_three_query_params(client):
    response = client.get("/api/predict", query_string={"league": "epl"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_rejects_an_unknown_league(client):
    response = client.get(
        "/api/predict",
        query_string={"league": "not-a-real-league", "home": "mancity", "away": "arsenal"},
    )
    assert response.status_code == 404


def test_predict_rejects_an_unknown_team(client):
    response = client.get(
        "/api/predict",
        query_string={"league": "epl", "home": "mancity", "away": "not-a-real-team"},
    )
    assert response.status_code == 404


def test_predict_returns_a_full_prediction_for_a_known_fixture(client):
    response = client.get(
        "/api/predict",
        query_string={"league": "epl", "home": "mancity", "away": "arsenal"},
    )
    assert response.status_code == 200
    body = response.get_json()
    for key in ("home_win_p", "draw_p", "away_win_p", "top_scores", "insight"):
        assert key in body


def test_predict_accepts_a_custom_team_name(client):
    response = client.get(
        "/api/predict",
        query_string={"league": "epl", "home": "custom_My Sunday League FC", "away": "arsenal"},
    )
    assert response.status_code == 200
    assert response.get_json()["home_team"] == "My Sunday League FC"


def test_simulate_requires_home_and_away_stats(client):
    response = client.post("/api/simulate", json={"home": {}})
    assert response.status_code == 400


def test_simulate_returns_a_monte_carlo_result(client):
    payload = {
        "home": {"attack": 70, "defense": 60, "form": 65, "home_advantage": True},
        "away": {"attack": 40, "defense": 45, "form": 50, "home_advantage": True},
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    body = response.get_json()
    assert body["simulations"] == 10000
    assert body["home_win_p"] + body["draw_p"] + body["away_win_p"] == pytest.approx(100.0, abs=0.2)


def test_simulate_clamps_out_of_range_stats_instead_of_crashing(client):
    payload = {
        "home": {"attack": 999, "defense": -50, "form": "not-a-number"},
        "away": {"attack": 50, "defense": 50, "form": 50},
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
