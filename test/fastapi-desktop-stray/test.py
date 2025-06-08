from fastapi import FastAPI
from pywebio.platform.fastapi import asgi_app , webio_routes
from pywebio.input import input, FLOAT, input_group  # 正确导入 input 和 input_group
from pywebio.output import put_text
from pywebio import input, output
# 定义一个 PyWebIO 应用
def my_app():
    data = input_group("请输入一个数字", [
        input('请输入一个数字', type=FLOAT, name='number'),
    ])
    number = data['number']
    result = number * 2
    put_text(f'您输入的数字乘以2的结果是: {result}')
def greet_user_page():
    username = input_group("请输入你的名字：", [
        input('请输入你的名字：', type=FLOAT, name='number'),
    ])
    put_text(f"你好，{username}！欢迎使用PyWebIO。")










# 使用 asgi_app 包装 PyWebIO 应用
app_fastapi = asgi_app(my_app)

# 创建 FastAPI 实例
app = FastAPI()

# 将 PyWebIO 应用挂载到 FastAPI 路由
app.mount("/webio", app_fastapi)
app.add_route("/greet_user", webio_routes(greet_user_page))