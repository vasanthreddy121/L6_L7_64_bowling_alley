import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# ---------------------------------------------------------
# Test Cases for Branch Coverage & Decision Edge Cases
# Student SRN: PES2UG25CS829
# ---------------------------------------------------------

# =========================================================
# Tests for lane_cost
# =========================================================

def test_lane_cost_weekday_standard():
    # Day: weekday, players <= 4, no league discount
    # cost = 400 * 2 + 0 + 2 * 50 = 900
    assert lane_cost("weekday", 2, 4, 2, False) == 900


def test_lane_cost_weekend_standard():
    # Day: weekend, players <= 4, no league discount
    # cost = 600 * 1 + 0 + 1 * 50 = 650
    assert lane_cost("weekend", 1, 3, 1, False) == 650


def test_lane_cost_invalid_day_type():
    # Branch: day_type not in LANE_RATE (True)
    with pytest.raises(ValueError, match="unknown day type"):
        lane_cost("holiday", 1, 2, 1, False)


def test_lane_cost_games_less_than_one():
    # Branch: games < 1 (True)
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 0, 4, 2, False)


def test_lane_cost_players_less_than_one():
    # Branch: players < 1 (True)
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 1, 0, 0, False)


def test_lane_cost_players_greater_than_six():
    # Branch: players > 6 (True)
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 1, 7, 2, False)


def test_lane_cost_shoe_rentals_exceed_players():
    # Branch: shoe_rentals > players (True)
    with pytest.raises(ValueError, match="too many shoe rentals"):
        lane_cost("weekday", 1, 3, 4, False)


def test_lane_cost_shoe_rentals_equal_players():
    # Branch: shoe_rentals > players (False - boundary equal)
    # cost = 400 * 1 + 0 + 3 * 50 = 550
    assert lane_cost("weekday", 1, 3, 3, False) == 550


def test_lane_cost_players_boundary_four_no_surcharge():
    # Branch: players > 4 (False - boundary: 4 players)
    # cost = 400 * 1 + 0 + 0 = 400
    assert lane_cost("weekday", 1, 4, 0, False) == 400


def test_lane_cost_players_surcharge_five_players():
    # Branch: players > 4 (True - 5 players)
    # cost = 400 * 2 + 100 * 2 + 2 * 50 = 800 + 200 + 100 = 1100
    assert lane_cost("weekday", 2, 5, 2, False) == 1100


def test_lane_cost_players_surcharge_max_players_six():
    # Branch: players > 4 (True - 6 players)
    # cost = 600 * 1 + 100 * 1 + 6 * 50 = 600 + 100 + 300 = 1000
    assert lane_cost("weekend", 1, 6, 6, False) == 1000


def test_lane_cost_league_member_discount():
    # Branch: is_league_member (True)
    # base = 400 * 1 = 400. discount = 400 // 5 = 80 -> cost = 320
    assert lane_cost("weekday", 1, 2, 0, True) == 320


def test_lane_cost_non_league_member_no_discount():
    # Branch: is_league_member (False)
    # base = 400 * 1 = 400
    assert lane_cost("weekday", 1, 2, 0, False) == 400


# =========================================================
# Tests for frame_score
# =========================================================

def test_frame_score_first_roll_negative():
    # Branch: first_roll < 0 (True)
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(-1, 5, [])


def test_frame_score_first_roll_exceeds_ten():
    # Branch: first_roll > 10 (True)
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(11, 0, [])


def test_frame_score_second_roll_negative():
    # Branch: second_roll < 0 (True)
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(5, -1, [])


def test_frame_score_strike_true():
    # Branch: first_roll == 10 (True)
    # Score = 10 + 10 + 10 = 30
    assert frame_score(10, 0, [10, 10]) == 30


def test_frame_score_strike_with_other_bonuses():
    # Branch: first_roll == 10 (True)
    assert frame_score(10, 0, [5, 4]) == 19


def test_frame_score_frame_sum_exceeds_ten():
    # Branch: first_roll + second_roll > 10 (True)
    with pytest.raises(ValueError, match="invalid frame"):
        frame_score(6, 5, [])


def test_frame_score_spare_true():
    # Branch: first_roll + second_roll == 10 (True)
    # Score = 10 + bonus_rolls[0]
    assert frame_score(7, 3, [8]) == 18


def test_frame_score_spare_zero_first_roll():
    # Branch: first_roll + second_roll == 10 (True, boundary 0 + 10)
    assert frame_score(0, 10, [6]) == 16


def test_frame_score_open_frame_normal():
    # Branch: open frame (first_roll + second_roll < 10)
    assert frame_score(3, 4, []) == 7


def test_frame_score_open_frame_zero_rolls():
    # Branch: open frame with zeroes (boundary 0 + 0)
    assert frame_score(0, 0, []) == 0


# =========================================================
# Tests for lane_assignment
# =========================================================

def test_lane_assignment_no_lanes_free():
    # Branch: lanes_free == 0 (True)
    assert lane_assignment(4, False, 0) == "wait"


def test_lane_assignment_kids_bumper_lane():
    # Branch: has_kids (True) with lanes available
    assert lane_assignment(3, True, 2) == "bumper lane"


def test_lane_assignment_kids_even_if_large_party():
    # Branch: has_kids (True) takes precedence over party size
    assert lane_assignment(8, True, 3) == "bumper lane"


def test_lane_assignment_large_party_multiple_lanes_available():
    # Branch: players > 6 and lanes_free >= 2 (True and True)
    assert lane_assignment(7, False, 2) == "two lanes"


def test_lane_assignment_large_party_plenty_lanes():
    # Branch: players > 6 and lanes_free >= 2 (True and True, larger)
    assert lane_assignment(10, False, 5) == "two lanes"


def test_lane_assignment_large_party_only_one_lane_free():
    # Branch: players > 6 and lanes_free < 2 -> elif players > 6 (True)
    assert lane_assignment(7, False, 1) == "wait"


def test_lane_assignment_standard_lane_small_party():
    # Branch: players <= 6, has_kids False, lanes_free > 0 -> standard lane
    assert lane_assignment(4, False, 1) == "standard lane"


def test_lane_assignment_standard_lane_boundary_six_players():
    # Branch: players == 6 (boundary <= 6), lanes_free >= 2 -> standard lane
    assert lane_assignment(6, False, 3) == "standard lane"
