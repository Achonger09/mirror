#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

class test_case_2(object):
    web_site = 'http://www.17k.com/list/2903409.html'
    def get_website_by_url(self,url):
        if  not url:
            print('website is Null ,please check')
            return False
        response = requests.get(url)
        if response.status_code > 300:
            print('website is unreachable')
            return False
        response.encoding = 'utf-8'
        return response.text

    def get_website_title(self,string):
        if not string:
            print('string is null ,cannot get website title')
            return False
        title = re.findall(r'<h1 class="Title">(.*?)</h1>',string,re.S)
        if not len(title) == 1:
            print('have more than one title ,please check')
            return False
        return title[0]

    def get_chapter_title(self,string):
        if not string:
            print('string is null ,cannot get chapter title and url')
            return False
        director = re.findall(r'<dl class="Volume">.*?</dl>',string,re.S)[0]
        chapter_title = re.findall(r'<span class="ellipsis">(.*?)</span>',director,re.S)
        return chapter_title

    def get_chapter_url(self,string,url):
        if not string:
            print('string is null ,cannot get chapter title and url')
            return False
        director = re.findall(r'<dl class="Volume">.*?</dl>',string,re.S)[0]
        chapter_url = re.findall(r'<a target="_blank" href=(.*?) title',director,re.S)
        chapter_url_list = []
        for chapter_u in chapter_url:
            chapter_url_list.append('%s%s' % (url,chapter_u.replace('\"','')))
        return chapter_url_list

    def get_chapter_content(self,string):
        if not string:
            print('string is null ,cannot get chapter title and url')
            return False
        chapter_content = re.findall(r'<div class="p">(.*?)<div class="author-say">',string,re.S)[0]
        return chapter_content

    def clear_string(self,string):
        if not string:
            print('string is null ,cannot get chapter title and url')
            return False
        string = string.replace('&#12288;','')
        string = string.replace(' ','')
        string = string.replace('<br/><br/>','\n')
        return string

if __name__ == '__main__':
    spiter = Spiter_17k_oop()
    content = spiter.get_website_by_url('http://www.17k.com/list/2914993.html')
    title = spiter.get_website_title(content)
    file = open('%s.txt' %spiter.clear_string(title),mode='w',encoding='utf-8')
    chapter_title_list = spiter.get_chapter_title(content)
    chapter_title_url = spiter.get_chapter_url(content,url='http://www.17k.com')
    if not len(chapter_title_list) == len(chapter_title_url):
        print('%s get chapter title not match url' % title)
        exit(0)
    for i in range(0,len(chapter_title_url)):
        file.write(chapter_title_list[i])
        print(chapter_title_url[i])
        chapter_content = spiter.get_chapter_content(spiter.get_website_by_url(chapter_title_url[i]))
        file.write(spiter.clear_string(chapter_content))
