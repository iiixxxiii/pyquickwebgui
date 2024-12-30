from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from pyquickwebgui import QuikeUI


app = FastAPI()

# Mounting default static files
app.mount("/public", StaticFiles(directory="public/"))
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("some_page.html", {"request": request})


@app.get("/close")
async def close_server():
    QuikeUI.close_application()


def start_fastapi():
    print("start_fastapi")

def saybye():
    print("on_exit bye")

if __name__ == "__main__":

    QuikeUI(
        server="fastapi",
        app=app,
        port=3000,
        browser_type="webview"
    ).run()


    # QuikeUI(
    #     server="fastapi",
    #     server_kwargs={
    #         "app": app,
    #         "port": 3000,
    #     },
    #     width=800,
    #     height=600,
    #     browser_type="webview",
    #     on_startup=start_fastapi,
    #     on_shutdown=saybye,
    # ).run()
