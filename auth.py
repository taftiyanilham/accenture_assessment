from datetime import datetime
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db
from sql_models import TokenDB
from utils import get_token_from_header_or_cookie

fake_users_db = {"taftiyan": {"username": "taftiyan", "password": "pythondev"}}


class AuthService:
    def login(self, form_data, db: Session, response: Response):
        user = fake_users_db.get(form_data.username)
        if not user or user["password"] != form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_entry = TokenDB.create_token(user["username"])
        db.add(token_entry)
        db.commit()

        response.set_cookie(
            key="access_token",
            value=token_entry.token,
            httponly=True,
            secure=False,
            samesite="lax",
        )

        return {"access_token": token_entry.token, "token_type": "bearer"}

    def get_current_user(
        self,
        db: Session = Depends(get_db),
        token: str = Depends(get_token_from_header_or_cookie),
    ):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_entry = db.query(TokenDB).filter(TokenDB.token == token).first()
        if not token_entry or token_entry.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_entry.username
