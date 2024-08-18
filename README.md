# py-desktop-webui
python使用webui制作桌面应用 


## 示例

- code-edit            代码编辑器示例
- md-edit              md 编辑器示例
- minimize             最小运行程序示例




##  打包

###  打包命令
```shell lines
pyinstaller -F package.py  -i "res/favicon.ico"  --add-data="res;res"
```

### 打包说明

res
文件内是目录

res.zip包含真正执行文件main.exe 资源目录 static ,被打包到 package.exe


xx.exe
启动时候先释放  res目录,找到main.exe 执行


包裹文件就负责释放执行文件和资源



