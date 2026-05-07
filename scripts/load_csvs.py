"""Bulk-load raw CSVs into the raw_app schema.

Idempotent — each target table is dropped and recreated on every run.
Intended for local dev and ephemeral seeding only; not for production
incremental loads.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Fail loudly at startup if any required env var is missing.
DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
    f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}"
    f"/{os.environ['POSTGRES_DB']}"
)

CSV_TO_TABLE = {
    "raw_customers.csv": "customers",
    "raw_plans.csv": "plans",
    "raw_subscriptions.csv": "subscriptions",
    "raw_events.csv": "events",
}


def main() -> None:
    engine = create_engine(DATABASE_URL)
    data_dir = PROJECT_ROOT / "data"

    for csv_filename, table_name in CSV_TO_TABLE.items():
        csv_path = data_dir / csv_filename
        if not csv_path.exists():
            print(f"[skip] {csv_path} not found")
            continue

        df = pd.read_csv(csv_path)
        # method="multi" batches INSERTs into one statement per chunk,
        # roughly 10x faster than the default row-at-a-time mode.
        df.to_sql(
            name=table_name,
            con=engine,
            schema="raw_app",
            if_exists="replace",
            index=False,
            method="multi",
        )
        print(f"[ok] {csv_filename} -> raw_app.{table_name} ({len(df)} rows)")


if __name__ == "__main__":
    main()