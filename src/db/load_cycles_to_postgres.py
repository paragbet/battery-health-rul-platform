# Load processed NASA battery cycle data into PostgreSQL

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine


# Path to processed combined CSV
CSV_FILE = Path("data/processed/all_batteries_cycles.csv")

# PostgreSQL connection details
DB_USER = "battery_user"
DB_PASSWORD = "battery_pass"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "battery_db"

# Table name
TABLE_NAME = "battery_cycles"


def load_csv_to_postgres():
    """
    Read processed CSV and load it into PostgreSQL.
    """

    # Read CSV file
    df = pd.read_csv(CSV_FILE)

    # Create database connection
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Load data into PostgreSQL table
    # if_exists="replace" means old table will be replaced
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    print("Data loaded successfully into PostgreSQL!")
    print(f"Table name: {TABLE_NAME}")
    print(f"Rows loaded: {len(df)}")


if __name__ == "__main__":
    load_csv_to_postgres()