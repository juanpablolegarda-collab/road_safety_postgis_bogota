from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


PROJECT_DIR = Path(__file__).resolve().parents[1]

SQL_FILES = [
    PROJECT_DIR / "sql" / "04_spatial_analysis.sql",
    PROJECT_DIR / "sql" / "05_risk_indicators.sql",
]


def create_db_engine():
    env_path = PROJECT_DIR / ".env"
    load_dotenv(env_path)

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(db_url)


def run_sql_file(connection, sql_file):
    print(f"\nExecuting SQL file: {sql_file.name}")

    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    sql_script = sql_file.read_text(encoding="utf-8")

    connection.exec_driver_sql(sql_script)

    print(f"Completed: {sql_file.name}")


def main():
    print("=" * 80)
    print("RUN SQL ANALYSIS VIEWS")
    print("=" * 80)

    engine = create_db_engine()

    with engine.begin() as connection:
        for sql_file in SQL_FILES:
            run_sql_file(connection, sql_file)

    print("\n" + "=" * 80)
    print("SQL VIEWS CREATED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()