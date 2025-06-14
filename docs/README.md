
## 打包

### 打包命令
```shell lines

# 自动生成 .rst 文件

cd pyquickwebgui
cd docs

sphinx-apidoc -o source/api ../src/pyquickwebgui --force --no-toc




make clean; make html

```

