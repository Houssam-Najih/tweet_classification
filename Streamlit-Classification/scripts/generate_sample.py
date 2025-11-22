from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

KEEP_COLUMNS = [
    "id",
    "created_at",
    "topics",
    "sentiment",
    "urgence",
    "incident",
    "is_claim",
    "favorite_count",
    "retweet_count",
    "reply_count",
    "quote_count",
    "full_text",
    "text_clean",
    "lang",
]


def _ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for engagement_col in ("favorite_count", "retweet_count", "quote_count", "reply_count"):
        if engagement_col not in df.columns:
            df[engagement_col] = 0
    if "lang" not in df.columns:
        df["lang"] = "fr"
    return df


def build_sample(source: Path, dest: Path, rows: int, seed: int) -> None:
    df = pd.read_csv(source)
    df = _ensure_columns(df)

    claims = df[df["is_claim"] == 1]
    non_claims = df[df["is_claim"] == 0]

    total = min(rows, len(df))
    claim_target = min(len(claims), max(1, total // 2))
    non_claim_target = min(len(non_claims), total - claim_target)
    remainder = total - (claim_target + non_claim_target)
    if remainder > 0 and len(non_claims) - non_claim_target > len(claims) - claim_target:
        non_claim_target = min(len(non_claims), non_claim_target + remainder)
    else:
        claim_target = min(len(claims), claim_target + remainder)

    samples = []
    if claim_target:
        samples.append(claims.sample(claim_target, random_state=seed))
    if non_claim_target:
        samples.append(non_claims.sample(non_claim_target, random_state=seed + 1))

    sample_df = pd.concat(samples, ignore_index=True)
    sample_df = sample_df.sort_values("created_at")
    available_cols = [col for col in KEEP_COLUMNS if col in sample_df.columns]
    sample_df = sample_df[available_cols]

    dest.parent.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(dest, index=False)
    print(f"[generate_sample] wrote {len(sample_df)} rows to {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a lightweight sample CSV.")
    parser.add_argument("--source", type=Path, required=True, help="Path to the full dataset CSV.")
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("Data/sample_clients.csv"),
        help="Path for the generated sample CSV.",
    )
    parser.add_argument("--rows", type=int, default=400, help="Maximum number of rows to keep in the sample.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    args = parser.parse_args()

    build_sample(args.source, args.dest, args.rows, args.seed)


if __name__ == "__main__":
    main()


