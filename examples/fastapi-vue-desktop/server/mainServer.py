import os


from doctest import debug
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from pyquickwebgui import QuikeUI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mounting default static files
app.mount("/assets", StaticFiles(directory="../ui/assets"), name="assets")
templates = Jinja2Templates(directory="../ui")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/close")
async def close_server():
    QuikeUI.close_application()




if __name__ == "__main__":

    DEBUG = True

    if (DEBUG):
        build = os.system(" cd ../guisrc & npm install & npm run build & cp -r dist/* ../mainServer/gui/  ")
        print(build)
        print("build end")
    QuikeUI(
        server="fastapi",
        app=app,
        port=3000,
        debug=DEBUG
        # browser_type="webview"
    ).run()
