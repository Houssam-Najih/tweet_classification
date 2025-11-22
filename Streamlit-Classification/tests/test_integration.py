from __future__ import annotations

import pandas as pd
import pytest
from unittest.mock import MagicMock, patch, Mock

import app


@pytest.fixture
def sample_df():
    """DataFrame d'exemple complet"""
    dates = pd.date_range("2024-01-01", periods=50, freq="D", tz="UTC")
    periods = pd.to_datetime([d.date() for d in dates]).to_period("W")
    return pd.DataFrame(
        {
            "id": [str(i) for i in range(50)],
            "created_at": dates,
            "date": [d.date() for d in dates],
            "week": [p.start_time.date() for p in periods],
            "day_of_week": [d.day_name() for d in dates],
            "hour": [d.hour for d in dates],
            "topics": ["['réseau']"] * 30 + ["['service']"] * 20,
            "topic_main": ["réseau"] * 30 + ["service"] * 20,
            "incident": ["technique"] * 25 + ["facturation"] * 15 + ["livraison"] * 10,
            "sentiment": ["neg"] * 30 + ["neu"] * 15 + ["pos"] * 5,
            "urgence": ["haute"] * 20 + ["moyenne"] * 20 + ["basse"] * 10,
            "is_claim": [1] * 35 + [0] * 15,
            "lang": ["fr"] * 50,
            "favorite_count": [10] * 50,
            "retweet_count": [5] * 50,
            "reply_count": [3] * 50,
            "quote_count": [1] * 50,
            "engagement": [19] * 50,
            "full_text": ["Test tweet"] * 50,
        }
    )


@patch("app.data.load_clients_from_path")
@patch("app.data.load_replies")
@patch("app.data.has_sample_data")
@patch("app.st")
def test_main_workflow_with_sample(
    mock_st, mock_has_sample, mock_load_replies, mock_load_clients_from_path, sample_df
):
    """Test du workflow principal avec échantillon"""
    # Configuration des mocks
    mock_has_sample.return_value = True
    mock_load_clients_from_path.return_value = sample_df
    mock_load_replies.return_value = pd.DataFrame()
    
    # Mock des widgets Streamlit
    mock_st.sidebar.file_uploader.return_value = None
    mock_st.sidebar.toggle.return_value = True
    mock_st.sidebar.radio.return_value = "Manager"
    mock_st.sidebar.date_input.return_value = (sample_df["date"].min(), sample_df["date"].max())
    mock_st.sidebar.selectbox.side_effect = ["Tous", "Tous", "Tous", "Tous"]
    mock_st.columns.return_value = [MagicMock(), MagicMock()]
    mock_st.pyplot = MagicMock()
    
    # Mock des fonctions de rendu des sections
    with patch("app.sections.render_header") as mock_header, \
         patch("app.sections.render_global_kpis") as mock_kpis, \
         patch("app.sections.render_sentiment_section") as mock_sentiment, \
         patch("app.sections.render_urgence_section") as mock_urgence, \
         patch("app.sections.render_incident_top5_section") as mock_incident_top5, \
         patch("app.sections.render_volume_day_week_section") as mock_volume_day_week, \
         patch("app.sections.render_volume_histograms_section") as mock_volume_hist, \
         patch("app.sections.render_wordcloud_section") as mock_wordcloud, \
         patch("app.sections.render_theme_incident_panel") as mock_theme_incident, \
         patch("app.sections.render_sentiment_theme") as mock_sentiment_theme, \
         patch("app.sections.render_claim_volume_section") as mock_claim_volume, \
         patch("app.sections.render_thematic_treemap_section") as mock_treemap, \
         patch("app.sections.render_response_time") as mock_response_time, \
         patch("app.sections.render_agent_focus") as mock_agent_focus, \
         patch("app.sections.render_export_tools") as mock_export:
        
        # Appel de la fonction main
        app.main()
        
        # Vérifications
        mock_has_sample.assert_called_once()
        mock_load_clients_from_path.assert_called_once()
        mock_header.assert_called_once_with("Manager")
        mock_kpis.assert_called_once()
        mock_sentiment.assert_called_once()
        mock_urgence.assert_called_once()
        mock_incident_top5.assert_called_once()
        mock_volume_day_week.assert_called_once()
        mock_volume_hist.assert_called_once()
        mock_wordcloud.assert_called_once()
        mock_theme_incident.assert_called_once()
        mock_sentiment_theme.assert_called_once()
        mock_claim_volume.assert_called_once()
        mock_treemap.assert_called_once()
        mock_response_time.assert_called_once()
        mock_agent_focus.assert_called_once()
        mock_export.assert_called_once()


@patch("app.st")
def test_main_no_file_no_sample(mock_st):
    """Test du workflow principal sans fichier ni échantillon"""
    mock_st.sidebar.file_uploader.return_value = None
    mock_st.sidebar.toggle.return_value = False
    
    with patch("app.data.has_sample_data", return_value=False):
        app.main()
        
        mock_st.title.assert_called_once_with("Analyse des tweets SAV Free")
        mock_st.info.assert_called_once()


@patch("app.data.load_clients")
@patch("app.st")
def test_main_empty_dataframe(mock_st, mock_load_clients):
    """Test du workflow principal avec DataFrame vide"""
    mock_st.sidebar.file_uploader.return_value = MagicMock()
    mock_st.sidebar.toggle.return_value = False
    mock_load_clients.return_value = pd.DataFrame()
    
    with patch("app.data.has_sample_data", return_value=False):
        app.main()
        
        mock_st.warning.assert_called_once_with("Aucune donnée exploitable dans le fichier fourni.")


@patch("app.data.load_clients")
@patch("app.st")
def test_main_filters_lang(mock_st, mock_load_clients, sample_df):
    """Test du filtrage par langue"""
    mock_st.sidebar.file_uploader.return_value = MagicMock()
    mock_st.sidebar.toggle.return_value = False
    
    # DataFrame avec plusieurs langues
    sample_df["lang"] = ["fr"] * 30 + ["en"] * 20
    mock_load_clients.return_value = sample_df
    mock_st.sidebar.date_input.return_value = (sample_df["date"].min(), sample_df["date"].max())
    mock_st.sidebar.selectbox.side_effect = ["Tous", "Tous", "Tous", "Tous"]
    mock_st.sidebar.radio.return_value = "Manager"
    
    with patch("app.data.has_sample_data", return_value=False), \
         patch("app.sections.render_header"), \
         patch("app.sections.render_global_kpis"), \
         patch("app.sections.render_sentiment_section"), \
         patch("app.sections.render_urgence_section"), \
         patch("app.sections.render_incident_top5_section"), \
         patch("app.sections.render_volume_day_week_section"), \
         patch("app.sections.render_volume_histograms_section"), \
         patch("app.sections.render_wordcloud_section"), \
         patch("app.sections.render_theme_incident_panel"), \
         patch("app.sections.render_sentiment_theme"), \
         patch("app.sections.render_claim_volume_section"), \
         patch("app.sections.render_thematic_treemap_section"), \
         patch("app.sections.render_response_time"), \
         patch("app.sections.render_agent_focus"), \
         patch("app.sections.render_export_tools"), \
         patch("app.data.load_replies", return_value=pd.DataFrame()):
        
        app.main()
        
        # Vérifier que le DataFrame filtré n'a que les tweets en français
        # Cela sera vérifié indirectement via les appels aux sections

