"""Validate and import CSV files into the PostgreSQL schema."""
from pathlib import Path
import pandas as pd
from sqlalchemy import text
from db_config import get_engine

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

IMPORT_ORDER = [
    ("categories", ["category_id", "name"]),
    ("authors", ["author_id", "full_name"]),
    ("users", ["user_id", "full_name", "email"]),
    ("books", ["book_id", "title", "isbn", "publication_year", "category_id"]),
    ("book_authors", ["book_id", "author_id"]),
]


def load_and_check(table_name: str, expected_columns: list[str]) -> pd.DataFrame:
    csv_path = DATA_DIR / f"{table_name}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")

    df = pd.read_csv(csv_path, encoding="utf-8")
    actual_columns = list(df.columns)
    if actual_columns != expected_columns:
        raise ValueError(
            f"Column mismatch in {csv_path.name}: expected {expected_columns}, got {actual_columns}"
        )

    if df.isna().any().any():
        raise ValueError(f"Null values found in {csv_path.name}")

    return df


def main() -> None:
    frames = {
        table_name: load_and_check(table_name, columns)
        for table_name, columns in IMPORT_ORDER
    }

    engine = get_engine()
    with engine.begin() as connection:
        for table_name, _ in IMPORT_ORDER:
            df = frames[table_name]
            df.to_sql(
                table_name,
                connection,
                if_exists="append",
                index=False,
                method="multi",
            )
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar_one()
            print(f"Imported {len(df)} rows into {table_name} (total now: {count})")

    print("Import completed successfully.")


if __name__ == "__main__":
    main()