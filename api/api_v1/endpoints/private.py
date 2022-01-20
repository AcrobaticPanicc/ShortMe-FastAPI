from login_manager.login_manager import manager
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.get("/private")
def private_route(user=Depends(manager)):
    return {"detail": f"Welcome {user.email}"}
