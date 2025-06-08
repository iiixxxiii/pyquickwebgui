# py-quick-webgui
python使用webui制作桌面应用

需要python>=3.6

支持 django flask fastapi webpy 等web框架
支持 vue框架
支持 webview
项目设计改进的初衷是用来方便开发在服务器和客户都可以运行的web应用

参考 [flaskwebgui](https://github.com/ClimenteA/flaskwebgui)


## 示例

- django-desktop                            代码编辑器示例
- fastapi-desktop                           代码编辑器示例
- fastapi-desktop-stray                     增加了系统托盘图标
- fastapi-vue-desktop                       带vue的代码编辑器示例
- fastapi-webview-desktop                   增加了webview支持
- flask-desktop                             md 编辑器示例
- tauripy-fastapi-desktop-stray(recommend)  tauri 集成(推荐使用该模板开发)
- webpy-desktop                             最小运行程序示例



## 打包

### 打包命令
```shell lines

package.bat

package.sh

```

### 打包说明

res
文件内是目录

res.zip包含真正执行文件main.exe 资源目录 static ,被打包到 package.exe


xx.exe
启动时候先释放  res目录,找到main.exe 执行


包裹文件就负责释放执行文件和资源






## 更新日志
- 2025-05-01   V 0.0.4
  - 增加:tauri支持


- 2025-04-12   V 0.0.3
  - 增加:系统托盘图标功能
  - 优化:vue 支持

- 2024-08-01   V 0.0.2
  - 增加:webview  支持
  - 增加:webpy 支持
