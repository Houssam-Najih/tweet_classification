from __future__ import annotations

import pandas as pd
import pytest

from app_core.plots import (
    incident_top5_bar,
    thematic_treemap,
    volume_day_line,
    volume_dayofweek_bar,
    volume_hour_bar,
    volume_week_bar,
)


@pytest.fixture
def sample_df_sav():
    """DataFrame d'exemple avec tweets SAV"""
    dates = pd.date_range("2024-01-01", periods=30, freq="D", tz="UTC")
    periods = pd.to_datetime([d.date() for d in dates]).to_period("W")
    return pd.DataFrame(
        {
            "id": [str(i) for i in range(30)],
            "date": [d.date() for d in dates],
            "week": [p.start_time.date() for p in periods],
            "day_of_week": [d.day_name() for d in dates],
            "hour": [d.hour for d in dates],
            "incident": ["technique"] * 15 + ["facturation"] * 10 + ["livraison"] * 5,
            "topic_main": ["réseau"] * 20 + ["service"] * 10,
            "sentiment": ["neg"] * 20 + ["neu"] * 7 + ["pos"] * 3,
            "urgence": ["haute"] * 12 + ["moyenne"] * 10 + ["basse"] * 8,
            "is_claim": [1] * 30,
        }
    )


def test_volume_day_line_empty():
    """Test volume_day_line avec DataFrame vide"""
    df = pd.DataFrame()
    result = volume_day_line(df)
    assert result is None


def test_volume_day_line_with_data(sample_df_sav):
    """Test volume_day_line avec données"""
    result = volume_day_line(sample_df_sav)
    assert result is not None
    assert result.layout.title.text == "Volume quotidien de tweets SAV"


def test_volume_week_bar_empty():
    """Test volume_week_bar avec DataFrame vide"""
    df = pd.DataFrame()
    result = volume_week_bar(df)
    assert result is None


def test_volume_week_bar_with_data(sample_df_sav):
    """Test volume_week_bar avec données"""
    result = volume_week_bar(sample_df_sav)
    assert result is not None
    assert result.layout.title.text == "Volume hebdomadaire de tweets SAV"


def test_volume_hour_bar_empty():
    """Test volume_hour_bar avec DataFrame vide"""
    df = pd.DataFrame()
    result = volume_hour_bar(df)
    assert result is None


def test_volume_hour_bar_with_data(sample_df_sav):
    """Test volume_hour_bar avec données"""
    result = volume_hour_bar(sample_df_sav)
    assert result is not None
    assert result.layout.title.text == "Volume de tweets SAV par heure"


def test_volume_dayofweek_bar_empty():
    """Test volume_dayofweek_bar avec DataFrame vide"""
    df = pd.DataFrame()
    result = volume_dayofweek_bar(df)
    assert result is None


def test_volume_dayofweek_bar_with_data(sample_df_sav):
    """Test volume_dayofweek_bar avec données"""
    result = volume_dayofweek_bar(sample_df_sav)
    assert result is not None
    assert result.layout.title.text == "Volume de tweets SAV par jour de la semaine"


def test_incident_top5_bar_empty():
    """Test incident_top5_bar avec DataFrame vide"""
    df = pd.DataFrame()
    result = incident_top5_bar(df)
    assert result is None


def test_incident_top5_bar_with_data(sample_df_sav):
    """Test incident_top5_bar avec données"""
    result = incident_top5_bar(sample_df_sav)
    assert result is not None
    assert result.layout.title.text == "Top 5 incidents les plus fréquents"
    # Vérifier qu'on a bien les 3 incidents uniques (technique, facturation, livraison)
    data = result.data[0]
    assert len(data.x) <= 5


def test_thematic_treemap_empty():
    """Test thematic_treemap avec DataFrame vide"""
    df = pd.DataFrame()
    result = thematic_treemap(df)
    assert result is None


def test_thematic_treemap_with_data(sample_df_sav):
    """Test thematic_treemap avec données"""
    result = thematic_treemap(sample_df_sav)
    assert result is not None
    assert "Cartographie des incidents par thème" in result.layout.title.text


def test_thematic_treemap_missing_columns():
    """Test thematic_treemap avec colonnes manquantes"""
    df = pd.DataFrame(
        {
            "id": ["1", "2"],
            "incident": ["technique", "facturation"],
            # topic_main manquant
        }
    )
    result = thematic_treemap(df)
    assert result is None

