#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import os
import xlrd
import xlwt
import time

def get_col_by_name(table,name):
    name_col = 0
    ncols = table.ncols
    for col in range(ncols):
        if table.cell(0,col).value == name:
            name_col = col
    return name_col

def read_case_list():
    excel_path = os.getcwd() + '/'+'CASE.xls'
    case_list=list()
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name('text_excel')
    nrows = table.nrows
    user_col = get_col_by_name(table,"E")
    case_col = get_col_by_name(table,"D")
    flag_col = get_col_by_name(table,"F")
    for row in range(nrows):
        if table.cell(row,user_col).value == "yes":
            case_list.append([table.cell(row,case_col).value,table.cell(row,flag_col).value])
    return  case_list

def set_no_ok_key(case_list,flag = "NOK"):
    global index
    for i in range(index):
        if not case_list[i][1]:
            case_list[i][1] = flag
    return case_list

def save_excel_with_case(case_list):
    case_list = set_no_ok_key(case_list)
    total_table = list()
    excel_path = os.getcwd() + '/'+'CASE.xls'
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name('text_excel')
    nrows = table.nrows
    ncols = table.ncols
    for rows in range(nrows):
        row_list = list()
        for cols in range(ncols):
            row_list.append(table.cell(rows,cols).value)
        total_table.append(row_list)
    #print(total_table)
    case_col = get_col_by_name(table,"D")
    flag_col = get_col_by_name(table,"F")
    case_col_list = list(map(lambda x:x[case_col],total_table))
    #print(list(case_col_list))
    for name,flag in case_list:
        i = case_col_list.index(name)
        total_table[i][flag_col] = flag
    #print(total_table)
    new_excel = os.getcwd()+'\\'+'CASE'+time.strftime("_%Y-%m-%d_%H_%M_%S", time.localtime())+'.xls'
    myWorkbook = xlwt.Workbook()
    mySheet = myWorkbook.add_sheet('text_excel')
    for i in range(len(total_table)):
        for j in range(len(total_table[i])):
            mySheet.write(i,j,total_table[i][j])
    myWorkbook.save(new_excel)
    #print(new_excel)
#save_excel()
def record_case_flag(case_list,case,flag="OK"):
    for i in range(len(case_list)):
        if case_list[i][0] == case:
            case_list[i][1] = flag
            break
    return

index = 0
def get_begin_index(case_list):
    global index
    for i in range(len(case_list)):
        if not case_list[i][1]:
            index = i
            break
    return index

def get_next_index(case_list):
    global index
    for i in range(index+1,len(case_list)):
        if not case_list[i][1]:
            index = i
            break
    return index

def get_begin_case(case_list):
    index = get_begin_index(case_list)
    return case_list[index][0]

def get_current_case(case_list):
    global index
    return case_list[index][0]

def get_next_case(case_list):
    index = get_next_index(case_list)
    return case_list[index][0]

def get_all_case_path():
    all_case_path = list()
    pwd = os.getcwd()
    file_path=""
    for names,b,c in os.walk(pwd):
        all_case_path.append(names)
    return all_case_path

ALL_CASE_PATH = get_all_case_path()

def get_case_path(case_name):
    all_case_path = ALL_CASE_PATH
    file_path=""
    for names in all_case_path:
        #print(names)
        if names.endswith(case_name):
            file_path = names
            break
    return file_path

def get_case_xml_path(case_name):
    file_path = get_case_path(case_name)
    return file_path + "/case.xml"

def get_python_path(case_name):
    file_path = get_case_path(case_name)
    py_path = ''
    for names in os.listdir(file_path):
        if names.lower().startswith('test') and names.lower().endswith('.py'):
            py_path = file_path + '/' + names
            break
    return py_path

SPLIT_WORDS = ['.','(',')',' ','#']
HLS_WORDS = ['replace','print']
NOTES_HLS_WORDS = ['#']
BLUE_HLS_WORDS = ['False','None', 'True','and','as', 'assert','break', 'class','continue', 'def','del','elif', 'else','except','finally', 'for', 'from','global','if','import','in','is','lambda', 'nonlocal','not','or','pass','raise', 'return','try','while','with','yield']
LIME_HLS_WORDS = ['clear_string','get_website_by_url','get_website_title']

def split_text(context,split_words):
    lines = context.split('\n')
    words = list()
    for line in lines:
        for split_word in split_words:
            line = line.replace(split_word,'\n'+split_word+'\n')
        words.append(line.split('\n'))
    return words

