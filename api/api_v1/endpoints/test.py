from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from services.templates import templates

router = APIRouter()


@router.get('/test', response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, 'name': ['tomer']})

