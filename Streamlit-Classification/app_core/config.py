from __future__ import annotations

from pathlib import Path

# ==========================
# Directories & data files
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
REPLIES_CSV_PATH = DATA_DIR / "reponses_free.csv"
SAMPLE_CLIENTS_PATH = DATA_DIR / "sample_clients.csv"


# ==========================
# UI constants
# ==========================
FREE_PRIMARY = "#E60000"
FREE_SECONDARY = "#FF7043"
FREE_DARK = "#B71C1C"
FREE_SENTIMENT_MAP = {
    "neg": FREE_PRIMARY,
    "neu": "#FFB300",
    "pos": "#4CAF50",
}
FREE_URGENCE_MAP = {
    "basse": "#4CAF50",
    "moyenne": "#FFB300",
    "haute": FREE_PRIMARY,
}
FREE_HEATMAP = ["#FFE5E5", "#FF9999", FREE_PRIMARY, "#8B0000"]

THEME = {
    "primaryColor": FREE_PRIMARY,
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F6F6F9",
    "textColor": "#111111",
    "font": "Poppins",
}

PROFILES = ["Manager", "Data analyst", "Agent SAV"]


# ==========================
# Data validation
# ==========================
REQUIRED_COLUMNS = [
    "id",
    "created_at",
    "topics",
    "sentiment",
    "urgence",
    "incident",
    "is_claim",
]

ENGAGEMENT_COLUMNS = [
    "favorite_count",
    "retweet_count",
    "reply_count",
    "quote_count",
]





