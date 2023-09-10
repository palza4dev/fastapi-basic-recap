from datetime import datetime, timedelta

import bcrypt
from jose import jwt


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "59ba8dc81f232c39e85758eb38cd708a6e2d004e716ef994deca863d843fffbf"
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str):
        byte_password = plain_password.encode(self.encoding)
        hashed_password: bytes = bcrypt.hashpw(byte_password, salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:

        return bcrypt.checkpw(
            plain_password.encode(self.encoding), hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,  # sub -> unique id
                "exp": datetime.now() + timedelta(days=1),
            },
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # expire check
        return payload["sub"]
