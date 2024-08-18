# coding=utf-8
import os
import sys
import zipfile
import tkMessageBox
import traceback

"""
安装脚本
"""


def checkV(v_file):
    '''
    检查版本
    '''
    pass


if __name__ == '__main__':
    try:
        exe_file = "res/main.exe"
        v_file = "res/static/v.txt"
        if not os.path.exists(exe_file) or checkV(v_file):
            zip_folder = os.path.join(sys._MEIPASS, 'res.zip')
            zip_file = zipfile.ZipFile(zip_folder)
            zip_list = zip_file.namelist()
            print("安装开始,请稍等:")
            for f in zip_list:
                print(f)
                zip_file.extract(f, "./res")
            zip_file.close()
            print("安装结束.")
        os.system("start "+exe_file)
    except Exception as e:
        print(traceback.format_exc())
        tkMessageBox.showinfo("错误", e)
 