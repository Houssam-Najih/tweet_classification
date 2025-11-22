from __future__ import annotations

import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from app_core.sections import (
    render_incident_top5_section,
    render_thematic_treemap_section,
    render_volume_day_week_section,
    render_volume_histograms_section,
    render_wordcloud_section,
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
            "full_text": ["Test tweet négatif"] * 20 + ["Tweet neutre"] * 7 + ["Tweet positif"] * 3,
        }
    )


@patch("app_core.sections.st")
def test_render_incident_top5_section_empty(mock_st):
    """Test render_incident_top5_section avec DataFrame vide"""
    df = pd.DataFrame()
    render_incident_top5_section(df)
    mock_st.subheader.assert_called_once_with("Top 5 des incidents")
    mock_st.info.assert_called_once()


@patch("app_core.sections.st")
def test_render_incident_top5_section_with_data(mock_st, sample_df_sav):
    """Test render_incident_top5_section avec données"""
    render_incident_top5_section(sample_df_sav)
    mock_st.subheader.assert_called_once_with("Top 5 des incidents")
    mock_st.plotly_chart.assert_called_once()


@patch("app_core.sections.st")
def test_render_volume_day_week_section_empty(mock_st):
    """Test render_volume_day_week_section avec DataFrame vide"""
    df = pd.DataFrame()
    render_volume_day_week_section(df)
    mock_st.subheader.assert_called_once_with("Volume de tweets SAV par jour et par semaine")
    mock_st.info.assert_called_once()


@patch("app_core.sections.st")
def test_render_volume_day_week_section_with_data(mock_st, sample_df_sav):
    """Test render_volume_day_week_section avec données"""
    # Mock columns pour retourner deux colonnes
    mock_col1 = MagicMock()
    mock_col2 = MagicMock()
    mock_st.columns.return_value = [mock_col1, mock_col2]
    render_volume_day_week_section(sample_df_sav)
    mock_st.subheader.assert_called_once_with("Volume de tweets SAV par jour et par semaine")
    assert mock_st.columns.call_count == 1


@patch("app_core.sections.st")
def test_render_volume_histograms_section_empty(mock_st):
    """Test render_volume_histograms_section avec DataFrame vide"""
    df = pd.DataFrame()
    render_volume_histograms_section(df)
    mock_st.subheader.assert_called_once_with("Histogrammes de volume des tweets SAV")
    mock_st.info.assert_called_once()


@patch("app_core.sections.st")
def test_render_volume_histograms_section_with_data(mock_st, sample_df_sav):
    """Test render_volume_histograms_section avec données"""
    # Mock columns pour retourner deux colonnes
    mock_col1 = MagicMock()
    mock_col2 = MagicMock()
    mock_st.columns.return_value = [mock_col1, mock_col2]
    render_volume_histograms_section(sample_df_sav)
    mock_st.subheader.assert_called_once_with("Histogrammes de volume des tweets SAV")
    assert mock_st.columns.call_count == 1


@patch("app_core.sections.st")
@patch("app_core.sections.WordCloud")
@patch("app_core.sections.plt")
def test_render_wordcloud_section_empty(mock_plt, mock_wordcloud, mock_st):
    """Test render_wordcloud_section avec DataFrame vide"""
    df = pd.DataFrame()
    render_wordcloud_section(df)
    mock_st.subheader.assert_called_once_with("Nuage de mots — tweets SAV négatifs")
    mock_st.info.assert_called_once()


@patch("app_core.sections.st")
@patch("app_core.sections.WordCloud")
@patch("app_core.sections.plt")
def test_render_wordcloud_section_no_full_text(mock_plt, mock_wordcloud, mock_st, sample_df_sav):
    """Test render_wordcloud_section sans colonne full_text"""
    df = sample_df_sav.drop(columns=["full_text"])
    render_wordcloud_section(df)
    mock_st.subheader.assert_called_once_with("Nuage de mots — tweets SAV négatifs")
    mock_st.info.assert_called_once()


@patch("app_core.sections.st")
@patch("app_core.sections.WordCloud")
@patch("app_core.sections.plt")
def test_render_wordcloud_section_with_data(mock_plt, mock_wordcloud, mock_st, sample_df_sav):
    """Test render_wordcloud_section avec données"""
    mock_wc_instance = MagicMock()
    mock_wordcloud.return_value = mock_wc_instance
    # Mock subplots pour retourner figure et axes
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)
    
    render_wordcloud_section(sample_df_sav)
    mock_st.subheader.assert_called_once_with("Nuage de mots — tweets SAV négatifs")
    mock_wordcloud.assert_called_once()
    mock_plt.subplots.assert_called_once()
    mock_st.pyplot.assert_called_once()


@patch("app_core.sections.st")
def test_render_thematic_treemap_section_empty(mock_st):
    """Test render_thematic_treemap_section avec DataFrame vide"""
    df = pd.DataFrame()
    render_thematic_treemap_section(df)
    mock_st.subheader.assert_called_once_with("Cartographie thématique des types de souci")
    mock_st.info.assert_called_once()


@patch("app_core.sections.st")
def test_render_thematic_treemap_section_with_data(mock_st, sample_df_sav):
    """Test render_thematic_treemap_section avec données"""
    render_thematic_treemap_section(sample_df_sav)
    mock_st.subheader.assert_called_once_with("Cartographie thématique des types de souci")
    mock_st.plotly_chart.assert_called_once()


@patch("app_core.sections.st")
def test_render_thematic_treemap_section_missing_columns(mock_st):
    """Test render_thematic_treemap_section avec colonnes manquantes"""
    df = pd.DataFrame(
        {
            "id": ["1", "2"],
            "incident": ["technique", "facturation"],
            # topic_main manquant
        }
    )
    render_thematic_treemap_section(df)
    mock_st.subheader.assert_called_once_with("Cartographie thématique des types de souci")
    mock_st.info.assert_called_once()

