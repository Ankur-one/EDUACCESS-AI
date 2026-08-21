import importlib


# Load the optional dependency dynamically so static analyzers do not report
# an unresolved import when the active interpreter has not installed bcrypt.
bcrypt = importlib.import_module("bcrypt")


# ============================================================
# HASH PASSWORD
# ============================================================

def hash_password(password: str) -> str:

    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed_password.decode("utf-8")


# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    password: str,
    password_hash: str
) -> bool:

    if not password or not password_hash:
        return False

    try:

        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )

    except (ValueError, TypeError):

        return False