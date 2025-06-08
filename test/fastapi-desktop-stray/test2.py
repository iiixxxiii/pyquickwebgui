from fastapi import FastAPI
from pywebio.platform.fastapi import webio_routes
from pywebio import start_server, config
from pywebio.input import input, FLOAT
from pywebio.output import put_text

# 定义你的PyWebIO应用
@config(title="简易BMI计算器")  # 可选配置，设置网页标题
async def bmi():
    height = await input("请输入您的身高(cm):", type=FLOAT)
    weight = await input("请输入您的体重(kg):", type=FLOAT)

    bmi_value = weight / (height / 100) ** 2

    put_text('您的BMI指数是：%.1f' % bmi_value)
    if bmi_value < 18.5:
        put_text('体重偏轻')
    elif bmi_value < 24:
        put_text('体重正常')
    else:
        put_text('体重偏重')

# 创建FastAPI实例
app = FastAPI()

# 使用webio_routes函数生成路由并添加到FastAPI应用
app.mount("/tools", start_server(bmi))  # 这里直接使用start_server的方式挂载
# 或者使用webio_routes生成路由列表并添加到FastAPI应用中
# app.include_router(webio_routes(bmi)[0])

# 如果你想在同一FastAPI实例下挂载多个PyWebIO应用，可以这样做：
# app.include_router(webio_routes(app1)[0])
# app.include_router(webio_routes(app2)[0])