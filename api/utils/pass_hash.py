import bcrypt

def hash_password(password: str) -> str:
    """Hash a password securely using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")  # Store as string

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches the stored hashed password."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

