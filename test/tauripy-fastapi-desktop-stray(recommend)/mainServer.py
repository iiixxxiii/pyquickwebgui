from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI


import os , sys
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "../../")
sys.path.append(src_dir)
from  src.pyquickwebgui.pyquickwebgui import QuikeUI
from  src.pyquickwebgui.config.QuickConfig import  Browser_type_enum ,Server_enum
from  src.pyquickwebgui.modules.BaseResponse import BaseResponse

app = FastAPI()

# Mounting default static files
app.mount("/public", StaticFiles(directory="./public"), name="static")
templates = Jinja2Templates(directory="templates")



import dominate
from dominate.tags import *

def home_page():

    # 创建一个新的HTML文档
    doc = dominate.document(title='Button Event Example')

    # 添加一些外部资源，如CSS或JS文件
    with doc.head:
        script(type='text/javascript', src='https://code.jquery.com/jquery-3.2.1.min.js')
        link( rel="stylesheet" , href ='/public/css/style.css')
    # 在body中添加内容
    with doc:
        with div(id='content'):
            # 创建一个按钮，并为它添加一个ID和一个onclick事件处理器
            button('Click Me!', _class="button_style", onclick="alert('Button was clicked!');")

            # 或者如果你想要更复杂的逻辑，可以定义一个函数并在onclick属性中调用它
            script("""
                function handleButtonClick() {
                    alert('Button was clicked and handled by a function!');
                }
            """, type='text/javascript')

            # 然后在按钮上引用这个函数
            button('Click Me with Function!', _class="button_style", onclick="handleButtonClick();")

    return doc


###############pages#################

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/home_page", response_class=HTMLResponse)
async def home(request: Request):
    return  HTMLResponse(content=home_page().render() , status_code=200)

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("some_page.html", {"request": request})

@app.get("/sql", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("sql_page.html", {"request": request})


###############apis#################
@app.get("/apis/open_file")
async def open_file():
    print("open_file")
    res = QuikeUI.open_local_file()
    print("open_file end")
    return BaseResponse.success(data=res)

@app.get("/apis/close")
async def close_server():
    print("closing server")
    QuikeUI.close_application()


def start_fastapi(**kwargs):
    import uvicorn

    uvicorn.run(**kwargs)


if __name__ == "__main__":

    QuikeUI(
        server = Server_enum.FASTAPI ,
        app=app,
        width=800,
        height=566,
        browser_type = Browser_type_enum.COMMAND,
        # debug=True,
        stray = {
            'img' : "favicon.png"
        },
        on_startup = lambda: print("=========>on_startup")
    ).run()

