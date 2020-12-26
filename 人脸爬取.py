import sys
import os
import glob
import re
import urllib3
from xml.dom.minidom import parse
import xml.dom.minidom


    

def parsexml(xmlfile):


    DOMTree = xml.dom.minidom.parse(xmlfile)
    Dom = DOMTree.documentElement

    URIs = Dom.getElementsByTagName("playbackURI")
    return URIs


def getImg(xmlfile,file_path1,file_path2,file_path3):
    #create filepath
    big_path = 'pic\\big\\'+file_path1+'\\'+file_path2+'\\'+file_path3+'\\'
    small_path =  'pic\\small\\'+file_path1+'\\'+file_path2+'\\'+file_path3+'\\'
    folder1 = os.path.exists(big_path)
    folder2 = os.path.exists(small_path)
    if not folder1:
        os.makedirs(big_path)
    if not folder2:
        os.makedirs(small_path)

    URIs = parsexml(xmlfile)

    for URI in URIs:
        print(URI.childNodes[0].data)
        imageURL = URI.childNodes[0].data
        print("imageurl",imageURL)
        #字符串分割
        a = imageURL.split("?")
        pic_name = a[1]
        b = a[1].split("&")
        size = int(b[3].split("=")[1])
        #设置大文件>100kb
        if size > 102400:
            file_path = big_path
            saveImage(imageURL,file_path, pic_name)
        else:
            file_path = small_path
            saveImage(imageURL,file_path, pic_name)


def saveImage(imageURL,filePath,pic_name):
    
    http = urllib3.PoolManager()
    header={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Content-Length":"0",
        "Cookie":"language=zh; WebSession_49c055a613=b3f6e8b156493788363a5ee27e6cf836fc5dc730f3d3f562eb22548f699c7bfb",
        "Host":"170.2.229.50",
        "If-Modified-Since":"0",
        "Origin":"http://170.2.229.50",
        # Referer:http://170.2.229.50/doc/page/preview.asp
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With":"XMLHttpRequest"}

#         Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Accept-Encoding:gzip, deflate, sdch
# Accept-Language:zh-CN,zh;q=0.8
# Cache-Control:max-age=0
# Connection:keep-alive
# Cookie:language=zh; WebSession_49c055a613=b3f6e8b156493788363a5ee27e6cf836fc5dc730f3d3f562eb22548f699c7bfb
# Host:170.2.229.50
# Upgrade-Insecure-Requests:1
# User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0

    # 下载单个imageURL的图片
    r = http.request('GET', imageURL,headers=header)
    data = r.data
    f = open(filePath+pic_name+'.jpg', 'wb+')
    f.write(data)
    print(u'正在保存的一张图片为:%s', pic_name+'.jpg')
    f.close()

def processxml(filepath):
    
    if (os.path.exists(filepath)):
        #得到该文件夹路径下下的所有xml文件路径
        f = glob.glob(filepath + '\\*.xml' ) 
    else:
        print('no path')
    
    file_path1 = filepath.split('\\')[-1]
    
    for file in f:
        print(file)
       
        filename = file.split('\\')[-1]
        file_path2 = filename.split('_')[0]
        file_path3 = filename.split('.')[0]
        getImg(file,file_path1,file_path2,file_path3)
    

    

   

if __name__=='__main__':

    processxml('xml\\1211_1220')
