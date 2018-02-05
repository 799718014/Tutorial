# -*- coding:utf-8 -*-
#python 2.7
#XiaoDeng
#http://tieba.baidu.com/p/2460150866
#标签操作


from bs4 import BeautifulSoup
import urllib.request
from dbbaidu import select,insert
import re

def get_content(url):
    #如果是网址，可以用这个办法来读取网页
    html_doc = url
    req = urllib.request.Request(html_doc)
    webpage = urllib.request.urlopen(req)
    html = webpage.read()

    soup = BeautifulSoup(html, 'html.parser')   #文档对象

    ids = soup.find(id="rs")            #查找id=rs的代码
    soup.find_all('a')

    lists = []   #字典
    i = 0
    # 类名为xxx而且文本内容为hahaha的div
    for k in ids.find_all('a'):      #,string='更多'
        url = 'http://www.baidu.com'+k.get('href')
        title = k.get_text()
        lists.append([url,title])
        i+=1
    return  lists;

#获取所有相关关键词
def getkeylist(url1):
    listall = []  # 全部关键词
    lister = []  # 二级相关关键词
    # 跟据网址获取相关关键词
    lists = get_content(url1)
    for item in lists:
        # 获取二级相关关键词
        lister = get_content(item[0])
        # 把目标关键词加到列表
        lister.append(item)
        # 把两个列表合并成一个列表
        listall.extend(lister)
    return listall


# main
if __name__ == '__main__':
    url1 = "http://www.baidu.com/s?ie=utf-8&wd=%E6%99%BA%E8%83%BD%E6%89%8B%E7%8E%AF"
    listall = getkeylist(url1)  #获取所有相关关键词

    #sql语句
    sql2 = """INSERT INTO `baidu` (`name`, `url`) VALUES """
    sql1 = ""
    i=0
    #循环列表插入数据库
    for item in listall:
        if(i==0):
            sql1 += """('""" + item[1] + """', '""" + item[0] + """')"""
        else:
            sql1 += """,('""" + item[1] + """', '""" + item[0] + """')"""

        i+=1;
        break

    sql = sql1
    print("开始插入数据")
    print(sql)
    # 插入数据库
    res = insert(sql)
    if(res):
        print("抓取成功")
    else:
        print("抓取失败")

#查询数据库
# select()
