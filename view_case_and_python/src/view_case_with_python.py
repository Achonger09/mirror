#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.excel.excel_control import *
from src.file.file_control import *
from src.show.show_control import *

class ViewCaseWithPython():

    excel_control = ExcelControl("..\\CASE.xls")
    file_control = FileControl("..\\case")
    show_control = ShowControl(excel_control,file_control)

    if __name__ == '__main__':
        show_control.TK_loop()
        '''
        print("#0 .current case :"+excel_control.get_current_caseName())
        excel_control.set_current_case_result("NOK")
        excel_control.save_excel()
       '''
        '''
        file_control.read_case_file("test_case_001")
        file_control.read_python_file("test_case_001")
        file_control.get_case_path("test_case_001")
       '''


