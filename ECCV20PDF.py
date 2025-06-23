# coding = UTF-8
# 爬取自己编写的html链接中的PDF文档,网址：file:///E:/ZjuTH/Documents/pythonCode/pythontest.html

import urllib.request
import re
import os
from tqdm import tqdm

# open the url and read
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()
    return html

# compile the regular expressions and find
# all stuff we need
def getUrl(html):
    # reg = r'([A-Z]\d+)' #匹配了G176200001
    reg = r'(?:href|HREF)="?((?:papers/eccv_2020/papers_ECCV/papers/)?.+?\.pdf)'
    # a href=\'papers/eccv_2020/papers_ECCV/papers/123460001.pdf
    url_re = re.compile(reg)
    # pdf_url = url_re.findall(html.decode('gb2312'))
    url_list = url_re.findall(html.decode('UTF-8')) #返回匹配的数组
    url_list = [url.split('/')[-1] for url in url_list if '2020' in url and 'supp' not in url]
    return(url_list)


def getFile(url, save_to):
    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(os.path.join(save_to, file_name), 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()

    print ("Sucessful downloaded" + " " + file_name)


root_url = 'https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/'  #下载地址中相同的部分

raw_url = 'https://www.ecva.net/papers.php'

html = getHtml(raw_url)
url_lst = getUrl(html)


root_dir = 'E:\Desktop\ECCV20'
paper_dir = os.path.join(root_dir, 'paper')
if not os.path.exists(root_dir): os.mkdir(root_dir)
if not os.path.exists(paper_dir): os.mkdir(paper_dir)
full_paper_url = [root_url + url for url in url_lst]

for url in url_lst[:]:
    url = root_url + url  #形成完整的下载地址
    getFile(url, save_to=paper_dir)