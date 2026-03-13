import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://lirio:lirio_pass@db-products:5432/products_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
