#!/usr/bin/python
#-*- coding:UTF-8 -*-
#python 3.6
import re
import requests
import os
import importlib,sys
importlib.reload(sys)
from pypinyin import pinyin, lazy_pinyin
import pypinyin
import urllib


#中文转拼音
def topinyin(str1):
    keys1 = str1.decode('utf-8')
    keys = lazy_pinyin(keys1)
    string = ''
    for key in keys:
        string += key

    return string

# 创建文件
def mkdir(path):

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

# 下载图片
def dowmloadPic(html,keyword,n,key):

    pic_url = re.findall('<img.*?data-src="(.*?)"',html,re.S)

    i = 0
    print ('找到关键词:'+keyword+'的图片，现在开始下载图片...')
    for each in pic_url:
        print ('正在下载第'+str(i+1)+'张图片，图片地址:'+str(each))
        try:
            pic= requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print ('【错误】当前图片无法下载')
            continue
        string = 'picturesnba\\'+keyword+'\\'+str(n)+'_'+str(key)+'_'+str(i) + '.jpg'
        #resolve the problem of encode, make sure that chinese name could be store
        fp = open(string,'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

# 获取列表URL
def getUrl(html,keyword,n):
    urls = re.findall('<h3>\s<a target="_blank" href="(.*?)"', html, re.S)
    print (urls)
    i = 0
    print ('已经获取列表的URL，现在进入URL下载图片...')
    for url in urls:
        print (url)
        result = requests.get(url,keyword)
        dowmloadPic(result.text, keyword,n,i)
        i+=1

#获取前N页是数据
def getPage(word,words,n):
    word =urllib.parse.quote(word)
    url = 'http://weixin.sogou.com/weixin?query=' + word + '&type=2&page='+str(n)
    result = requests.get(url)
    html = re.sub("&amp;", "&", result.text)
    # 获取关键词url
    getUrl(html, words,n)

# main
if __name__ == '__main__':
    word = input("Input key word: ")
    word = word.encode('UTF-8','strict')
    words = topinyin(word)
    mkpath = 'picturesnba\\' + words
    # 创建文件夹
    mkdir(mkpath)
    #判断i<n就循环
    for i in range(0,1):
        getPage(word,words,i)

    print ("采集完成")

