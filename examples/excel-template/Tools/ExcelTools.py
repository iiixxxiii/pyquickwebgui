# coding=utf-8
import sys, os
import requests
import json
import time
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

from LogTools import LogTools


class ExcelTools():
    """
    读取 excel 工具

    数据表 从 0开始计算
    行 , 列 从 0开始计算

    """
    def __init__(self, log=None, file_path=None):
        if log:
            self.log = log
        else:
            self.log = LogTools().getlogger()

        if file_path:
            self._read(file_path)

    def _read(self, file_path):
        """
        读取文件
        :param file_path:
        :return: wb
        """
        self.wb = None
        try:
            self.file_path = file_path

            # 获取工作簿对象
            self.wb  = pd.ExcelFile(file_path)
        except Exception as e:
            self.log.error("读取文件:" + file_path+str(e))

        return self


    def read(self, file_path):
        """
        读取文件
        :param file_path:
        :return: ExcelTools
        """
        self.log.info("read读取文件:" + file_path)
        return ExcelTools(log=self.log , file_path=file_path)


    def get_sheetnames(self):
        """
        获取所有工作表名称
        :return: array
        """
        self.log.info("get_sheetnames:" + str(self.wb))
        return  self.wb.sheet_names


    def read_sheet(self,index=0,name=None, headindex=0):
        """_summary_
            读取工作表
        Args:
            index (int, optional): _description_. Defaults to 0.
            name (_type_, optional): _description_. Defaults to None.
            headindex (_type_, optional): _description_. Defaults to 0 无头.

        Returns:
            _type_: _description_
        """
        self.sheeto = self.get_sheeto(index,name)
        # 填充缺失值
        self.sheeto.fillna("", inplace=True)
        self.headindex = headindex
        self.columns = self.sheeto.columns.values
        #真正的头数据
        self.heads = self.get_heads(headindex)

        return self

    def get_heads(self,headindex=0):
        """
        获取工作表对象头部
        :headindex  默认0 无头用数字作为头部
        :return: array
        """
        if headindex>0:
            return self.get_rowarrs(row=headindex)
        else:
            return self.columns.tolist()

    def _get_def_head(self):
        """
        获取默认工作表对象头部 使用A..Z
        """
        _def_head = []
        rows , cols = self.get_len()
        for i in range(1,cols):
            _def_head.append(self.convert_to_letter(i,1))
        return _def_head

    def get_sheeto(self,index=None,name=None):
        """
        获取工作表对象
        :return: sheet
        """
        sheeto = None
        if name in self.wb.sheet_names:
            sheeto = self.wb.parse(sheet_name=name)
        elif index>=0:
            sheeto = self.wb.parse(index_col=index)
        return sheeto

    def get_len(self,sheeto=None):
        """
        获取工作表数据长度
        :return: rows cols
        """
        if  sheeto is None:
            sheeto = self.sheeto
        # 获取工作表总行数
        rows = len(self.sheeto)
        # 获取工作表总列数
        cols = len(self.sheeto.columns)
        return rows , cols

    def get_cellvalue(self , row, column , sheeto=None):

        if not sheeto:
            sheeto = self.sheeto
        return  sheeto.ic

    def get_rowarrs(self , row, sheeto=None):
        if not sheeto:
            sheeto = self.sheeto
        # 读取一行的所有内容
        row_list = sheeto.iloc[row].values
        return row_list


    def get_rowMap(self , row, sheeto=None):

        if not sheeto:
            sheeto = self.sheeto
        #整体位移
        row = row + self.headindex - 1
        row_map = {}
        # 大于 0 特殊处理
        if self.headindex>0:
            row_list = sheeto.iloc[row].values
            for i in range( 0, len(self.heads) ):
                row_map[self.heads[i]] = row_list[i]
        else:
            row_map = sheeto.iloc[row].to_dict()
        return row_map

    def get_rowMapArr(self , srow = 1 , erow = 0 ):

        srow = srow + self.headindex

        if erow == 0:
            erow = len(self.sheeto) - self.headindex
        self.log.info("get_rowMap srow=" + str(srow)+ " erow="+str(erow))
        row_map_arr = []
        for i in range(srow, erow+1):
            rmap = self.get_rowMap(i)
            self.log.info( "get_rowMap i=" + str(i)+ " |rmap="+ str(rmap) )
            if len(rmap)>0:
                row_map_arr.append(rmap)
        return row_map_arr

    def save(self,file_path=None):
        """
        保存文件
        :param file_path:
        :return: ExcelTools
        """
        if not file_path:
            file_path = self.file_path
        self.wb.save(file_path)


    def convert_to_number(self,letter, columnA=0):
        """
        字母列号转数字
        columnA: 你希望A列是第几列(0 or 1)? 默认0
        return: int
        """
        ab = '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letter0 = letter.upper()
        w = 0
        for _ in letter0:
            w *= 26
            w += ab.find(_)
        return w - 1 + columnA


    def convert_to_letter(self,number, columnA=0):
        """
        数字转字母列号
        columnA: 你希望A列是第几列(0 or 1)? 默认0
        return: str in upper case
        """
        ab = '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        n = number - columnA
        x = n % 26
        if n >= 26:
            n = int(n / 26)
            return self.convert_to_letter(n,1) + ab[x+1]
        else:
            return ab[x+1]


if __name__ == "__main__":
    # excel =  ExcelTools(file_path="C:\\Users\\lixin\\Desktop\\templateExportrabbitmq.xlsx")
    # # print(excel.get_sheetnames())
    # excel.read_sheet(headindex=1)
    # print(excel.get_rowMap(1))

    # print (self.head)
    # print (excel.convert_to_letter(26))

    for i in range(1, 2):
        print i