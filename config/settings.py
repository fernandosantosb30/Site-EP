import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    CANDIDATURE_URL = os.getenv(
        "CANDIDATURE_URL",
        ""
    )

    CANDIDATURE_EMAIL = os.getenv(
        "CANDIDATURE_EMAIL",
        ""
    )