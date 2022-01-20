from fastapi import APIRouter
from api.api_v1.endpoints import private, shorten, redirect, test
from api.api_v1.endpoints.user_endpoints import activate, login, register, user


api_router = APIRouter()

api_router.include_router(test.router, tags=["test"])
api_router.include_router(shorten.router, tags=["shorten"])
api_router.include_router(private.router, tags=["private"])
api_router.include_router(user.router, tags=["user"])

api_router.include_router(activate.router, tags=["activate"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(register.router, tags=["register"])
api_router.include_router(redirect.router, tags=["redirect"])
