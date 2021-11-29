from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password_or_key(plain_password_or_key, hashed_password_or_key):
    return pwd_context.verify(plain_password_or_key, hashed_password_or_key)


def get_password_or_key_hash(password_or_key):
    return pwd_context.hash(password_or_key)
