#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class FileControl():

    def __init__(self,case_dir):
        self.file_name_case = "case.xml"
        if not case_dir.startswith("//"):
            self.case_dir = os.path.join(os.getcwd(),case_dir)
        else:
            self.case_dir = case_dir
        self.all_case_dir_list = list()
        self.case_path_list = list()
        self.init_case_path()

    def __get_path_by_caseName(self,caseName):
        case_dir = ""
        for tmp_dir in self.all_case_dir_list:
            #print("#2. match file :" + caseName + " " + tmp_dir)
            if tmp_dir.endswith(caseName) or tmp_dir.endswith(caseName+"\\"):
                print("#2. match file success:" + caseName + " " + tmp_dir)
                case_dir = tmp_dir
                break
        if len(case_dir) == 0:
            print("#2. match failed :" + caseName)
        return case_dir

    def __get_python_path(self,caseName):
        case_dir = self.__get_path_by_caseName(caseName)
        py_path = ""
        for names in os.listdir(case_dir):
            if names.lower().startswith('test') and names.lower().endswith('.py'):
                py_path = os.path.join(case_dir,names)
                break
        print("#2. python path : "+ py_path)
        return py_path

    def get_case_path(self,caseName):
        return self.__get_case_path(caseName)

    def __get_case_path(self,caseName):
        case_dir = self.__get_path_by_caseName(caseName)
        case_path = os.path.join(case_dir,self.file_name_case)
        print("#2. case path : "+ case_path)
        return case_path

    def read_file_context(self,file_name):
        with open(file_name,"r") as f :
            file_context = f.read()
        print("#2. read file:"+file_name )
        return file_context

    def read_python_file(self,caseName):
        py_path = self.__get_python_path(caseName)
        return self.read_file_context(py_path)

    def read_case_file(self,caseName):
        case_path = self.__get_case_path(caseName)
        return self.read_file_context(case_path)

    def write_file_context(self,file_name,context):
        print("#2. write file:"+file_name )
        with open(file_name,"w") as f:
            f.write(context)

    def write_python_file(self,caseName,context):
        py_path = self.__get_path_by_caseName(caseName)
        self.write_file_context(py_path)

    def write_case_file(self,caseName,context):
        case_path = self.__get_case_path(caseName)
        self.write_file_context(case_path,context)

    def init_case_path(self):
        for names,b,c in os.walk(self.case_dir):
            if names.split("\\")[-1].startswith("test"):
                self.all_case_dir_list.append(names)
        #print("#2. all_case_dir_list :" + str(self.all_case_dir_list))

