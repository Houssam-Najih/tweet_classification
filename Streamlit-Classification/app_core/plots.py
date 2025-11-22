from __future__ import annotations

import pandas as pd
import plotly.express as px

from .config import FREE_PRIMARY, FREE_SENTIMENT_MAP, FREE_URGENCE_MAP


THEME_SCALE = ["#36010E", "#5A0617", "#7E0C1F", "#A11326", "#C81F2E", "#E23A3C", "#F1644C", "#F99A6A", "#FEC4A0"]
INCIDENT_COLORS = {
    "aucun": "#1EA64B",
    "information": "#10A0C4",
    "technique": "#E01717",
    "incident_reseau": "#CC0000",
    "processus_sav": "#B30000",
    "facturation": "#F07818",
    "livraison": "#F44336",
}
SENTIMENT_LABELS = {"neg": "Négatif", "neu": "Neutre", "pos": "Positif"}
SENTIMENT_COLOR_MAP = {
    SENTIMENT_LABELS[key]: value for key, value in FREE_SENTIMENT_MAP.items()
}


def apply_free_layout(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(family="Poppins, sans-serif"),
    )
    return fig


def _prepare_counts(df: pd.DataFrame, column: str, top_n: int | None = None):
    if column not in df.columns:
        return pd.DataFrame()
    temp = df.copy()
    temp[column] = temp[column].fillna("Non renseigné")
    counts = (
        temp.groupby(column)["id"]
        .count()
        .reset_index(name="nb")
        .sort_values("nb", ascending=False)
    )
    if top_n:
        counts = counts.head(top_n)
    total = counts["nb"].sum()
    if total:
        counts["pct"] = (counts["nb"] / total * 100).round(2)
        counts["label"] = counts.apply(lambda r: f"{int(r['nb'])} ({r['pct']:.2f}%)", axis=1)
    else:
        counts["pct"] = 0
        counts["label"] = counts["nb"]
    return counts


def sentiment_pie(df_sav: pd.DataFrame):
    if df_sav.empty:
        return None
    sent_counts = _prepare_counts(df_sav, "sentiment")
    if sent_counts.empty:
        return None
    sent_counts["sentiment_label"] = sent_counts["sentiment"].map(
        SENTIMENT_LABELS
    ).fillna(sent_counts["sentiment"])
    fig = px.pie(
        sent_counts,
        names="sentiment_label",
        values="nb",
        title="Distribution des sentiments",
        color="sentiment_label",
        color_discrete_map=SENTIMENT_COLOR_MAP,
        hole=0.55,
    )
    fig.update_traces(textposition="inside", textinfo="label+percent", pull=0.02)
    return apply_free_layout(fig)


def urgency_bar(df_sav: pd.DataFrame):
    if df_sav.empty:
        return None
    urg_counts = _prepare_counts(df_sav, "urgence")
    fig = px.bar(
        urg_counts,
        x="urgence",
        y="nb",
        color="urgence",
        color_discrete_map=FREE_URGENCE_MAP,
        title="Tweets SAV par niveau d'urgence",
        labels={"urgence": "Niveau d'urgence", "nb": "Tweets SAV"},
        text="label",
    )
    fig.update_traces(marker_line=dict(width=0), hovertemplate="%{x}: %{customdata[0]} tweets<extra></extra>", customdata=urg_counts[["nb"]])
    return apply_free_layout(fig)


def incident_top_modern(df: pd.DataFrame, top_n: int = 10):
    if df.empty:
        return None
    inc_counts = _prepare_counts(df, "incident", top_n)
    if inc_counts.empty:
        return None
    fig = px.bar(
        inc_counts,
        x="incident",
        y="nb",
        color="nb",
        color_continuous_scale=THEME_SCALE,
        title=f"Top {top_n} incidents",
        labels={"incident": "Type d'incident", "nb": "Tweets"},
        text="label",
    )
    fig.update_traces(marker_line=dict(width=0), hovertemplate="%{x}<br>Tweets: %{y}<extra></extra>")
    return apply_free_layout(fig)


