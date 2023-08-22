from fastapi import APIRouter, HTTPException
from configs.auth import auth_name, auth_pass
from modules.secret import get_md5_hash
from pydantic import BaseModel

router = APIRouter()


class UserCredentials(BaseModel):
    name: str
    password: str


@router.post('/login')
def check_login(user: UserCredentials):
    if user.name == auth_name and user.password == auth_pass:
        token = get_md5_hash("token4assert_review")
        return {"code": 200, "data": {"token": token}}
    else:
        return HTTPException(status_code=401, detail="Invalid Credentials")
