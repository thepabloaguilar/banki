from typing import Final

from pydantic import BaseSettings, EmailStr


class _Settings(BaseSettings):
    PROJECT_NAME: str = 'banki'
    PROJECT_DESCRIPTION: str = 'Charges API'
    DEBUG: bool = False
    SQLALCHEMY_DB_URI: str = 'postgresql+psycopg2://user:password@localhost:6000/banki'
    SQLALCHEMY_ECHO: bool = True

    # Email Configuration
    MAIL_USERNAME: str = 'contact@banki.com'
    MAIL_PASSWORD: str = ''
    MAIL_PORT: int = 7000
    MAIL_SERVER: str = 'localhost'
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = False
    MAIL_FROM: EmailStr = 'contact@banki.com'  # type: ignore[assignment]
    USE_CREDENTIALS: bool = False
    VALIDATE_CERTS: bool = False

    class Config:  # noqa: WPS431
        case_sensitive = True


settings: Final = _Settings()
