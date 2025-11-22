from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS

from .metrics import compute_response_time, minutes_to_dhm
from .plots import (
    claim_distribution_pie,
    incident_distribution_main,
    incident_top5_bar,
    sentiment_by_theme,
    sentiment_pie,
    thematic_treemap,
    top_theme_bar,
    urgency_bar,
    volume_day_line,
    volume_dayofweek_bar,
    volume_hour_bar,
    volume_week_bar,
)


def render_header(profil: str):
    st.title("Analyse des tweets SAV Free")
    st.markdown(f"Vue actuelle : **{profil}** — tableau de bord filtré selon les options.")


def render_global_kpis(df: pd.DataFrame, df_sav: pd.DataFrame):
    st.subheader("Indicateurs généraux")
    col1, col2, col3 = st.columns(3)
    total_tweets = int(len(df))
    total_sav = int(df_sav["is_claim"].sum()) if not df_sav.empty else 0
    taux_sav = (total_sav / total_tweets * 100) if total_tweets else 0

    with col1:
        st.metric("Tweets analysés", f"{total_tweets:,}".replace(",", " "))
    with col2:
        st.metric("Tweets SAV (réclamations)", f"{total_sav:,}".replace(",", " "))
    with col3:
        st.metric("Part de tweets SAV", f"{taux_sav:.1f} %")
    st.caption("Ces KPI reflètent toujours la période et les filtres sélectionnés.")
    st.markdown("---")


def render_export_tools(df: pd.DataFrame, df_sav: pd.DataFrame):
    st.subheader("Export des données filtrées")
    if df.empty:
        st.info("Aucun tweet disponible pour l'export.")
        st.markdown("---")
        return
    col1, col2 = st.columns(2)
    csv_all = df.to_csv(index=False).encode("utf-8")
    with col1:
        st.download_button(
            "Exporter tous les tweets filtrés (CSV)",
            data=csv_all,
            file_name="tweets_free_filtres.csv",
            mime="text/csv",
        )
    with col2:
        csv_claims = df_sav.to_csv(index=False).encode("utf-8") if not df_sav.empty else b""
        st.download_button(
            "Exporter uniquement les réclamations (CSV)",
            data=csv_claims,
            file_name="tweets_reclamations_filtres.csv",
            mime="text/csv",
            disabled=df_sav.empty,
        )
    st.caption("Les exports sont synchronisés avec les filtres actifs (dates, thèmes, incidents…).")
    st.markdown("---")


def render_sentiment_section(df_sav: pd.DataFrame):
    st.subheader("Distribution des sentiments (tweets SAV)")
    fig = sentiment_pie(df_sav)
    if fig is None:
        st.info("Aucun tweet SAV pour calculer la répartition des sentiments.")
    else:
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


def render_urgence_section(df_sav: pd.DataFrame):
    st.subheader("Répartition des niveaux d'urgence (tweets SAV)")
    fig = urgency_bar(df_sav)
    if fig is None:
        st.info("Aucune réclamation pour afficher l'urgence.")
    else:
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


def render_claim_volume_section(df: pd.DataFrame):
    st.subheader("Nombre de Réclamation des tweets")
    fig = claim_distribution_pie(df)
    if fig is None:
        st.info("Aucune réclamation pour la période actuelle.")
    else:
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


def render_theme_incident_panel(df: pd.DataFrame):
    if df.empty:
        st.subheader("Distribution des Thèmes")
        st.info("Aucun tweet pour calculer les thématiques/incidents.")
        st.markdown("---")
        return
    fig_theme = top_theme_bar(df)
    fig_incident = incident_distribution_main(df)
    if fig_theme is None and fig_incident is None:
        st.subheader("Distribution des Thèmes")
        st.info("Impossible de calculer les thématiques/incidents.")
        st.markdown("---")
        return
    col_theme, col_incident = st.columns(2)
    with col_theme:
        st.subheader("Distribution des Thèmes")
        if fig_theme is None:
            st.info("Pas assez de données pour ce visuel.")
        else:
            st.plotly_chart(fig_theme, use_container_width=True)
    with col_incident:
        st.subheader("Distribution des Incidents")
        if fig_incident is None:
            st.info("Pas assez de données pour ce visuel.")
        else:
            st.plotly_chart(fig_incident, use_container_width=True)
    st.markdown("---")


