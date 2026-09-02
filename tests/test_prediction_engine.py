"""Unit tests for prediction_engine.py.

Covers the pure-math pieces (Poisson PMF, form multiplier, xG calc) and the
two prediction entry points (generate_prediction, run_monte_carlo).
"""
import math

import pytest

from prediction_engine import (
    calculate_form_multiplier,
    generate_prediction,
    get_xg,
    poisson_probability,
    run_monte_carlo,
    sample_poisson,
)


# ---------------------------------------------------------------------------
# poisson_probability
# ---------------------------------------------------------------------------

def test_poisson_probability_matches_known_value():
    # P(0; 1) = e^-1
    assert poisson_probability(1, 0) == pytest.approx(math.exp(-1), rel=1e-9)


def test_poisson_probability_zero_lambda_puts_all_mass_on_zero_goals():
    assert poisson_probability(0, 0) == 1.0
    assert poisson_probability(0, 3) == 0.0


def test_poisson_probability_sums_to_roughly_one_over_a_wide_range():
    lmbda = 1.8
    total = sum(poisson_probability(lmbda, k) for k in range(30))
    assert total == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# calculate_form_multiplier
# ---------------------------------------------------------------------------

def test_form_multiplier_no_games_is_neutral():
    assert calculate_form_multiplier([]) == 1.0


def test_form_multiplier_perfect_form_is_capped_at_1_1():
    assert calculate_form_multiplier(["W", "W", "W", "W", "W"]) == pytest.approx(1.1)


def test_form_multiplier_all_losses_is_floored_at_0_9():
    assert calculate_form_multiplier(["L", "L", "L", "L", "L"]) == pytest.approx(0.9)


def test_form_multiplier_draws_sit_between_the_extremes():
    all_draws = calculate_form_multiplier(["D", "D", "D", "D", "D"])
    assert 0.9 < all_draws < 1.1


# ---------------------------------------------------------------------------
# get_xg
# ---------------------------------------------------------------------------

STRONG_HOME = {"attack": 2.4, "defense": 0.8, "elo": 1950, "form": ["W", "W", "W", "W", "W"]}
WEAK_AWAY = {"attack": 1.0, "defense": 1.6, "elo": 1400, "form": ["L", "L", "L", "L", "L"]}


def test_get_xg_favours_the_stronger_home_side():
    home_xg, away_xg = get_xg(STRONG_HOME, WEAK_AWAY)
    assert home_xg > away_xg


def test_get_xg_never_drops_below_the_floor():
    # Two threadbare teams should still clear the 0.2 expected-goal floor.
    weak = {"attack": 0.1, "defense": 5.0, "elo": 1000, "form": []}
    home_xg, away_xg = get_xg(weak, weak)
    assert home_xg >= 0.2
    assert away_xg >= 0.2


def test_get_xg_elo_gap_is_clamped_to_plus_minus_40_percent():
    # An absurd Elo gap should not blow past the documented +-40% clamp.
    home = {"attack": 1.5, "defense": 1.1, "elo": 5000, "form": []}
    away = {"attack": 1.5, "defense": 1.1, "elo": 100, "form": []}
    home_xg, _ = get_xg(home, away)
    # Base xG with these ratings and default home advantage, before the Elo term:
    base = 1.5 * 1.1 * 1.1
    # elo_adjust is clamped to 0.4, so the multiplier tops out at (1 + 0.4*0.5) = 1.2
    assert home_xg == pytest.approx(round(base * 1.2, 2))


# ---------------------------------------------------------------------------
# generate_prediction
# ---------------------------------------------------------------------------

def test_generate_prediction_outcome_probabilities_sum_to_100():
    result = generate_prediction(STRONG_HOME, WEAK_AWAY)
    total = result["home_win_p"] + result["draw_p"] + result["away_win_p"]
    assert total == pytest.approx(100.0, abs=0.2)


def test_generate_prediction_returns_top_three_scorelines():
    result = generate_prediction(STRONG_HOME, WEAK_AWAY)
    assert len(result["top_scores"]) == 3
    # Each top score should carry a well-formed "H - A" label.
    for entry in result["top_scores"]:
        assert entry["score"] == f"{entry['home']} - {entry['away']}"


def test_generate_prediction_favours_the_stronger_side():
    result = generate_prediction(STRONG_HOME, WEAK_AWAY)
    assert result["home_win_p"] > result["away_win_p"]


# ---------------------------------------------------------------------------
# sample_poisson / run_monte_carlo
# ---------------------------------------------------------------------------

def test_sample_poisson_near_zero_lambda_almost_always_returns_zero():
    random_state = __import__("random").Random(42)
    import prediction_engine as pe

    original_random = pe.random.random
    pe.random.random = random_state.random
    try:
        results = [sample_poisson(0.05) for _ in range(200)]
    finally:
        pe.random.random = original_random

    zero_fraction = results.count(0) / len(results)
    assert zero_fraction > 0.9


def test_run_monte_carlo_outcome_shares_sum_to_100():
    home_stats = {"attack": 80, "defense": 70, "form": 70, "home_advantage": True}
    away_stats = {"attack": 40, "defense": 40, "form": 40, "home_advantage": True}
    result = run_monte_carlo(home_stats, away_stats, num_simulations=2000)
    total = result["home_win_p"] + result["draw_p"] + result["away_win_p"]
    assert total == pytest.approx(100.0, abs=0.2)


def test_run_monte_carlo_respects_the_requested_trial_count():
    result = run_monte_carlo(
        {"attack": 50, "defense": 50, "form": 50}, {"attack": 50, "defense": 50, "form": 50},
        num_simulations=500,
    )
    assert result["simulations"] == 500


def test_run_monte_carlo_favours_the_stronger_side_on_average():
    strong = {"attack": 90, "defense": 85, "form": 80, "home_advantage": True}
    weak = {"attack": 20, "defense": 20, "form": 20, "home_advantage": True}
    result = run_monte_carlo(strong, weak, num_simulations=3000)
    assert result["home_win_p"] > result["away_win_p"]
