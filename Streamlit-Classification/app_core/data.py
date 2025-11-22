from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import streamlit as st

from .config import (
    ENGAGEMENT_COLUMNS,
    REQUIRED_COLUMNS,
    SAMPLE_CLIENTS_PATH,
)


def _validate_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(
            "Colonnes obligatoires manquantes : "
            + ", ".join(f"`{col}`" for col in missing)
        )
        st.stop()


def _ensure_engagement_columns(df: pd.DataFrame) -> None:
    for col in ENGAGEMENT_COLUMNS:
        if col not in df.columns:
            df[col] = 0


def _prepare_clients_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()
    _validate_columns(df)

    created = pd.to_datetime(df["created_at"].astype(str), errors="coerce", utc=True)
    if created.isna().all():
        st.error("Impossible de parser les dates de 'created_at'. Vérifie le format.")
        st.stop()

    df["created_at"] = created
    df["date"] = created.dt.date
    df["week"] = created.dt.to_period("W").apply(lambda r: r.start_time.date())
    df["day_of_week"] = created.dt.day_name()
    df["hour"] = created.dt.hour

    if "topics" in df.columns:
        df["topic_main"] = df["topics"].astype(str).str.extract(r"\['?(.*?)'?\]")[0]
    else:
        df["topic_main"] = None

    _ensure_engagement_columns(df)
    df["engagement"] = (
        df["favorite_count"]
        + df["retweet_count"]
        + df.get("reply_count", 0)
        + df.get("quote_count", 0)
    )

    df["id"] = df["id"].astype(str)
    return df


def _read_csv(source: Path | str | Iterable[str]):
    return pd.read_csv(source, encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_clients(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return pd.DataFrame()
    df = pd.read_csv(uploaded_file, encoding="utf-8")
    return _prepare_clients_df(df)


@st.cache_data(show_spinner=False)
def load_clients_from_path(path: Path = SAMPLE_CLIENTS_PATH) -> pd.DataFrame:
    if not path.exists():
        st.error(f"Fichier échantillon introuvable : {path}")
        st.stop()
    df = pd.read_csv(path, encoding="utf-8")
    return _prepare_clients_df(df)


@st.cache_data(show_spinner=False)
def load_replies(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, encoding="utf-8")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
    df["id"] = df["id"].astype(str)
    if "in_reply_to" in df.columns:
        df["in_reply_to"] = df["in_reply_to"].astype(str)
        df = df[~df["in_reply_to"].isna()]
    return df


def has_sample_data(path: Optional[Path] = None) -> bool:
    target = path or SAMPLE_CLIENTS_PATH
    return target.exists()

