import bcrypt


class UserService:
    encoding: str = "UTF-8"

    def hash_password(self, plain_password: str):
        byte_password = plain_password.encode(self.encoding)
        hashed_password: bytes = bcrypt.hashpw(byte_password, salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)