# py-quick-webgui
python使用webui制作桌面应用

python3.6版本以上

参考 [flaskwebgui](https://github.com/ClimenteA/flaskwebgui)


## 示例

- django-desktop
- fastapi-desktop         代码编辑器示例
- flask-desktop           md 编辑器示例
- webpy-desktop           最小运行程序示例



##  打包

###  打包命令
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