def incident_distribution_main(df: pd.DataFrame):
    if df.empty:
        return None
    inc_counts = _prepare_counts(df, "incident")
    if inc_counts.empty:
        return None
    fig = px.bar(
        inc_counts,
        x="nb",
        y="incident",
        orientation="h",
        color="incident",
        color_discrete_map={**INCIDENT_COLORS},
        labels={"incident": "Type d'incident", "nb": "Nombre de tweets"},
        title="Distribution des incidents principaux",
        text="label",
    )
    fig.update_traces(marker_line=dict(width=0))
    fig.update_yaxes(categoryorder="total ascending")
    return apply_free_layout(fig)


def volume_line(df: pd.DataFrame):
    if df.empty:
        return None
    volume_jour = (
        df.groupby("date")["id"]
        .count()
        .reset_index(name="nb_tweets")
        .sort_values("date")
    )
    fig = px.bar(
        volume_jour,
        x="date",
        y="nb_tweets",
        color="nb_tweets",
        color_continuous_scale=THEME_SCALE,
        title="Volume de tweets Free par jour",
        labels={"date": "Date", "nb_tweets": "Tweets"},
        text_auto=True,
    )
    fig.update_traces(marker_line=dict(width=0))
    return apply_free_layout(fig)


def top_theme_bar(df: pd.DataFrame, top_n: int = 10):
    if df.empty:
        return None
    theme_counts = _prepare_counts(df, "topic_main", top_n)
    if theme_counts.empty:
        return None
    fig = px.bar(
        theme_counts,
        x="topic_main",
        y="nb",
        color="nb",
        color_continuous_scale=THEME_SCALE,
        title="Top 10 Thème principal",
        labels={"topic_main": "Thème principal", "nb": "Nombre de tweets"},
        text="label",
    )
    fig.update_traces(marker_line=dict(width=0))
    return apply_free_layout(fig)


