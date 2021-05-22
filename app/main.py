from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

version = "1.0.1"
app = FastAPI(
    docs_url=None,
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "version": version,
        },
    )


@app.get('/app', response_class=HTMLResponse)
async def main(request: Request):

    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "version": version,
        },
    )


@app.get('/app/base64', response_class=HTMLResponse)
async def b64(request: Request):

    return templates.TemplateResponse(
        "b64.html",
        {
            "request": request,
            "version": version,
        },
    )


@app.get('/help', response_class=HTMLResponse)
async def help_(request: Request):

    return templates.TemplateResponse(
        "help.html",
        {
            "request": request,
            "version": version,
        },
    )
