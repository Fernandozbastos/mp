from app.auth.security import get_password_hash, verify_password


def test_password_hashing() -> None:
    password = "secret"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)
