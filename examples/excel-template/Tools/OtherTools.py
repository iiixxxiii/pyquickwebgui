# coding=utf-8

import sys, os, time, math, json
import base64
import multiprocessing
from threading import *
import platform
import signal
import codecs, ConfigParser
import shelve
import traceback
import paramiko
import shutil
import web
import hashlib


from LogTools import LogTools
from CommonStatic import CommonStatic




class ReturnData():

    def __init__(self, jsonTools ):
        self.jsonTools = jsonTools



    def ok(self, msg='', code=0, data=None, ):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>okokoko")
        return self.jsonTools.dumps({
            "code":  code  ,
            "data": data ,
            "msg":  msg
        }  )

    def err(self, msg='', code=1, data=None, ):
        return self.jsonTools.dumps({
            "code":  code  ,
            "data":  data ,
            "msg":  msg
        } )

    def unknown(self, msg='', code=1, data=None, ):
        return self.jsonTools.dumps({
            "code": code  ,
            "data":  data ,
            "msg": msg
        } )


class OutTools():
    def __init__(self , log=None):
        self.outstr = ""
        if log:
            self.log = log
        else:
            self.log = LogTools().getlogger()

    def start(self, old=""):
        self.outstr = old
        self.put_timestr()

    def put_timestr(self, tips=""):
        self.outstr += "\n========================[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "|" + tips + "]================================\n"

    def put(self, s):
        self.outstr += s
        self.outstr += "\n"

    def out(self):
        self.outstr += "\n"
        outstr = str(self.outstr)
        self.outstr = ""
        return outstr


