# -*- coding:utf-8 -*-
#python 3.6
#XiaoDeng
#http://tieba.baidu.com/p/2460150866
#标签操作


from bs4 import BeautifulSoup
import urllib.request
import xlwt

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
    word = input("Input key word: ")
    url1 = "http://www.baidu.com/s?ie=utf-8&wd="+urllib.parse.quote(word)
    listall = getkeylist(url1)  #获取所有相关关键词
    print("数据插入开始")

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    # indexing is zero based, row then column
    sheet.write(0, 0, '关键词')
    sheet.write(0, 1, 'url')
    i = 1;
    for item in listall:
        print(item)
        sheet.write(i, 0, item[1])
        sheet.write(i, 1, item[0])
        i += 1;
    wbk.save(word+'.xls')  # 默认保存在桌面上

    print("数据插入成功")
