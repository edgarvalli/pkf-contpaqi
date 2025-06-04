import hashlib

def encrypt_password(password: str) -> str:
    """
    Encrypts a password using SHA-256 hashing algorithm.

    Args:
        password (str): The password to encrypt.

    Returns:
        str: The encrypted password in hexadecimal format.
    """
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return encrypt_password(password) == hashed_password