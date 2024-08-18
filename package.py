# coding=utf-8
import os, sys
import zipfile
import shutil


"""
打包应用脚本
"""


def zip_dir(path, output=None):
    """压缩指定目录"""
    output = output or os.path.basename(path) + '.zip' # 压缩文件的名字
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(path):
            relative_root = '' if root == path else root.replace(path, '') + os.sep  # 计算文件相对路径
            # relative_root = root
            for filename in files:
                zip.write(os.path.join(root, filename), relative_root + filename)  # 文件路径 压缩文件路径（相对路径）





if __name__ == '__main__':

    try:

        # 项目
        project_name = "/minimize"
        # exe名称
        exe_name = "web-ui-minimize"

        print("编译开始......")
        if os.path.isdir("dist_tmp"):
            shutil.rmtree("dist_tmp")
        if os.path.isdir("dist"):
            shutil.rmtree("dist")

        print("打包项目")
        a = os.system('pyinstaller -F  src/' + project_name + '/main.py --name=main -i "src/' + project_name + '/static/favicon.ico"  ')
        print("项目打包end:")
        print("复制目录")

        # 移动操作
        shutil.copytree('src/' + project_name + "/static", "dist_tmp/static")

        # 删除 用户配置文件
        if os.path.isfile("dist_tmp/static/user_config.ini"):
            os.remove("dist_tmp/static/user_config.ini")

        shutil.copy("dist/main.exe", "dist_tmp/main.exe")
        print("复制目录end")
        print("资源打包")
        zip_dir(r'dist_tmp','dist/res.zip')
        print("资源打包end")
        print("package打包")
        a = os.system('pyinstaller -F -w -c --onefile --windowed init_package_run.py --name=package -i "src/' + project_name + '/static/favicon.ico"  --add-data="dist/res.zip;."')

        print("package打包end")

        print("编译end......")
    except Exception as e:
        print(e)