def render_sentiment_theme(df: pd.DataFrame):
    st.subheader("Distribution des sentiments par thème")
    fig = sentiment_by_theme(df)
    if fig is None:
        st.info("Pas assez de données pour répartir les sentiments par thème.")
    else:
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


def render_response_time(df_sav: pd.DataFrame, df_replies: pd.DataFrame):
    st.subheader("Temps de réponse du SAV Free")
    if df_replies.empty or df_sav.empty:
        st.info("Impossible de calculer le temps de réponse (données manquantes).")
        st.markdown("---")
        return

    first_reply, mean_delay, median_delay = compute_response_time(df_sav, df_replies)
    if mean_delay is None:
        st.info("Aucune correspondance entre tweets clients et réponses Free.")
        st.markdown("---")
        return

    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        st.metric("Temps moyen de réponse", minutes_to_dhm(mean_delay))
    with col_tr2:
        st.metric("Temps médian de réponse", minutes_to_dhm(median_delay))

    with st.expander("Voir quelques exemples de délais de réponse"):
        df_display = first_reply[
            ["in_reply_to", "created_at_client", "created_at_reply", "delay_minutes"]
        ].copy()
        df_display["Délai"] = df_display["delay_minutes"].apply(minutes_to_dhm)
        df_display = df_display.drop(columns=["delay_minutes"])
        df_display = df_display.rename(
            columns={
                "in_reply_to": "Tweet client (ID)",
                "created_at_client": "Date tweet client",
                "created_at_reply": "Date réponse Free",
            }
        )
        st.dataframe(df_display, use_container_width=True)
    st.markdown("---")


def render_agent_focus(df_sav: pd.DataFrame):
    st.subheader("File priorisée (vue Agent SAV)")
    if df_sav.empty:
        st.info("Aucune réclamation à prioriser.")
        st.markdown("---")
        return
    priority_map = {"haute": 2, "moyenne": 1, "basse": 0}
    prioritized = df_sav.copy()
    prioritized["urgence_score"] = prioritized["urgence"].map(priority_map).fillna(-1)
    prioritized = (
        prioritized.sort_values(
            by=["urgence_score", "engagement"],
            ascending=[False, False],
        )
        .head(20)
    )
    cols = [
        "id",
        "created_at",
        "topic_main",
        "sentiment",
        "urgence",
        "incident",
        "engagement",
        "urgence_score",
    ]
    subset = prioritized[cols].drop(columns=["urgence_score"])
    st.dataframe(subset, use_container_width=True)
    st.caption("Top 20 réclamations classées par urgence et engagement.")
    st.markdown("---")


def render_incident_top5_section(df_sav: pd.DataFrame):
    """Affiche le Top 5 des incidents"""
    st.subheader("Top 5 des incidents")
    fig = incident_top5_bar(df_sav)
    if fig is None:
        st.info("Aucune réclamation pour afficher les incidents.")
    else:
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


def render_volume_day_week_section(df_sav: pd.DataFrame):
    """Affiche le volume quotidien et hebdomadaire des tweets SAV"""
    st.subheader("Volume de tweets SAV par jour et par semaine")
    if df_sav.empty:
        st.info("Aucun tweet SAV sur la période sélectionnée.")
        st.markdown("---")
        return
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        fig_vol_jour = volume_day_line(df_sav)
        if fig_vol_jour is None:
            st.info("Pas de données pour le volume quotidien.")
        else:
            st.plotly_chart(fig_vol_jour, use_container_width=True)
    
    with col_v2:
        fig_vol_semaine = volume_week_bar(df_sav)
        if fig_vol_semaine is None:
            st.info("Pas de données pour le volume hebdomadaire.")
        else:
            st.plotly_chart(fig_vol_semaine, use_container_width=True)
    
    st.markdown("---")


