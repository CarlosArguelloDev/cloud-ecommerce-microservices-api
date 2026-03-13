import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://lirio:lirio_pass@db-payments:5432/payments_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
