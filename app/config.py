import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "sigmon-dev-secret")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    APP_NAME = "SIGMon"

    # Futuro PostgreSQL:
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # MIGRATIONS_DIR = "migrations/"