def sentiment_by_theme(df: pd.DataFrame, top_n: int = 6):
    if df.empty:
        return None
    temp = df.copy()
    temp["topic_main"] = temp["topic_main"].fillna("Non renseigné")
    counts = (
        temp.groupby(["topic_main", "sentiment"])["id"]
        .count()
        .reset_index(name="nb")
        .sort_values("nb", ascending=False)
    )
    top_topics = (
        counts.groupby("topic_main")["nb"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .index.tolist()
    )
    filtered = counts[counts["topic_main"].isin(top_topics)]
    if filtered.empty:
        return None
    filtered["topic_main"] = filtered["topic_main"].fillna("Non renseigné")
    fig = px.bar(
        filtered,
        x="topic_main",
        y="nb",
        color="sentiment",
        color_discrete_map=FREE_SENTIMENT_MAP,
        title="Distribution des sentiments par thème",
        labels={"topic_main": "Thème", "nb": "Tweets"},
        text_auto=True,
    )
    fig.update_layout(barmode="stack")
    return apply_free_layout(fig)


def claim_distribution_pie(df: pd.DataFrame):
    if df.empty:
        return None
    claims = df[df["is_claim"] == 1]
    if claims.empty:
        return None
    counts = _prepare_counts(claims, "incident")
    if counts.empty:
        return None
    fig = px.pie(
        counts,
        names="incident",
        values="nb",
        title="Nombre de Réclamation des tweets",
        color="incident",
        color_discrete_sequence=THEME_SCALE,
    )
    fig.update_traces(textinfo="label+percent", pull=0.04)
    return apply_free_layout(fig)


def volume_day_line(df_sav: pd.DataFrame):
    """Volume quotidien de tweets SAV (graphique en ligne)"""
    if df_sav.empty:
        return None
    volume_jour = (
        df_sav.groupby("date")["id"]
        .count()
        .reset_index(name="nb_tweets")
        .sort_values("date")
    )
    fig = px.line(
        volume_jour,
        x="date",
        y="nb_tweets",
        title="Volume quotidien de tweets SAV",
        labels={"date": "Date", "nb_tweets": "Tweets SAV"},
        markers=True,
        color_discrete_sequence=[FREE_PRIMARY],
    )
    return apply_free_layout(fig)


def volume_week_bar(df_sav: pd.DataFrame):
    """Volume hebdomadaire de tweets SAV (graphique en barres)"""
    if df_sav.empty:
        return None
    volume_semaine = (
        df_sav.groupby("week")["id"]
        .count()
        .reset_index(name="nb_tweets")
        .sort_values("week")
    )
    fig = px.bar(
        volume_semaine,
        x="week",
        y="nb_tweets",
        title="Volume hebdomadaire de tweets SAV",
        labels={"week": "Semaine (lundi)", "nb_tweets": "Tweets SAV"},
        color_discrete_sequence=[FREE_PRIMARY],
    )
    return apply_free_layout(fig)


def volume_hour_bar(df_sav: pd.DataFrame):
    """Volume de tweets SAV par heure"""
    if df_sav.empty:
        return None
    vol_hour = (
        df_sav.groupby("hour")["id"]
        .count()
        .reset_index(name="nb_tweets")
        .sort_values("hour")
    )
    fig = px.bar(
        vol_hour,
        x="hour",
        y="nb_tweets",
        title="Volume de tweets SAV par heure",
        labels={"hour": "Heure", "nb_tweets": "Tweets SAV"},
        color_discrete_sequence=[FREE_PRIMARY],
    )
    return apply_free_layout(fig)


def volume_dayofweek_bar(df_sav: pd.DataFrame):
    """Volume de tweets SAV par jour de la semaine"""
    if df_sav.empty:
        return None
    vol_dow = (
        df_sav.groupby("day_of_week")["id"]
        .count()
        .reset_index(name="nb_tweets")
    )
    
    order_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    vol_dow["day_of_week"] = pd.Categorical(
        vol_dow["day_of_week"],
        categories=order_days,
        ordered=True
    )
    vol_dow = vol_dow.sort_values("day_of_week")
    
    fig = px.bar(
        vol_dow,
        x="day_of_week",
        y="nb_tweets",
        title="Volume de tweets SAV par jour de la semaine",
        labels={"day_of_week": "Jour", "nb_tweets": "Tweets SAV"},
        color_discrete_sequence=[FREE_PRIMARY],
    )
    return apply_free_layout(fig)


def incident_top5_bar(df_sav: pd.DataFrame):
    """Top 5 des incidents les plus fréquents"""
    if df_sav.empty:
        return None
    inc_counts = (
        df_sav.groupby("incident")["id"]
        .count()
        .reset_index(name="nb")
        .sort_values("nb", ascending=False)
        .head(5)
    )
    fig = px.bar(
        inc_counts,
        x="incident",
        y="nb",
        title="Top 5 incidents les plus fréquents",
        labels={"incident": "Incident", "nb": "Tweets SAV"},
        color_discrete_sequence=[FREE_PRIMARY],
    )
    return apply_free_layout(fig)


def thematic_treemap(df_sav: pd.DataFrame):
    """Cartographie thématique des types de souci (treemap)"""
    if df_sav.empty:
        return None
    # Vérifier que les colonnes existent
    required_cols = ["incident", "topic_main"]
    if not all(col in df_sav.columns for col in required_cols):
        return None
    df_them = df_sav.dropna(subset=required_cols).copy()
    if df_them.empty:
        return None
    df_them_grp = (
        df_them
        .groupby(["incident", "topic_main"])["id"]
        .count()
        .reset_index(name="nb_tweets")
    )
    fig = px.treemap(
        df_them_grp,
        path=["incident", "topic_main"],
        values="nb_tweets",
        title="Cartographie des incidents par thème (nombre de tweets SAV)",
    )
    return apply_free_layout(fig)

