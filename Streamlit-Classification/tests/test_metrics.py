from __future__ import annotations

import pandas as pd
import pytest

from app_core.metrics import compute_response_time, minutes_to_dhm


def test_minutes_to_dhm_formats():
    assert minutes_to_dhm(0) == "0 min"
    assert minutes_to_dhm(45) == "45 min"
    assert minutes_to_dhm(1500) == "1 jour 1 h"
    assert minutes_to_dhm(1505) == "1 jour 1 h 5 min"


def test_minutes_to_dhm_none():
    assert minutes_to_dhm(None) == "N/A"


def test_compute_response_time_empty_frames():
    empty = pd.DataFrame()
    assert compute_response_time(empty, empty) == (None, None, None)


def test_compute_response_time_nominal_case():
    df_clients = pd.DataFrame(
        {
            "id": ["1", "2", "3"],
            "created_at": [
                "2024-07-10 10:00:00+00:00",
                "2024-07-10 10:05:00+00:00",
                "2024-07-10 10:10:00+00:00",
            ],
        }
    )
    df_replies = pd.DataFrame(
        {
            "in_reply_to": ["1", "2", "2", "3"],
            "created_at": [
                "2024-07-10 10:07:00+00:00",  # 7 min
                "2024-07-10 10:20:00+00:00",  # 15 min for id=2 (first)
                "2024-07-10 10:40:00+00:00",  # ignored
                "2024-07-10 10:25:00+00:00",  # 15 min
            ],
        }
    )

    first_reply, mean_delay, median_delay = compute_response_time(df_clients, df_replies)

    assert len(first_reply) == 3
    assert pytest.approx(mean_delay, rel=1e-3) == 12.3333333333
    assert median_delay == 15


def test_compute_response_time_requires_in_reply_to():
    df_clients = pd.DataFrame({"id": ["1"], "created_at": ["2024-07-10 10:00:00+00:00"]})
    df_replies = pd.DataFrame({"id": ["r1"], "created_at": ["2024-07-10 10:03:00+00:00"]})

    assert compute_response_time(df_clients, df_replies) == (None, None, None)


