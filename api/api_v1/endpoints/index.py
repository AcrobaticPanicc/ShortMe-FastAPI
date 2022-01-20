from starlette.responses import HTMLResponse
from app import application


@application.get("/")
async def index():
    with open("./templates/index.html", 'r') as f:
        return HTMLResponse(content=f.read())
