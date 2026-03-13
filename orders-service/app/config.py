import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://lirio:lirio_pass@db-orders:5432/orders_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
