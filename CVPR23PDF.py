# coding = UTF-8
# 爬取自己编写的html链接中的PDF文档,网址：file:///E:/ZjuTH/Documents/pythonCode/pythontest.html

import urllib.request
import re
import os
from tqdm import tqdm


def norm_title(title):
    title = title.replace(':', '：')
    title = title.replace('： ', '：')
    title = title.replace('\\xc2\\xb2', '2')
    title = title.replace('\\xe2\\x80\\x9c', '\'')
    title = title.replace('\\xe2\\x80\\x93', '\'')
    title = title.replace('\\xe2\\x80\\x9d', '')
    title = title.replace('\\xe2\\x80\\x99', '\'')
    title = title.replace('\\xe2\\x88\\x98', '')
    title = title.replace('\\xc2\\xa0', ' ')
    title = title.replace('\\xc3\\xa9', 'e')
    title = title.replace('\\xe2\\x82\\x81', '1')
    title = title.replace('\\xc2\\xb3', '3')
    title = title.replace('\\\\&amp;', '&')
    title = title.replace('&#x27;', "'")
    title = title.replace('?', '')
    title = title.replace('/', '-')
    title = title.replace('\\\\%', '%')
    title = title.replace('\\\\${\\\\textasciicircum', '2fM: Structure From Motion on Neural Level Set of Implicit Surfaces')
    return title

# open the url and read
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()
    return html

# compile the regular expressions and find
# all stuff we need
def getUrl(html):
    reg = r'(?:href|HREF)="?((?:/content/CVPR2023/papers/)?.+?\.pdf)'
    url_re = re.compile(reg)
    url_list = url_re.findall(html.decode('UTF-8')) #返回匹配的数组
    url_list = [url.split('/')[-1] for url in url_list if 'paper' in url and 'supplemental' not in url]
    return(url_list)


def getFile(url, title, save_to):
    path = os.path.join(save_to, title)
    if not os.path.exists(path):
        u = urllib.request.urlopen(url)
        f = open(path, 'wb')

        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            f.write(buffer)
        f.close()

root_url_0 = 'https://openaccess.thecvf.com'
root_url = '/content/CVPR2023/papers/'  #下载地址中相同的部分

raw_url = 'https://openaccess.thecvf.com/CVPR2023?day=all'

html = getHtml(raw_url)
url_lst = getUrl(html)

root_dir = 'E:\Desktop\CVPR23'
paper_dir = os.path.join(root_dir, 'paper')
if not os.path.exists(root_dir): os.mkdir(root_dir)
if not os.path.exists(paper_dir): os.mkdir(paper_dir)

content_list = str(html).split('title     = {')[1:]
title_list = [title.split('}')[0] for title in content_list]
assert len(title_list) == len(url_lst)

for i, (title, url) in enumerate(zip(title_list, url_lst[:])):
    url = root_url_0 + root_url + url  #形成完整的下载地址
    title = norm_title(title) + '.pdf'
    getFile(url, title, save_to=paper_dir)
    print (f"{i}, Sucessful downloaded" + " " + title)