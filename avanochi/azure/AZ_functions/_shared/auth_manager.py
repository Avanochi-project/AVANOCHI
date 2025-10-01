# _shared/auth_service.py

import os
import jwt
import datetime
from jwt import PyJWTError

class AuthManager:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET", "dev-secret")  # en Azure -> App Setting
        self.algorithm = "HS256"
        self.exp_minutes = int(os.getenv("JWT_EXP_MINUTES", "60"))

    def generate_token(self, user_id: str) -> str:
        now = datetime.datetime.utcnow()
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + datetime.timedelta(minutes=self.exp_minutes)
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return {"valid": True, "user_id": payload.get("sub")}
        except PyJWTError as e:
            return {"valid": False, "error": str(e)}
