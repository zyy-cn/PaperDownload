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
    reg = r'(?:href|HREF)="?((?:papers/eccv_2024/papers_ECCV/papers/)?.+?\.pdf)'
    # a href=\'papers/eccv_2020/papers_ECCV/papers/123460001.pdf
    url_re = re.compile(reg)
    # pdf_url = url_re.findall(html.decode('gb2312'))
    url_list = url_re.findall(html.decode('UTF-8')) #返回匹配的数组
    url_list = [url.split('/')[-1] for url in url_list if '2024' in url and 'supp' not in url]
    return(url_list)

def norm_title(title):
    title = title + '.pdf'
    title = title.replace(':', '：')
    title = title.replace('： ', '：')
    title = title.replace('"', '')
    title = title.replace('*', '')
    title = title.replace('\\\\&', '&')
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
    title = title.replace('\\xc3\\xb6', 'ö')
    title = title.replace('\\xc2\\xb0', '°')
    title = title.replace('\\xc3\\x97', '×')
    title = title.replace('&#x27;', "'")
    title = title.replace("\\'", "'")
    title = title.replace('?', '')
    title = title.replace('/', '-')
    title = title.replace('\\xe2\\x80\\x94', '—')
    title = title.replace('$', '')
    title = title.replace('\\\\el', '')
    title = title.replace('\\\\infty', 'infty')
    title = title.replace('^\\\\rho', 'ρ')
    title = title.replace('\\xc3\\x9c', 'Ü')
    title = title.replace('\\\\texttt{\\\\textbf{PointScatter}}', 'PointScatter')
    title = title.replace('\\\\textit{Radiance}', 'Radiance')
    title = title.replace('\\\\textit{Light}', 'Light')
    title = title.replace('\\\\textit{Zero Level Set}', 'Zero Level Set')
    title = title.replace('\\xe2\\x88\\x9e', '∞')
    title = title.replace('\\\\\\\\beta', 'beta')
    title = title.replace('\\xce\\xb5', 'ε')

    return title


def getFile(url, save_path):



    f = open(save_path, 'wb')

    u = urllib.request.urlopen(url)
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()



root_url = 'https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/'  #下载地址中相同的部分

raw_url = 'https://www.ecva.net/papers.php'

html = getHtml(raw_url)
# url_lst = getUrl(html)

content_list = str(html).split('ptitle')[1:]
content_list = [c for c in content_list if '2024' in c]
file_name_list = [c.split('</a>')[1].split("=\\'")[1].split('/')[-1].split("\\'")[0] for c in content_list if '2024' in c]
title_list = [c.split('</a>')[0].split('\\n')[-1] for c in content_list if '2024' in c]
assert len(title_list) == len(file_name_list)

root_dir = 'E:\Desktop\ECCV24'
paper_dir = os.path.join(root_dir, 'paper')
if not os.path.exists(root_dir): os.mkdir(root_dir)
if not os.path.exists(paper_dir): os.mkdir(paper_dir)
full_paper_url = [root_url + url for url in file_name_list]

for i, (file, title) in enumerate(zip(file_name_list, title_list)):
    url = root_url + file  #形成完整的下载地址
    title = norm_title(title)

    path = os.path.join(paper_dir, title)
    if not os.path.exists(path):
        getFile(url, save_path=path)
        print(f"{i+1}/{len(file_name_list)}\tSucessful downloaded" + " " + title)
    else:
        print(f"{i+1}/{len(file_name_list)}\t{title} existed")