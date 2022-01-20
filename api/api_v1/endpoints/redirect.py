from fastapi import HTTPException, Depends
from fastapi_cache.backends.redis import RedisCacheBackend
from starlette.responses import RedirectResponse
from fastapi import Request, APIRouter
from crud.url import url_crud
from db.models.models import ShortUrl
from login_manager.login_manager import verify_password
from responses.responses import error_responses
from schemas.password import Password
from services.redis_cache import redis_cache
from services.templates import templates
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/{short_url}', response_class=HTMLResponse)
async def redirect(request: Request, short_url, cache: RedisCacheBackend = Depends(redis_cache)):
    """
    This route will query the database with the short_url and will
    redirect to the original url if it exist in the database.
    """
    url = url_crud.get_url(short_url=short_url)

    if not url:
        return error_responses.get_response('URL_NOT_EXIST')

    if url.visits >= url.available_clicks != -1:
        return error_responses.get_response('URL_EXPIRED')

    if url and url.password:
        base_url = str(request.base_url)
        redirect_url = f'{base_url}validate/{url.short_url}'
        await cache.set('short_url', url.short_url)
        await cache.set('password', url.password)
        return templates.TemplateResponse("index.html", {"request": request, 'redirect_url': redirect_url})

    return url_handler(url)


@router.post('/validate/{short_url}')
async def validate(request: Request, password: Password = None, cache: RedisCacheBackend = Depends(redis_cache)):
    route_url = str(request.url)
    short_url = await cache.get('short_url')
    cached_password = await cache.get('password')

    if password and cached_password:
        if verify_password(password.password, cached_password):
            url = url_crud.get_url(short_url=short_url)
            return url

    return templates.TemplateResponse("index.html", {"request": request, 'redirect_url': route_url, 'wrong_password': 'True'}, status_code=202)


def url_handler(url: ShortUrl):
    """
    Helper function used to increment the visits count, commit to db and redirect to the long url
    """
    url.visits = url.visits + 1
    url_crud.add_and_commit(url)
    response = RedirectResponse(url.long_url)
    return response
