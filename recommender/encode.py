from math import cos, pi, sin, sqrt

import numpy as np

from recommender.constants import (
    BUDGET_RANK,
    PLACE_TYPES,
    SCORE_COLS,
    WEATHERS,
)


def active_feature_blocks(prefs):
    blocks = []
    if prefs.get("budget"):
        blocks.append("budget")
    if prefs.get("place_type"):
        blocks.append("place_type")
    if prefs.get("weather"):
        blocks.append("weather")
    for col in SCORE_COLS:
        if prefs.get(col, 0) > 0:
            blocks.append(col)
    if prefs.get("trip_days"):
        blocks.append("trip_days")
    return blocks


SCORE_WEIGHT = 2.0
CATEGORY_WEIGHT = 1.25
TRIP_DAYS_WEIGHT = 1.0


def _one_hot(value, choices, weight=CATEGORY_WEIGHT):
    """Encode an unordered category with a constant block magnitude."""
    scale = sqrt(weight)
    return [scale if value == choice else 0.0 for choice in choices]


def _ordinal_pair(value, minimum, maximum, weight):
    """Map an ordinal value to a constant-length vector on a quarter circle.

    A two-dimensional encoding is important for cosine similarity: encoding a
    rating as one positive scalar would make all non-zero ratings point in the
    same direction and therefore appear perfectly similar.
    """
    span = float(maximum) - float(minimum)
    position = 0.0 if span == 0 else (float(value) - float(minimum)) / span
    position = min(1.0, max(0.0, position))
    angle = position * pi / 2.0
    scale = sqrt(weight)
    return [scale * cos(angle), scale * sin(angle)]


def destination_matrix(df, blocks, prefs=None):
    rows = []
    for _, item in df.iterrows():
        rows.append(_destination_vector(item, blocks, prefs))
    return np.array(rows, dtype=float)


def user_vector(prefs, blocks):
    vec = []
    if "budget" in blocks:
        vec.extend(
            _ordinal_pair(BUDGET_RANK[prefs["budget"]], 1, 3, CATEGORY_WEIGHT)
        )
    if "place_type" in blocks:
        vec.extend(_one_hot(prefs["place_type"], PLACE_TYPES))
    if "weather" in blocks:
        vec.extend(
            _ordinal_pair(WEATHERS.index(prefs["weather"]), 0, 3, CATEGORY_WEIGHT)
        )
    for col in SCORE_COLS:
        if col in blocks:
            vec.extend(_ordinal_pair(prefs[col], 1, 5, SCORE_WEIGHT))
    if "trip_days" in blocks:
        vec.extend(_ordinal_pair(prefs["trip_days"], 1, 30, TRIP_DAYS_WEIGHT))
    return np.array(vec, dtype=float).reshape(1, -1)


def _destination_vector(item, blocks, prefs=None):
    vec = []
    if "budget" in blocks:
        vec.extend(
            _ordinal_pair(BUDGET_RANK[item["budget"]], 1, 3, CATEGORY_WEIGHT)
        )
    if "place_type" in blocks:
        vec.extend(_one_hot(item["place_type"], PLACE_TYPES))
    if "weather" in blocks:
        vec.extend(
            _ordinal_pair(WEATHERS.index(item["weather"]), 0, 3, CATEGORY_WEIGHT)
        )
    for col in SCORE_COLS:
        if col in blocks:
            vec.extend(_ordinal_pair(item[col], 1, 5, SCORE_WEIGHT))
    if "trip_days" in blocks:
        minimum = float(item["trip_days_min"])
        maximum = float(item["trip_days_max"])
        if prefs and prefs.get("trip_days"):
            wanted = float(prefs["trip_days"])
            representative_days = min(max(wanted, minimum), maximum)
        else:
            representative_days = (minimum + maximum) / 2.0
        vec.extend(_ordinal_pair(representative_days, 1, 30, TRIP_DAYS_WEIGHT))
    return vec
