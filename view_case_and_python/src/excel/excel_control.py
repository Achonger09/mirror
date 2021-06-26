#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import xlwt
import os
import time
from src.util.case_format import *

class ExcelControl():

    def __init__(self,excel_path):
        self.CASE_BEGIN_ROW = 3
        self.CASE_TITLE_ROW = 2
        self.excel_path = excel_path
        self.case_format = CaseFromat()
        self.sheet_name = 'text_excel'
        self.sheet_data = None
        self.table = None
        self.nrows = None
        self.ncols = None
        self.all_case_data = list()
        self.case_data = list()
        self.current_case_row = 0
        self.init_case_data()

    def init_excel(self):
        if not self.excel_path.startswith("/"):
            self.excel_path = os.path.join(os.getcwd(),self.excel_path)
        data = xlrd.open_workbook(self.excel_path)
        self.table = data.sheet_by_name(self.sheet_name)
        #print("tables" + str(self.table))
        self.nrows = self.table.nrows
        print("nrows :" + str(self.nrows))
        self.ncols = self.table.ncols
        print("ncows :" + str(self.ncols))
        self.case_format.caseName = self.__get_col_by_name("caseName")
        print("self.case_format.caseName :"+str(self.case_format.caseName))
        self.case_format.isHandle = self.__get_col_by_name("isHandle")
        self.case_format.result = self.__get_col_by_name("result")
        print("self.case_format.result :"+str(self.case_format.result))

        for r in range(0,self.nrows):
            list_tmp = list()
            for c in range(0,self.ncols):
                list_tmp.append(self.table.cell(r,c).value)
            self.all_case_data.append(list_tmp)
        #print("#1 . all case data :" + str(self.all_case_data))

    def __get_col_by_name(self,name):
        name_col = 0
        for col in range(self.ncols):
            if self.table.cell(self.CASE_TITLE_ROW-1,col).value == name:
                name_col = col
                break
        return name_col

    def init_case_data(self):
        self.init_excel()
        for row in range(self.nrows):
            if self.table.cell(row,self.case_format.isHandle).value == "yes":
                self.case_data.append([self.table.cell(row,self.case_format.caseName).value,
                                       self.table.cell(row,self.case_format.result).value])
        print("#1. case data :" + str(self.case_data))

    def change_next(self):
        for now_row in range(self.current_case_row+1,len(self.case_data)):
            if not self.case_data[now_row][1]:
                self.current_case_row = now_row
                break

    def get_current_caseName(self):
        print("#1 .current row "+str(self.current_case_row))
        return self.case_data[self.current_case_row][0]

    def set_current_case_result(self,result):
        if self.case_data[self.current_case_row][1]:
            print("#1. result is not null ,set failed !!")
        else:
            print("#1. change row " + str(self.current_case_row))
            self.case_data[self.current_case_row][1] = result

    def save_excel_with_name(self,new_file_path):
        print("#1. before save case date :" + str(self.case_data))
        new_table_data = self.all_case_data
        for now_row in range(self.nrows):
            for now_case_data in self.case_data:
                #print("#1. compare:"+str(new_table_data[now_row][self.case_format.caseName]) + " "+ now_case_data[0])
                if new_table_data[now_row][self.case_format.caseName] == now_case_data[0]:
                    #print("#1. compare:"+str(new_table_data[now_row][self.case_format.caseName]) + " "+ now_case_data[0] + "true")
                    new_table_data[now_row][self.case_format.result] = now_case_data[1]
        #print("#1. result date" + str(new_table_data))
        myWorkbook = xlwt.Workbook()
        mySheet = myWorkbook.add_sheet('text_excel')
        for i in range(len(new_table_data)):
            for j in range(len(new_table_data[i])):
                mySheet.write(i,j,new_table_data[i][j])
        myWorkbook.save(new_file_path)

    def save_excel(self):
        file_excel_name = os.path.basename(self.excel_path)
        file_excel_dir = os.path.dirname(self.excel_path)
        file_name_pre,file_name_sub = file_excel_name.split(".")
        new_file_name = file_name_pre+time.strftime("_%Y-%m-%d_%H_%M_%S", time.localtime())+"."+file_name_sub
        print("#1. new file path :"+ os.path.join(file_excel_dir,new_file_name))
        self.save_excel_with_name(os.path.join(file_excel_dir,new_file_name))




