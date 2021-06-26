#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import xlwt
import os
import time
import re

class ExcelControl():

    def __init__(self):
        self.sheet_name = 'Sheet1'
        self.col_name = 'URL'
        self.re_format = '(.*)'
        self.dir = 'D:\\code\\mirror\\compile_excel_by_key\\'
        self.old_excel_name = self.dir + 'old.xls'
        self.new_excel_name = self.dir + 'new.xls'
        #self.datef = time.strftime("_%Y-%m-%d_%H_%M_%S", time.localtime())
        self.del_lines = dict()
        self.add_lines = dict()
    
    def _init_data(self):
        old_date = self._get_exce_data(self.old_excel_name)
        new_data = self._get_exce_data(self.new_excel_name)
        self.banner = old_date[0]
        col_index = self._get_col_by_name(self.col_name, self.banner)
        old_date ,new_data = old_date[1:], new_data[1:]
        self.old_dict_data = self._get_date_with_key_value(col_index, old_date)
        self.new_dict_data = self._get_date_with_key_value(col_index, new_data)
        print(self.old_dict_data)
        print(self.new_dict_data)
        self.del_lines = self._diff_add_by_key(self.old_dict_data, self.new_dict_data)
        self.add_lines = self._diff_add_by_key(self.new_dict_data, self.old_dict_data)
        new_data = self._gen_new_data(self.banner, self.old_dict_data, self.del_lines, self.add_lines)
        save_path = self.dir + "output" + time.strftime("_%Y-%m-%d_%H_%M_%S", time.localtime()) + ".xls"
        self._save_date(save_path, new_data)

    
    def _gen_new_data(self,banner, old_data, del_lines=None, add_lines = None):
        new_data = list()
        new_data.append(banner)
        for key_tmp in old_data:
            new_data.append(old_data[key_tmp])
        del_tmp = ["Delete" ] + [""] * (len(banner)-1)
        new_data.append(del_tmp)
        for key_tmp in del_lines:
            new_data.append(del_lines[key_tmp])
        add_tmp = ["Add" ] + [""] * (len(banner) - 1)
        new_data.append(add_tmp)
        for key_tmp in add_lines:
            new_data.append(add_lines[key_tmp])
        return new_data

    def _save_date(self, save_path, new_table_data):
        myWorkbook = xlwt.Workbook()
        mySheet = myWorkbook.add_sheet(self.sheet_name)
        for i in range(len(new_table_data)):
            for j in range(len(new_table_data[i])):
                mySheet.write(i,j,new_table_data[i][j])
        myWorkbook.save(save_path)

    def _diff_add_by_key(self, sour, des):
        diff_lines = dict()
        for key_tmp in sour: 
            if key_tmp not in des:
                print(key_tmp)
                diff_lines[key_tmp] = sour[key_tmp]
        return diff_lines

    def _get_exce_data(self, excel_path):
        result = list()
        data = xlrd.open_workbook(excel_path)
        table = data.sheet_by_name(self.sheet_name)
        for i in range(table.nrows):
            result.append(table.row_values(i))
        return result
    
    def _get_col_by_name(self, name, name_list):
        print(name_list.index(name))
        return name_list.index(name)
    
    def _get_date_with_key_value(self, index, excel_data):
        res = dict()
        for line in excel_data:
            line_key = re.search(self.re_format, line[index])[0]
            res[line_key] = line
        return res


if __name__ == '__main__':
    ec = ExcelControl()
    ec._init_data()




