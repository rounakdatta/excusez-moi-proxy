import os

class DatabaseConfig:
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")

    # we're using asyncpg as the DB client, hence the notation
    db_config_urn = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

db_config = DatabaseConfig()
