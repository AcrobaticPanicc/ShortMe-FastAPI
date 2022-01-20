from fastapi import APIRouter, Depends
from crud.url import url_crud
from responses.responses import success_responses
from schemas.url import ShortenUrl, UrlResponse
from login_manager.login_manager import manager
from starlette.requests import Request

router = APIRouter()


@router.post('/shorten')
async def shorten(url: ShortenUrl, request: Request, user=Depends(manager)):
    req_data = dict(url)
    req_data['owner_id'] = user.id_
    shorten_url = url_crud.shorten_url(**req_data)
    req_data['short_url'] = f'{str(request.base_url)}{shorten_url.short_url}'
    req_data['date_created'] = str(shorten_url.date_created)
    data = UrlResponse(**req_data).dict()
    return success_responses.get_response('URL_SHORTENED_SUCCESSFUL', data=data)
