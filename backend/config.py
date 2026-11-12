import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
TOKEN_EXPIRE_MINUTES = int(os.environ["TOKEN_EXPIRE_MINUTES"])
REFRESH_TOKEN_DAYS = int(os.environ["REFRESH_TOKEN_DAYS"])

pass_hash = PasswordHash.recommended()
outh2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")