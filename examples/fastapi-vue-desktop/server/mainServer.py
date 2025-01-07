import os


from doctest import debug
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from pyquickwebgui import QuikeUI


app = FastAPI()

# Mounting default static files
app.mount("/assets", StaticFiles(directory="../gui/dist/assets"), name="assets")
templates = Jinja2Templates(directory="../gui/dist")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("some_page.html", {"request": request})


@app.get("/close")
async def close_server():
    QuikeUI.close_application()




if __name__ == "__main__":

    DEBUG = True

    if (DEBUG):
        build = os.system(" cd ../gui & npm run dev ")
        print(build)
        print("build end")
    QuikeUI(
        server="fastapi",
        app=app,
        port=3000,
        debug=DEBUG
        # browser_type="webview"
    ).run()
