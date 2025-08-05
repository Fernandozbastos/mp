from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel

from ..auth.jwt import create_access_token, get_token_subject
from ..auth.security import get_password_hash, verify_password

router = APIRouter()

fake_users_db: dict[str, str] = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class UserCreate(BaseModel):
    username: str
    password: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        username = get_token_subject(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return username


@router.post("/register", status_code=201)
async def register(user: UserCreate) -> dict[str, str]:
    """Register a new user."""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = hashed_password
    return {"username": user.username}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Authenticate a user and return an access token."""
    hashed_password = fake_users_db.get(form_data.username)
    if not hashed_password or not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/")
async def read_root(current_user: str = Depends(get_current_user)) -> dict[str, str]:
    """Root API endpoint."""
    return {"message": "Welcome to mp API"}
