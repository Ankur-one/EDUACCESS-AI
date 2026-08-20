import base64
import hashlib
import hmac
import os


# Password hashing configuration. This uses the Python standard library and
# therefore does not require the unavailable ``passlib`` package.
_ALGORITHM = "pbkdf2_sha256"
_ITERATIONS = 600_000
_SALT_LENGTH = 16


def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure hash.
    """
    salt = os.urandom(_SALT_LENGTH)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _ITERATIONS
    )
    return "$".join(
        (
            _ALGORITHM,
            str(_ITERATIONS),
            base64.urlsafe_b64encode(salt).decode("ascii"),
            base64.urlsafe_b64encode(digest).decode("ascii"),
        )
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain password against its stored hash.
    """
    try:
        algorithm, iterations, encoded_salt, encoded_digest = hashed_password.split(
            "$", 3
        )
        if algorithm != _ALGORITHM:
            return False

        salt = base64.urlsafe_b64decode(encoded_salt.encode("ascii"))
        expected = base64.urlsafe_b64decode(encoded_digest.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256", password=plain_password.encode("utf-8"),
            salt=salt, iterations=int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (TypeError, ValueError):
        return False