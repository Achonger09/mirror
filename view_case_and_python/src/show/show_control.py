#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from src.excel.excel_control import *
from src.file.file_control import *

class ShowControl():

    SPLIT_WORDS = ['.','(',')',' ','#']
    HLS_WORDS = ['replace','print']
    NOTES_HLS_WORDS = ['#']
    BLUE_HLS_WORDS = ['False','None', 'True','and','as', 'assert','break', 'class','continue', 'def','del','elif', 'else',
                      'except','finally', 'for', 'from','global','if','import','in','is','lambda', 'nonlocal','not','or',
                      'pass','raise', 'return','try','while','with','yield']
    LIME_HLS_WORDS = ['clear_string','get_website_by_url','get_website_title']

    def __init__(self,excel_contorl,file_control):
        self.count = 0
        self.excel_control = excel_contorl
        self.file_control = file_control

    def show_paint(self,title='View Case and Pyhton',size='1000x600'):
         #windows
        self.root_windows = tk.Tk()
        self.root_windows.title(title)
        self.root_windows.geometry(size)

    def show_case_box_context(self,context,title="Case",f_width=492,f_height=525,f_index_x = 5,
                      f_index_y = 6,t_width=68,t_height=38,bg='whitesmoke',t_index_x = 1,t_index_y=1):
        self.case_frame = tk.LabelFrame(self.root_windows,text = title,width = f_width,height = f_height)
        self.case_frame.place(x=f_index_x,y=f_index_y)
        self.case_text = tk.Text(self.case_frame,width = t_width,height = t_height,bg=bg)
        case_text = self.case_text
        case_text.place(x=t_index_x,y=t_index_y)
        case_text.insert(tk.INSERT,context)

    def show_python_box_context(self,context,title="Python",f_width=492,f_height=525,f_index_x = 502,
                      f_index_y = 6,t_width=68,t_height=38,bg='whitesmoke',t_index_x = 1,t_index_y=1):
        self.py_frame = tk.LabelFrame(self.root_windows,text = title,width = f_width,height = f_height)
        self.py_frame.place(x=f_index_x,y=f_index_y)
        self.py_text = tk.Text(self.py_frame, width = t_width, height = t_height,bg=bg)
        py_text = self.py_text
        py_text.place(x=t_index_x,y=t_index_y)
        py_text.tag_config('green',foreground = 'green')
        py_text.tag_config('blue',foreground = 'blue')
        py_text.tag_config('red',foreground = 'red')
        words = self.split_text(context)
        for lines in words:
            notes_flag = False
            for word in lines:
                if notes_flag:
                    py_text.insert(tk.CURRENT,word,'green')
                elif word in self.NOTES_HLS_WORDS:
                    notes_flag = True
                    py_text.insert(tk.CURRENT,word,'green')
                elif word in self.BLUE_HLS_WORDS:
                    py_text.insert(tk.CURRENT,word,'blue')
                elif word in self.LIME_HLS_WORDS:
                    py_text.insert(tk.CURRENT,word,'red')
                else:
                    py_text.insert(tk.CURRENT,word)
            py_text.insert(tk.CURRENT,'\n')


    def split_text(self,context):
        lines = context.split('\n')
        words = list()
        for line in lines:
            for split_word in self.SPLIT_WORDS:
                line = line.replace(split_word,'\n'+split_word+'\n')
            words.append(line.split('\n'))
        return words

    def update_bottom(self,bg = 'burlywood',text="Update",b_width = 20, b_height = 2,b_index_x=100,b_index_y=535):
        update_button = tk.Button(self.root_windows,bg = bg,text=text,width = b_width, height = b_height,command = self.func_update)
        update_button.place(x = b_index_x , y=b_index_y)

    def flush_bottom(self,bg = 'burlywood',text="Flush",b_width = 20, b_height = 2,b_index_x=300,b_index_y=535):
        flush_button = tk.Button(self.root_windows,bg = bg,text=text,width = b_width, height = b_height,command = self.func_flush)
        flush_button.place(x = b_index_x , y=b_index_y)

    def next_bottom(self,bg = 'burlywood',text="Next",b_width = 20, b_height = 2,b_index_x=550,b_index_y=535):
        next_button = tk.Button(self.root_windows,bg = bg,text=text,width = b_width, height = b_height,command = self.func_next)
        next_button.place(x = b_index_x , y=b_index_y)

    def save_bottom(self,bg = 'burlywood',text="Save",b_width = 20, b_height = 2,b_index_x=750,b_index_y=535):
        next_button = tk.Button(self.root_windows,bg = bg,text=text,width = b_width, height = b_height,command = self.func_save)
        next_button.place(x = b_index_x , y=b_index_y)

    def count_label(self):
        self.textvar = tk.StringVar()
        label = tk.Label(self.root_windows,textvariable=self.textvar,bg='snow')
        label.place(x=492 ,y = 548)

    def func_update(self):
        txt = self.case_text.get("0.0","end")
        case_name = self.excel_control.get_current_caseName()
        self.file_control.write_case_file(case_name,txt)
        self.excel_control.set_current_case_result("NOK")

    def func_flush(self):
        self.py_text.delete("0.0","end")
        self.case_text.delete("0.0","end")
        case_name = self.excel_control.get_current_caseName()
        case_context = self.file_control.read_case_file(case_name)
        py_context = self.file_control.read_python_file(case_name)
        self.py_text.insert(tk.INSERT,py_context)
        self.case_text.insert(tk.INSERT,case_context)

    def func_next(self):
        if not self.textvar :
            self.count_label()
        self.count += 1
        self.textvar.set(self.count)
        self.py_text.delete("0.0","end")
        self.case_text.delete("0.0","end")
        self.excel_control.change_next()
        case_name = self.excel_control.get_current_caseName()
        case_context = self.file_control.read_case_file(case_name)
        py_context = self.file_control.read_python_file(case_name)
        self.py_text.insert(tk.INSERT,py_context)
        self.case_text.insert(tk.INSERT,case_context)

    def func_save(self):
        self.excel_control.save_excel()

    def TK_loop(self):
        self.show_paint()
        case_context = self.file_control.read_case_file(self.excel_control.get_current_caseName())
        py_context = self.file_control.read_python_file(self.excel_control.get_current_caseName())
        self.show_case_box_context(case_context)
        self.show_python_box_context(py_context)
        self.update_bottom()
        self.flush_bottom()
        self.next_bottom()
        self.save_bottom()
        self.count_label()
        tk.mainloop()