def render_volume_histograms_section(df_sav: pd.DataFrame):
    """Affiche les histogrammes de volume par heure et par jour de la semaine"""
    st.subheader("Histogrammes de volume des tweets SAV")
    if df_sav.empty:
        st.info("Aucun tweet SAV pour afficher les histogrammes de volume.")
        st.markdown("---")
        return
    
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        fig_hour = volume_hour_bar(df_sav)
        if fig_hour is None:
            st.info("Pas de données pour le volume par heure.")
        else:
            st.plotly_chart(fig_hour, use_container_width=True)
    
    with col_h2:
        fig_dow = volume_dayofweek_bar(df_sav)
        if fig_dow is None:
            st.info("Pas de données pour le volume par jour de la semaine.")
        else:
            st.plotly_chart(fig_dow, use_container_width=True)
    
    st.markdown("---")


def render_wordcloud_section(df_sav: pd.DataFrame):
    """Affiche le nuage de mots pour les tweets SAV négatifs"""
    st.subheader("Nuage de mots — tweets SAV négatifs")
    
    if df_sav.empty:
        st.info("Aucun tweet SAV pour afficher un nuage de mots.")
        st.markdown("---")
        return
    
    df_neg = df_sav[df_sav["sentiment"] == "neg"]
    
    if "full_text" not in df_neg.columns or df_neg["full_text"].dropna().empty:
        st.info("La colonne 'full_text' est absente ou vide, impossible de générer un nuage de mots.")
        st.markdown("---")
        return
    
    texte_neg = " ".join(df_neg["full_text"].dropna().astype(str)).lower()
    
    if not texte_neg.strip():
        st.info("Pas assez de texte pour générer un nuage de mots négatifs.")
        st.markdown("---")
        return
    
    stopwords = set(STOPWORDS)
    
    # Stopwords FR à exclure du nuage
    french_stopwords = {
        "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles",
        "me", "moi", "toi", "lui", "leur", "leurs", "se", "ses", "son", "sa",
        "mon", "ma", "mes", "tes", "notre", "nos", "votre", "vos",
        "de", "du", "des", "le", "la", "les", "un", "une", "au", "aux",
        "et", "ou", "où", "mais", "donc", "or", "ni", "car", "n", "depuis", "ai",
        "à", "en", "dans", "sur", "sous", "chez", "par", "pour", "avec", "sans",
        "ne", "pas", "plus", "moins", "rien", "tout", "tous", "toutes", "aucun",
        "ce", "cet", "cette", "ces", "ça", "cela", "c'", "qu'", "que", "qui",
        "quand", "comme", "si", "bien", "très", "trop", "alors", "d", "j'ai",
        "être", "avoir", "fait", "faire", "est", "j", "co", "t", "c'est", "c", ".", "suis",
        # mots peu utiles dans les tweets
        "rt", "https", "http", "www", "com",
        "bonjour", "bonsoir", "merci", "svp",
        "free", "freebox", "freemobile", "free_1337"  # ça pollue trop
    }
    
    stopwords.update(french_stopwords)
    
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=stopwords,
        collocations=False
    ).generate(texte_neg)
    
    fig_wc, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    
    st.pyplot(fig_wc)
    st.markdown("---")


def render_thematic_treemap_section(df_sav: pd.DataFrame):
    """Affiche la cartographie thématique des types de souci"""
    st.subheader("Cartographie thématique des types de souci")
    
    if df_sav.empty:
        st.info("Aucun tweet SAV pour afficher la cartographie thématique.")
        st.markdown("---")
        return
    
    # Vérifier que les colonnes existent
    required_cols = ["incident", "topic_main"]
    if not all(col in df_sav.columns for col in required_cols):
        st.info("Pas assez de données (incident / topic) pour construire la cartographie.")
        st.markdown("---")
        return
    
    df_them = df_sav.dropna(subset=required_cols).copy()
    
    if df_them.empty:
        st.info("Pas assez de données (incident / topic) pour construire la cartographie.")
        st.markdown("---")
        return
    
    fig = thematic_treemap(df_sav)
    if fig is None:
        st.info("Pas assez de données pour construire la cartographie.")
    else:
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

