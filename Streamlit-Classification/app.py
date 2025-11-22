from __future__ import annotations

import pandas as pd
import streamlit as st

from app_core import data, sections
from app_core.config import (
    PROFILES,
    REPLIES_CSV_PATH,
    SAMPLE_CLIENTS_PATH,
)

# --------------------------------------------------
# CONFIG PAGE
# --------------------------------------------------
st.set_page_config(
    page_title="Free - Analyse SAV Twitter",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Tableau de bord Free SAV — Streamlit",
    },
)


def _side_filters(df):
    if df.empty:
        return df

    st.sidebar.markdown("---")
    st.sidebar.title("Filtres")

    min_date = df["date"].min()
    max_date = df["date"].max()

    date_range = st.sidebar.date_input(
        "Période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    start_date, end_date = (
        date_range if isinstance(date_range, tuple) else (date_range, date_range)
    )
    filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    def _options(column, label):
        if column not in filtered.columns:
            return ["Tous"], "Tous"
        values = sorted(filtered[column].dropna().unique().tolist())
        options = ["Tous"] + values
        selection = st.sidebar.selectbox(label, options)
        return options, selection

    _, selected_topic = _options("topic_main", "Thème (topic)")
    _, selected_sentiment = _options("sentiment", "Sentiment")
    _, selected_incident = _options("incident", "Type d'incident")
    _, selected_urgence = _options("urgence", "Niveau d'urgence")

    if selected_topic != "Tous":
        filtered = filtered[filtered["topic_main"] == selected_topic]
    if selected_sentiment != "Tous":
        filtered = filtered[filtered["sentiment"] == selected_sentiment]
    if selected_incident != "Tous":
        filtered = filtered[filtered["incident"] == selected_incident]
    if selected_urgence != "Tous":
        filtered = filtered[filtered["urgence"] == selected_urgence]

    return filtered


def _load_clients(uploaded_file, use_sample: bool):
    if use_sample:
        st.sidebar.success("Jeu d'exemple chargé.")
        return data.load_clients_from_path(SAMPLE_CLIENTS_PATH)
    return data.load_clients(uploaded_file)


def main():
    st.sidebar.title("Import du fichier")
    uploaded_file = st.sidebar.file_uploader(
        "Importer un fichier CSV de tweets clients",
        type=["csv"],
        accept_multiple_files=False,
    )

    can_use_sample = data.has_sample_data(SAMPLE_CLIENTS_PATH)
    use_sample = st.sidebar.toggle(
        "Utiliser l'échantillon",
        value=False,
        disabled=not can_use_sample,
        help="Charge un dataset de démonstration" if can_use_sample else "Ajoute Data/sample_clients.csv pour activer",
    )

    if uploaded_file is None and not use_sample:
        st.title("Analyse des tweets SAV Free")
        st.info(
            "Veuillez importer un fichier CSV dans la barre latérale "
            "ou activer l'échantillon pour afficher le tableau de bord."
        )
        return

    df = _load_clients(uploaded_file, use_sample)
    if df.empty:
        st.warning("Aucune donnée exploitable dans le fichier fourni.")
        return

    if "lang" in df.columns:
        df = df[df["lang"] == "fr"]

    if df.empty:
        st.warning("Toutes les lignes ont été filtrées (langue ≠ fr).")
        return

    df = _side_filters(df)

    if df.empty:
        st.warning("Les filtres sélectionnés n'ont retourné aucun tweet.")
        return

    df_sav = df[df["is_claim"] == 1]

    try:
        df_replies = data.load_replies(REPLIES_CSV_PATH)
    except Exception:
        df_replies = pd.DataFrame()
        st.sidebar.error(f"Fichier réponses introuvable : {REPLIES_CSV_PATH}")

    st.sidebar.markdown("---")
    profil = st.sidebar.radio("Profil de vue", PROFILES, index=0)

    sections.render_header(profil)

    if profil in {"Manager", "Data analyst"}:
        sections.render_global_kpis(df, df_sav)

    sections.render_sentiment_section(df_sav)
    sections.render_urgence_section(df_sav)
    sections.render_incident_top5_section(df_sav)
    sections.render_volume_day_week_section(df_sav)
    sections.render_volume_histograms_section(df_sav)
    sections.render_wordcloud_section(df_sav)
    sections.render_theme_incident_panel(df)
    sections.render_sentiment_theme(df)
    sections.render_claim_volume_section(df)
    sections.render_thematic_treemap_section(df_sav)

    if profil in {"Manager", "Data analyst"}:
        sections.render_response_time(df_sav, df_replies)

    sections.render_agent_focus(df_sav)
    sections.render_export_tools(df, df_sav)


if __name__ == "__main__":
    main()