def read_file_context(file_name):
    with open(file_name,"r") as f :
        file_context = f.read()
        #print(file_context)
    return file_context

def show_py_context(py_text,words):
    py_text.tag_config('green',foreground = 'green')
    py_text.tag_config('blue',foreground = 'blue')
    py_text.tag_config('red',foreground = 'red')
    for lines in words:
        notes_flag = False
        for word in lines:
            if notes_flag:
                py_text.insert(tk.CURRENT,word,'green')
            elif word in NOTES_HLS_WORDS:
                notes_flag = True
                py_text.insert(tk.CURRENT,word,'green')
            elif word in BLUE_HLS_WORDS:
                py_text.insert(tk.CURRENT,word,'blue')
            elif word in LIME_HLS_WORDS:
                py_text.insert(tk.CURRENT,word,'red')
            else:
                py_text.insert(tk.CURRENT,word)
        py_text.insert(tk.CURRENT,'\n')


def write_file_context(file_name,context):
    with open(file_name,"w") as f:
        f.write(context)

#windows
root_windows = tk.Tk()
root_windows.title('View Case and Pyhton')
root_windows.geometry('1000x600')

#case
case_list = read_case_list()
case_frame = tk.LabelFrame(root_windows,text = 'Case',width = 492,height = 525)
case_frame.place(x=5,y=6)
b_index = get_begin_case(case_list)
file_context = read_file_context(get_case_xml_path(b_index))
case_text = tk.Text(case_frame,width = 68,height = 38,bg='whitesmoke')
case_text.place(x=1,y=1)
case_text.insert(tk.INSERT,file_context)
#case_text.insert(tk.END,'sample','a')
#python
py_frame = tk.LabelFrame(root_windows,text = 'Python',width = 492,height = 525)
py_frame.place(x=502,y=6)
file_context = read_file_context(get_python_path(b_index))
words = split_text(file_context,SPLIT_WORDS)
py_text = tk.Text(py_frame, width = 68, height = 38,bg='whitesmoke')
py_text.place(x=1,y=1)
show_py_context(py_text,words)
#case_text.tag_config('a',foreground = 'red')
#py_text.insert(tk.INSERT,file_context)

#update button
def update():
    txt = case_text.get("0.0","end")
    c_case = get_current_case(case_list)
    write_file_context(get_case_xml_path(c_case),txt)
    record_case_flag(case_list,c_case,"OK")
    #print(case_list)
update_button = tk.Button(root_windows,bg = 'burlywood',text="Update",width = 20, height = 2,command = update)
update_button.place(x = 100 , y=535)

#flush button
def flush():
    py_text.delete("0.0","end")
    case_text.delete("0.0","end")
    c_case = get_current_case(case_list)
    file_context = read_file_context(get_python_path(c_case))
    py_text.insert(tk.INSERT,file_context)
    file_context = read_file_context(get_case_xml_path(c_case))
    case_text.insert(tk.INSERT,file_context)
flush_button = tk.Button(root_windows,bg = 'burlywood',text="Flush",width = 20, height = 2,command = flush)
flush_button.place(x = 300 , y=535)

# count label
count = 0
textvar = tk.StringVar()
label = tk.Label(root_windows,textvariable=textvar,bg='snow')
label.place(x=492 ,y = 548)


#next button
def next():
    global count
    count += 1
    print(count)
    textvar.set(count)
    py_text.delete("0.0","end")
    case_text.delete("0.0","end")
    n_case = get_next_case(case_list)
    file_context = read_file_context(get_python_path(n_case))
    words = split_text(file_context,SPLIT_WORDS)
    show_py_context(py_text,words)
    #py_text.insert(tk.INSERT,file_context)
    file_context = read_file_context(get_case_xml_path(n_case))
    case_text.insert(tk.INSERT,file_context)
next_button = tk.Button(root_windows,bg = 'burlywood',text="Next",width = 20, height = 2,command = next)
next_button.place(x = 550 , y=535)

def save_excel():
    global case_list
    global index
    save_excel_with_case(case_list)
    case_list = read_case_list()
    index = 0
next_button = tk.Button(root_windows,bg = 'burlywood',text="Save",width = 20, height = 2,command = save_excel)
next_button.place(x = 750 , y=535)

tk.mainloop()
