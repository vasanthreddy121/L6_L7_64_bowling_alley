import pytest
from bowling_alley import lane_cost, frame_score, lane_assignment


# ---------------------------------------------------------
# Test Cases for Code (Statement) Coverage
# Student SRN: PES2UG25CS829
# ---------------------------------------------------------

# --- Tests for lane_cost ---

def test_lane_cost_weekday_standard():
    # Normal weekday booking without extra player fee or league discount
    assert lane_cost("weekday", 2, 4, 2, False) == 900


def test_lane_cost_invalid_day_type():
    # Covers line 5-6: day_type not in LANE_RATE
    with pytest.raises(ValueError, match="unknown day type"):
        lane_cost("holiday", 1, 3, 1, False)


def test_lane_cost_invalid_booking_games():
    # Covers line 7-8: games < 1
    with pytest.raises(ValueError, match="invalid booking"):
        lane_cost("weekday", 0, 3, 1, False)


def test_lane_cost_too_many_shoes():
    # Covers line 9-10: shoe_rentals > players
    with pytest.raises(ValueError, match="too many shoe rentals"):
        lane_cost("weekday", 1, 2, 3, False)


def test_lane_cost_weekend_large_group_league_member():
    # Covers line 11, line 12-13 (players > 4), line 14, line 15-16 (is_league_member)
    # Weekend rate: 600 * 2 = 1200
    # players > 4 (5): + 100 * 2 = +200 -> 1400
    # shoes: 3 * 50 = 150 -> 1550
    # league discount: 1550 - (1550 // 5) = 1550 - 310 = 1240
    assert lane_cost("weekend", 2, 5, 3, True) == 1240


# --- Tests for frame_score ---

def test_frame_score_invalid_first_roll():
    # Covers line 21-22: first_roll < 0
    with pytest.raises(ValueError, match="invalid roll"):
        frame_score(-1, 5, [])


def test_frame_score_strike():
    # Covers line 23-24: strike (first_roll == 10)
    assert frame_score(10, 0, [10, 10]) == 30


def test_frame_score_invalid_frame_sum():
    # Covers line 25-26: first_roll + second_roll > 10
    with pytest.raises(ValueError, match="invalid frame"):
        frame_score(7, 5, [])


def test_frame_score_spare():
    # Covers line 27-28: spare (first_roll + second_roll == 10)
    assert frame_score(6, 4, [5]) == 15


def test_frame_score_open_frame():
    # Covers line 29: open frame return
    assert frame_score(3, 4, []) == 7


# --- Tests for lane_assignment ---

def test_lane_assignment_no_lanes_free():
    # Covers line 33-34: lanes_free == 0
    assert lane_assignment(4, False, 0) == "wait"


def test_lane_assignment_has_kids():
    # Covers line 35-36: has_kids is True
    assert lane_assignment(3, True, 2) == "bumper lane"


def test_lane_assignment_large_party_two_lanes():
    # Covers line 37-38: players > 6 and lanes_free >= 2
    assert lane_assignment(8, False, 3) == "two lanes"


def test_lane_assignment_large_party_wait():
    # Covers line 39-40: players > 6 and lanes_free < 2
    assert lane_assignment(8, False, 1) == "wait"


def test_lane_assignment_standard_lane():
    # Covers line 41: standard lane return
    assert lane_assignment(4, False, 2) == "standard lane"
