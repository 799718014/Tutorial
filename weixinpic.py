#-*- coding:utf-8 -*-
import re
import requests
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


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

        print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False

# 下载图片
def dowmloadPic(html,keyword,n,key):

    pic_url = re.findall('<img.*?data-src="(.*?)"',html,re.S)

    i = 0
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for each in pic_url:
        print '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each)
        try:
            pic= requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
            continue
        string = 'picturesnba\\'+keyword+'\\'+str(n)+'_'+str(key)+'_'+str(i) + '.jpg'
        #resolve the problem of encode, make sure that chinese name could be store
        fp = open(string.decode('utf-8').encode('cp936'),'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

# 获取列表URL
def getUrl(html,keyword,n):
    urls = re.findall('<h3>\s<a target="_blank" href="(.*?)"', html, re.S)
    print urls
    i = 0
    print '已经获取列表的URL，现在进入URL下载图片...'
    for url in urls:
        print url
        result = requests.get(url,keyword)
        dowmloadPic(result.text, keyword,n,i)
        i+=1

#获取前N页是数据
def getPage(word,n):
    url = 'http://weixin.sogou.com/weixin?query=' + word + '&type=2&page='+str(n)
    print url
    result = requests.get(url)
    html = re.sub("&amp;", "&", result.text)
    # 获取关键词url
    getUrl(html, word,n)

# main
if __name__ == '__main__':
    word = raw_input("Input key word: ")
    mkpath = 'picturesnba\\' + word.encode('gb2312')
    # 创建文件夹
    mkdir(mkpath)
    #判断i<n就循环
    for i in range(0,3):
        getPage(word,i)

    print "采集完成"
'''
    url = 'http://weixin.sogou.com/weixin?query='+word+'&type=2&page=1'
    result = requests.get(url)

    html = re.sub("&amp;", "&",  result.text)

    # 获取关键词url
    getUrl(html,word)
    #dowmloadPic(html,word)
'''


