"""Run sample validation checks against the PostgreSQL book database."""
from sqlalchemy import text
from db_config import get_engine

EXPECTED_COUNTS = {
    "categories": 3,
    "authors": 5,
    "users": 2,
    "books": 4,
    "book_authors": 5,
}


def main() -> None:
    engine = get_engine()
    with engine.connect() as connection:
        for table_name, expected in EXPECTED_COUNTS.items():
            actual = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar_one()
            print(f"{table_name}: {actual} rows (expected {expected})")
            if actual != expected:
                raise AssertionError(f"Unexpected count in {table_name}")

        joined_rows = connection.execute(
            text(
                """
                SELECT b.title, c.name AS category_name, a.full_name AS author_name
                FROM books AS b
                JOIN categories AS c ON b.category_id = c.category_id
                JOIN book_authors AS ba ON b.book_id = ba.book_id
                JOIN authors AS a ON ba.author_id = a.author_id
                ORDER BY b.book_id, a.author_id
                """
            )
        ).all()

        print(f"Joined book-author-category rows: {len(joined_rows)}")
        for title, category_name, author_name in joined_rows:
            print(f"  - {title} | {category_name} | {author_name}")

    print("All sample checks passed.")


if __name__ == "__main__":
    main()