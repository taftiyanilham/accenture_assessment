from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user database
fake_users_db = {
    "taftiyan": {
        "username": "taftiyan",
        "password": "pythondev",
    }
}

active_tokens = {}


class AuthService:
    def login(self, form_data: OAuth2PasswordRequestForm):
        user = fake_users_db.get(form_data.username)
        if not user or user["password"] != form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = f"token-{user['username']}"
        active_tokens[token] = user["username"]
        return {"access_token": token, "token_type": "bearer"}

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        username = active_tokens.get(token)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
