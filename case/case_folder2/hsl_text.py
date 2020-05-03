#!/usr/bin/env python
# -*- coding: utf-8 -*-

file_path = 'D:\\python_demo\\view_case_and_python\\case_folder1\\test_case_001\\test_case_1.py'

with open(file_path,'r') as f:
    context = f.read()

split_words = ['.','(',')']
hls_words = ['clear_string']

def split_text(context,split_words):
    lines = context.split('\n')
    words = list()
    for line in lines:
        for split_word in split_words:
            line = line.replace(split_word,'\n'+split_word+'\n')
        words.append(line.split('\n'))
    return words
print(split_text(context,split_words))