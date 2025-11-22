from __future__ import annotations

import pandas as pd


def compute_response_time(
    df_clients: pd.DataFrame, df_replies: pd.DataFrame
):
    if df_clients.empty or df_replies.empty:
        return None, None, None

    df_clients = df_clients.copy()
    df_replies = df_replies.copy()

    df_clients["id"] = df_clients["id"].astype(str)
    if "in_reply_to" not in df_replies.columns:
        return None, None, None

    df_replies["in_reply_to"] = df_replies["in_reply_to"].astype(str)

    client_ids = df_clients["id"].unique()
    rep = df_replies[df_replies["in_reply_to"].isin(client_ids)].copy()
    if rep.empty:
        return None, None, None

    merged = rep.merge(
        df_clients[["id", "created_at"]],
        left_on="in_reply_to",
        right_on="id",
        suffixes=("_reply", "_client"),
    )

    merged["created_at_reply"] = pd.to_datetime(
        merged["created_at_reply"], errors="coerce"
    )
    merged["created_at_client"] = pd.to_datetime(
        merged["created_at_client"], errors="coerce"
    )
    merged = merged.dropna(subset=["created_at_reply", "created_at_client"])
    if merged.empty:
        return None, None, None

    merged["delay_minutes"] = (
        merged["created_at_reply"] - merged["created_at_client"]
    ).dt.total_seconds() / 60
    merged = merged[merged["delay_minutes"] >= 0]
    if merged.empty:
        return None, None, None

    first_reply = (
        merged.sort_values("delay_minutes")
        .groupby("in_reply_to")
        .first()
        .reset_index()
    )

    mean_delay = first_reply["delay_minutes"].mean()
    median_delay = first_reply["delay_minutes"].median()
    return first_reply, mean_delay, median_delay


def minutes_to_dhm(minutes):
    if minutes is None:
        return "N/A"
    total_minutes = int(round(minutes))
    days = total_minutes // (24 * 60)
    remaining = total_minutes % (24 * 60)
    hours = remaining // 60
    mins = remaining % 60

    parts = []
    if days:
        parts.append(f"{days} jour{'s' if days > 1 else ''}")
    if hours:
        parts.append(f"{hours} h")
    if mins or not parts:
        parts.append(f"{mins} min")
    return " ".join(parts)





