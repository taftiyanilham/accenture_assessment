# models_sql.py
from sqlalchemy import Column, Integer, String, Date, DateTime
from database import Base
from datetime import datetime, timedelta


class TokenDB(Base):
    __tablename__ = "tokens"

    token = Column(String, primary_key=True, index=True, unique=True)
    username = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    @staticmethod
    def create_token(username: str, lifetime_minutes: int = 60):
        import secrets

        token_value = secrets.token_urlsafe(32)  # random string
        expiry = datetime.utcnow() + timedelta(minutes=lifetime_minutes)
        return TokenDB(token=token_value, username=username, expires_at=expiry)


class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # PK auto
    book_title = Column(String, unique=True, index=True, nullable=False)  # unik
    author = Column(String, nullable=False)
    publish_date = Column(Date, nullable=False)
